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

    data["teachers"], data["times"] = split_teacher_time(pure_text(next(course).text))

    data["mixed"] = pure_text(next(course).text)
    data["syllabus"] = re.findall(r"(?<=go_next\(').+(?='\))", next(course).attrib["onclick"])[0]

    tmp = next(course)

    data["notes"] = pure_text(tmp.text)

    if len(tmp.getchildren()) > 1:
        data["limit"] = True
    else:
        data["limit"] = False

    return data


def split_teacher_time(text: str) -> tuple[list[str], list[dict[str, t.Union[str, list[str]]]]]:
    if "/" in text:
        tmp = text.split("/")
        teachers = [tmp[0]]
        times = [
            {
                "day": tmp[1],
                "time": [""],
            }
        ]
    else:
        reg: list[Match] = [
            _
            for _ in re.finditer(
                r"(?P<teacher>.*?) ?\(?(?P<day>(?<=\().(?=\))|時間未定)\)?(?P<time>\d{1,3}(?:-\d{1,3})?)?(?:\((?P<location>.*?)\))?",
                text,
            )
        ]

        if reg:
            teachers = [pure_text(_.group("teacher")) for _ in reg if _.group("teacher") != ""]

            times = [
                {
                    "day": _.group("day"),
                    "time": (
                        list(range(*map(lambda t: int(t[1]) + t[0], enumerate(_.group("time").split("-", maxsplit=1)))))
                        if _.group("time") is not None and "-" in _.group("time")
                        else [] if _.group("time") is None else [_.group("time")]
                    ),
                }
                for _ in reg
            ]

            # remove duplicate dict from https://stackoverflow.com/a/9428041
            times = [i for n, i in enumerate(times) if i not in times[n + 1 :]]
        else:
            teachers = [text]
            times = [
                {
                    "day": "",
                    "time": [""],
                }
            ]

    return teachers, times
