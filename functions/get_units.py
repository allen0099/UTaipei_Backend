from .get_semester import get_semester
from .get_year import get_year


def get_units(dept) -> list[dict[str, str]]:
    url: str = "http://shcourse.utaipei.edu.tw/utaipei/ag_pro/ag203.jsp"

    headers: dict[str, str] = {
        "Host": "shcourse.utaipei.edu.tw",
        "Connection": "keep-alive",
        "Content-Type": "application/x-www-form-urlencoded",
    }
    params: dict[str, str] = {
        "yms_yms": f"{get_year()}#{get_semester()}",
        "dgr_id": "%",
        "dpt_id": f"{dept}",
        "unt_id": "%",
        "clyear": "%",
        "class_type": "",
        "sub_name": "",
        "teacher": "",
        "ls_year": f"{get_year()}",
        "ls_sms": f"{get_semester()}",
        "hid_crk": "",  # hidden value
        "ls_years": "0",  # hidden value
        "ls_smss": "0",  # hidden value
    }

    r = requests.post(url, data=params, headers=headers)
    if r.status_code != 200:
        return abort(r.status_code)

    root: _Element = etree.HTML(r.text)
    unit: list[_Element] = root.xpath("//select[@id='unt_id']/*")

    return [{_.text: _.attrib['value']} for _ in unit if _.attrib['value'] != ""]
