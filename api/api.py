import logging
import typing as t
from abc import ABC
from abc import abstractmethod

from httpx import Response
from lxml import etree
from typing_extensions import override

from http_client import RequestClient
from utils import get_semester
from utils import get_year

from .common import VALIDATE_RULES
from .exceptions import WrapperAPIException

if t.TYPE_CHECKING:
    from lxml.etree import _Element

logger: logging.Logger = logging.getLogger(__name__)

_T = t.TypeVar("_T")


class _APIBase(ABC):
    URL: str = "https://shcourse.utaipei.edu.tw/utaipei/ag_pro/ag203.jsp"

    __slots__ = [
        "year",
        "semester",
        "degree",
        "department",
        "unit",
        "class_year",
        "class_type",
        "sub_name",
        "teacher",
        "hid_crk",
    ]

    def __init__(
            self,
            *,
            year: int | None = None,
            semester: int | None = None,
            degree: str = "%",
            department: str = "%",
            unit: str = "%",
            class_year: str = "%",
            class_type: str = "",
            sub_name: str = "",
            teacher: str = "",
            hid_crk: str = "",
    ) -> None:
        self.year: int = year or get_year()
        self.semester: int = semester or get_semester()
        self.degree: str = degree
        self.department: str = department
        self.unit: str = unit
        self.class_year: str = class_year
        self.class_type: str = class_type
        self.sub_name: str = sub_name
        self.teacher: str = teacher
        self.hid_crk: str = hid_crk

    @staticmethod
    def _get_header() -> dict[str, str]:
        return {
            "Host": "shcourse.utaipei.edu.tw",
            "Connection": "keep-alive",
            "Content-Type": "application/x-www-form-urlencoded",
        }

    def _get_data(self) -> dict[str, str]:
        self._validate_params()

        return {
            "yms_yms": f"{self.year}#{self.semester}",  # 學年期(Academic Year & Semester)
            "dgr_id": f"{self.degree}",  # 學制(Level)
            "dpt_id": f"{self.department}",  # 學院(College)
            "unt_id": f"{self.unit}",  # 科系(Department / Program)
            "clyear": f"{self.class_year}",  # 年級(Grades)
            "class_type": f"{self.class_type}",  # 屬性(Course Type)
            "sub_name": f"{self.sub_name}",  # 科目(Course Name)
            "teacher": f"{self.teacher}",  # 教師(Instructor)
            "ls_year": f"{self.year}",  # hidden value
            "ls_sms": f"{self.semester}",  # hidden value
            "hid_crk": f"{self.hid_crk}",  # 類別(Category) hidden value
            "ls_years": "0",  # hidden value
            "ls_smss": "0",  # hidden value
        }

    def _validate_params(self) -> None:
        for k, v in VALIDATE_RULES.items():
            if not v(getattr(self, k)):
                raise WrapperAPIException(f"Invalid '{k}', got '{getattr(self, k)}'")

    def _get_response(self) -> Response:
        with RequestClient() as client:
            result: Response = client.post(
                self.URL,
                data=self._get_data(),
                headers=self._get_header(),
            )

            if not result.is_success:
                raise WrapperAPIException("Failed to get result", self.URL, result.text)

            return result

    def is_alive(self) -> bool:
        try:
            self._get_response()
            return True

        except WrapperAPIException as e:
            logger.error(e)
            return False

    @abstractmethod
    def result(self) -> list[tuple[str, str]]:
        ...


class _CommonAPI(_APIBase, ABC):
    def __init__(
            self,
            *,
            year: int | None = None,
            semester: int | None = None,
    ) -> None:
        super().__init__(
            year=year or get_year(),
            semester=semester or get_semester(),
            degree="%",
            department="%",
            unit="%",
            class_year="%",
            class_type="",
            sub_name="",
            teacher="",
            hid_crk="",
        )


class GetCategory(_CommonAPI):
    URL: str = "https://shcourse.utaipei.edu.tw/utaipei/ag_pro/ag203_crk.jsp"

    @override
    def _get_data(self) -> dict[str, str]:
        self._validate_params()

        return {
            "ls_year": f"{self.year}",
            "ls_sms": f"{self.semester}",
        }

    def result(self) -> list[tuple[str, str]]:
        response: Response = self._get_response()

        root: _Element = etree.HTML(response.text)
        degree: list[_Element] = root.xpath("//select/*")

        return [(_.attrib["value"], _.text) for _ in degree]


class GetDegree(_CommonAPI):
    def result(self) -> list[tuple[str, str]]:
        response: Response = self._get_response()

        root: _Element = etree.HTML(response.text)
        degree: list[_Element] = root.xpath("//select[@id='dgr_id']/*")

        return [(_.attrib["value"], _.text) for _ in degree]


class GetDepartments(_CommonAPI):
    def result(self) -> list[tuple[str, str]]:
        response: Response = self._get_response()

        root: _Element = etree.HTML(response.text)
        department: list[_Element] = root.xpath("//select[@id='dpt_id']/*")

        return [(_.attrib["value"], _.text) for _ in department if _.attrib["value"] != ""]


class GetClassYear(_CommonAPI):
    def result(self) -> list[tuple[str, str]]:
        response: Response = self._get_response()

        root: _Element = etree.HTML(response.text)
        class_year: list[_Element] = root.xpath("//select[@id='clyear']/*")

        return [(_.attrib["value"], _.text) for _ in class_year]


class GetClassType(_CommonAPI):
    def result(self) -> list[tuple[str, str]]:
        response: Response = self._get_response()

        root: _Element = etree.HTML(response.text)
        class_type: list[_Element] = root.xpath("//select[@id='class_type']/*")

        return [(_.attrib["value"], _.text) for _ in class_type]
