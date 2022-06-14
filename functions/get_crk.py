import requests
from lxml import etree
from lxml.etree import _Element
from werkzeug.exceptions import abort


def get_crk(year, semester):
    url: str = "https://shcourse.utaipei.edu.tw/utaipei/ag_pro/ag203_crk.jsp"
    headers: dict[str, str] = {
        "Host": "shcourse.utaipei.edu.tw",
        "Connection": "keep-alive",
        "Content-Type": "application/x-www-form-urlencoded",
    }
    params: dict[str, str] = {
        "ls_year": f"{year}",
        "ls_sms": f"{semester}",
    }

    r = requests.post(url, data=params, headers=headers)
    if r.status_code != 200:
        return abort(r.status_code)

    root: _Element = etree.HTML(r.text)
    degree: list[_Element] = root.xpath("//select/*")

    return [(_.attrib['value'], _.text) for _ in degree]
