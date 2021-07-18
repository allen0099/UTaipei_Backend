import json
import re
from typing import Any
from urllib.parse import unquote

import requests
from flask import Response, abort, redirect, request, session, url_for
from lxml import etree
from lxml.etree import _Element

from models import Collection
from routes.api import api


@api.route("/choose", methods=['POST'])
def choose() -> Response:
    _: str = request.cookies.get('settings')

    if _ is None:
        return redirect('/')

    _: str = unquote(_)
    settings: dict = json.loads(_)
    data: dict = request.form

    url: str = "http://shcourse.utaipei.edu.tw/utaipei/ag_pro/ag203_1.jsp"

    year: int = settings['year']
    semester: int = settings['semester']
    if semester not in [1, 2, 3]:
        return abort(404)

    options = values(year, semester)
    degree: str = data['degree']
    if degree not in options["degree"]:
        return abort(404)

    department: str = data["department"]
    if department not in options["department"]:
        return abort(404)

    unit: str = data["unit"]
    if unit not in options["unit"]:
        return abort(404)

    class_year: str = data["year"]
    if class_year not in options["class_year"]:
        return abort(404)

    class_type: str = data["attr"]
    if class_type not in options["class_type"]:
        return abort(404)

    course_name: str = data["subject"]
    teacher: str = data["teacher"]

    response: dict[str, Any] = {
        "search_word": {
            "year": year,
            "semester": semester,
            "degree": degree,
            "department": department,
            "unit": unit,
            "class_year": class_year,
            "class_type": class_type,
            "course_name": course_name,
            "teacher": teacher,
        },
        "available_options": options,
    }
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
        "clyear": f"{class_year}",
        "class_type": f"{class_type}",
        "sub_name": f"{course_name}",
        "teacher": f"{teacher}",
        "ls_year": f"{year}",
        "ls_sms": f"{semester}",
        "hid_crk": "%",  # hidden value
        "ls_years": "0",  # hidden value
        "ls_smss": "0",  # hidden value
    }

    r = requests.post(url, data=params, headers=headers)
    if r.status_code != 200:
        # return abort error...
        return abort(r.status_code)

    root: _Element = etree.HTML(r.text)

    error: list[_Element] = root.xpath('//body//script[@language]')
    if error:
        reg = re.findall(r'(?<=alert\(\").*(?=\"\))', error[0].text)

        response["error"] = reg[0]
        session["data"] = response
        return redirect(url_for('result'))

    head: str = root.xpath('//html//body//table//font[@color]')[0].text
    reg = re.findall(r'(?<=\(共)\d+', head)
    total: int = int(reg[0])

    class_table: list[_Element] = root.xpath("//body//table[@id='list_table']//tr[not(@align='center')]")

    list_classes: list[Collection] = []

    if total > 0:
        for row in class_table:
            class_ = Collection(iter(row))
            list_classes.append(class_)

    response["total"] = total
    response["classes"] = [_.to_dict() for _ in list_classes]
    session["data"] = response
    return redirect(url_for('routes.result'))


def values(year, semester) -> dict[str, list[str]]:
    url: str = "http://shcourse.utaipei.edu.tw/utaipei/ag_pro/ag203.jsp"

    headers: dict[str, str] = {
        "Host": "shcourse.utaipei.edu.tw",
        "Connection": "keep-alive",
        "Content-Type": "application/x-www-form-urlencoded",
    }
    params: dict[str, str] = {
        "yms_yms": f"{year}#{semester}",
        "dgr_id": "%",
        "dpt_id": "%",
        "unt_id": "%",
        "clyear": "%",
        "class_type": "",
        "sub_name": "",
        "teacher": "",
        "ls_year": f"{year}",
        "ls_sms": f"{semester}",
        "hid_crk": "",  # hidden value
        "ls_years": "0",  # hidden value
        "ls_smss": "0",  # hidden value
    }

    r = requests.post(url, data=params, headers=headers)
    if r.status_code != 200:
        return abort(r.status_code)

    root: _Element = etree.HTML(r.text)
    degree: list[_Element] = root.xpath("//select[@id='dgr_id']/*")
    department: list[_Element] = root.xpath("//select[@id='dpt_id']/*")
    unit: list[_Element] = root.xpath("//select[@id='unt_id']/*")
    class_year: list[_Element] = root.xpath("//select[@id='clyear']/*")
    class_type: list[_Element] = root.xpath("//select[@id='class_type']/*")

    return {
        "degree": [_.attrib['value'] for _ in degree],
        "department": [_.attrib['value'] for _ in department],
        "unit": [_.attrib['value'] for _ in unit],
        "class_year": [_.attrib['value'] for _ in class_year],
        "class_type": [_.attrib['value'] for _ in class_type],
    }
