import logging
from typing import Annotated

from fastapi import APIRouter, Depends, Query, Response

from api import GetCategory, GetDepartments, GetNotification, GetUnit, GetUnitByDepartment
from api.common import DEGREE_MAP, Degree, Department, Grade, Unit
from responses import success_response
from utils import get_semester, get_year
from utils.functions import get_courses

logger: logging.Logger = logging.getLogger(__name__)

router = APIRouter(tags=["API Calls"])


async def _year_semester(
    year: Annotated[
        int | None,
        Query(
            description=f"The class year, minimal: 98, max: {get_year()}",
            ge=98,
            le=get_year(),
        ),
    ] = get_year(),
    semester: Annotated[
        int | None,
        Query(
            description="The class semester, between 1 to 5",
            ge=1,
            le=5,
        ),
    ] = get_semester(),
):
    return {"year": year, "semester": semester}


YearSMS = Annotated[dict, Depends(_year_semester)]


@router.get("/degree")
async def get_degree() -> Response:
    """
    Get all degree
    """
    return success_response(
        [
            {
                "id": key,
                "name": value,
            }
            for key, value in DEGREE_MAP.items()
        ]
    )


@router.get("/departments")
async def get_departments(commons: YearSMS) -> Response:
    """
    Get all departments
    """
    return success_response(
        [
            {
                "id": department[0],
                "name": department[1],
            }
            for department in GetDepartments(year=commons.get("year"), semester=commons.get("semester")).result()
        ]
    )


@router.get("/units")
async def get_units(
    commons: YearSMS, department: Annotated[Department, Query(description="The department id")] = None
) -> Response:
    """
    Get units by department
    """
    if department:
        return success_response(
            [
                {
                    "id": unit[0],
                    "name": unit[1],
                }
                for unit in GetUnitByDepartment(
                    year=commons.get("year"),
                    semester=commons.get("semester"),
                    department=department,
                ).result()
            ]
        )

    return success_response(
        [
            {
                "id": unit[0],
                "name": unit[1],
            }
            for unit in GetUnit(year=commons.get("year"), semester=commons.get("semester")).result()
        ]
    )


@router.get("/category")
async def get_category(commons: YearSMS) -> Response:
    """
    Get all category
    """
    return success_response(
        [
            {
                "id": category[0],
                "name": category[1],
            }
            for category in GetCategory(year=commons.get("year"), semester=commons.get("semester")).result()
        ]
    )


@router.get("/notification")
async def get_notification() -> Response:
    """
    Get all notification
    """
    return success_response(GetNotification().result())


@router.get("/courses")
async def _get_courses(
    commons: YearSMS,
    category: Annotated[str, Query(description="The category")] = "%",
    degree: Annotated[Degree, Query(description="The degree")] = Degree.ALL,
    department: Annotated[Department, Query(description="The department id")] = Department.ALL,
    unit: Annotated[Unit, Query(description="The unit id")] = Unit.ALL,
    grade: Annotated[Grade, Query(description="The grade")] = Grade.ALL,
    course_name: Annotated[str, Query(description="The course name")] = "",
    teacher: Annotated[str, Query(description="The teacher name")] = "",
) -> Response:
    """
    Get courses
    """
    return success_response(
        get_courses(
            commons.get("year"),
            commons.get("semester"),
            degree,
            department,
            unit,
            grade,
            category,
            course_name,
            teacher,
        )
    )
