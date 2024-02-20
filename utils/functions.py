import logging
import re
import typing as t
from re import Match

from httpx import Response
from lxml import etree
from lxml.etree import _Element

from api.common import Degree, Department, Grade, Unit
from exceptions import UTCAPIException
from http_client import RequestClient
from utils import get_semester, get_year

logger: logging.Logger = logging.getLogger(__name__)


def pure_text(text: str) -> str:
    return re.sub(r"\s+", "", text).replace("\xa0", "").replace("\u3000", "")


def get_courses(
    year: int | None = None,
    semester: int | None = None,
    degree: Degree = Degree.ALL,
    department: Department = Department.ALL,
    unit: Unit = Unit.ALL,
    grade: Grade = Grade.ALL,
    category: str = "",
    course_name: str = "",
    teacher: str = "",
) -> list[dict[str, t.Any]]:
    data: list[dict[str, t.Any]] = []

    if year is None:
        year = get_year()

    if semester is None:
        semester = get_semester()

    for course in iter_courses(
        raw_response(
            year, semester, degree.value, department.value, unit.value, grade.value, category, course_name, teacher
        )
    ):
        data.append(jsonify_course(iter(course)))

    return data


def raw_response(
    year: int,
    semester: int,
    degree: str = "%",
    department: str = "%",
    unit: str = "%",
    grade: str = "%",
    hid_crk: str = "%",
    course_name: str = "",
    teacher: str = "",
) -> Response:
    url: str = "https://shcourse.utaipei.edu.tw/utaipei/ag_pro/ag203_1.jsp"
    headers: dict[str, str] = {
        "Host": "shcourse.utaipei.edu.tw",
        "Connection": "keep-alive",
        "Content-Type": "application/x-www-form-urlencoded",
    }
    params: dict[str, str] = {
        "yms_yms": f"{year}#{semester}",
        "dgr_id": f"{degree}",
        "dpt_id": f"{department}",
        "unt_id": f"{unit}",
        "clyear": f"{grade}",
        "class_type": "",
        "sub_name": f"{course_name}",
        "teacher": f"{teacher}",
        "ls_year": f"{year}",
        "ls_sms": f"{semester}",
        "hid_crk": f"{hid_crk}",  # hidden value
        "ls_years": "0",  # hidden value
        "ls_smss": "0",  # hidden value
    }

    with RequestClient() as client:
        result: Response = client.post(url, data=params, headers=headers)

        if not result.is_success:
            raise UTCAPIException(f"Failed to get data from UTC API, status code: {result.status_code}")

        return result


def iter_courses(response: Response) -> t.Generator[_Element, None, None]:
    root: _Element = etree.HTML(response.text)
    error: list[_Element] = root.xpath("//body//script[@language]")

    if error:
        raise UTCAPIException(f"Failed to get data from UTC API, error: {error[0].text}")

    head: str = root.xpath("//html//body//table//font[@color]")[0].text
    reg = re.findall(r"(?<=\(共)\d+", head)
    total: int = int(reg[0])

    class_table: list[_Element] = root.xpath("//body//table[@id='list_table']//tr[not(@align='center')]")

    if total > 0:
        for row in class_table:
            yield row


def get_course_name(el: _Element) -> dict[str, str]:
    text: str = pure_text(el.text)
    tag: str | None = None

    if el.getchildren():
        tag = pure_text(el.getchildren()[0].text)

    return {
        "text": text,
        "tag": tag,
    }


def jsonify_course(course: t.Iterator[_Element]) -> dict[str, t.Any]:
    data: dict[str, t.Any] = {}

    data["class_name"] = pure_text(next(course).text)
    data["course_code"] = pure_text(next(course).text)
    data["category"] = pure_text(next(course).text)

    data["name"] = {
        "chinese": get_course_name(next(course)),
        "english": get_course_name(next(course)),
    }

    data["credit"] = pure_text(next(course).text)
    data["full_half"] = pure_text(next(course).text)
    data["req_select"] = pure_text(next(course).text)
    data["lecturing_hours"] = pure_text(next(course).text)

    people_counts: list[str] = pure_text(next(course).text).split("/")
    data["enrolled"] = {
        "max": people_counts[0],
        "min": people_counts[1],
        "current": people_counts[2],
    }
    data["campus"] = pure_text(next(course).text)

    data["teachers"] = v2(next(course).text)

    data["mixed"] = pure_text(next(course).text)
    data["syllabus"] = re.findall(r"(?<=go_next\(').+(?='\))", next(course).attrib["onclick"])[0]

    tmp = next(course)

    data["notes"] = pure_text(tmp.text)

    if len(tmp.getchildren()) > 1:
        data["limit"] = True
    else:
        data["limit"] = False

    return data


def v2(text: str) -> list[dict[str, t.Any]]:
    data: list[dict[str, t.Any]] = [new_split_teacher_time_location(pure_text(_)) for _ in text.splitlines() if _ != ""]

    logger.info("Data length: %s", len(data))

    if len(data[-1]["times"]) >= 1:
        last_location = data[-1]["times"][-1]["location"]

        for locations in data:
            for time in locations["times"]:
                if time["location"] == "":
                    time["location"] = last_location

    return data


def calc_time(time: str | None) -> list[int]:
    time_list: list[int] = []

    if time is not None:
        split = time.split("-", maxsplit=1)

        if len(split) == 1:
            time_list.append(int(split[0]))

        else:
            time_list = list(range(*map(lambda t: int(t[1]) + t[0], enumerate(split))))

    return time_list


def find_location(text: str | None = None) -> str:
    if text is None:
        return ""

    test: re.Match | None = re.search(r"(?<=[(\[]).*(?=[)\]])", text)
    if test:
        return test.group(0)
    return ""


def new_split_teacher_time_location(text: str) -> dict[str, t.Any]:
    teacher_obj = dict(
        teacher="",
        single_week=False,
        times=[],
    )

    if text.startswith("(單週)"):
        teacher_obj["single_week"] = True
        text = text.replace("(單週)", "", 1)

    if test := re.search(r"^.+?(?=[\[(])", text):  # NOSONAR, this is a valid regex
        teacher_name: str = test.group(0)
        teacher_obj["teacher"] = teacher_name

        text = text.replace(teacher_name, "", 1)

    if reg := [
        _
        for _ in re.finditer(
            r"(?P<day>\([一二三四五六日]\)|時間未定)(?P<time>\d{1,2}(?:-\d{1,2})?)?(?P<location>[\[(][^])]{2,}[])])?",
            text,
        )
    ]:
        for _ in reg:
            teacher_obj["times"].append(
                {
                    "day": _.group("day").split("(", 1)[1].rsplit(")", 1)[0],
                    "time": calc_time(_.group("time")),
                    "location": find_location(_.group("location")),
                }
            )

    return teacher_obj
