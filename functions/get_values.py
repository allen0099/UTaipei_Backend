import requests
from lxml import etree
from lxml.etree import _Element
from werkzeug.exceptions import abort

from . import get_crk


def get_values(year, semester) -> dict[str, list[str]]:
    url: str = "https://shcourse.utaipei.edu.tw/utaipei/ag_pro/ag203.jsp"

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
        "crk": get_crk(year, semester),
        "class_year": [_.attrib['value'] for _ in class_year],
        "class_type": [_.attrib['value'] for _ in class_type],
    }
