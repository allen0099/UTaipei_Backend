import logging

from httpx import Response
from lxml import etree
from lxml.etree import _Element

from utils import get_semester, get_year
from .api import _APIBase
from .common import Department

logger: logging.Logger = logging.getLogger(__name__)


class UnitBase(_APIBase):
    def result(self) -> list[tuple[str, str]]:
        response: Response = self._get_response()

        root: _Element = etree.HTML(response.text)
        unit: list[_Element] = root.xpath("//select[@id='unt_id']/*")

        return [(_.attrib["value"], _.text) for _ in unit if _.attrib["value"] != ""]


class GetUnit(UnitBase):
    pass


class GetUnitByDepartment(UnitBase):
    def __init__(
        self,
        department: Department = Department.ALL,
        *,
        year: int = get_year(),
        semester: int = get_semester(),
    ) -> None:
        super().__init__(
            year=year,
            semester=semester,
            degree="%",
            department=department.value,
            unit="%",
            class_year="%",
            class_type="",
            sub_name="",
            teacher="",
            hid_crk="",
        )
