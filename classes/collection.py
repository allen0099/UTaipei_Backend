import re
from collections import Iterator

from lxml.etree import _Element


class Collection:
    def __init__(self, cols: Iterator[_Element]):
        def get_text() -> str:
            text: str = next(cols).text
            if text is not None:
                return text.replace('\xa0', '').replace('\u3000', '')
            else:
                return ""

        self.class_name = get_text()
        self.course_code = get_text()
        self.category = get_text()
        self.chinese_name = get_text()
        self.english_name = get_text()
        self.credit = get_text()
        self.full_half = get_text()
        self.req_select = get_text()
        self.lecturing_hours = get_text()

        people_counts = get_text().split('/')
        self.enrolled_max = people_counts[0]
        self.enrolled_min = people_counts[1]
        self.enrolled_current = people_counts[2]

        self.campus = get_text()

        tmp = get_text()
        reg = re.findall(r'(?P<teacher>.*)\((?P<day>(?<=\().(?=\)))\)(?P<time>\d{1,3}-\d{1,3})', tmp)

        if reg:
            self.teacher = reg[0][0]
            self.day = reg[0][1]
            _split = reg[0][2].split('-', maxsplit=1)
            self.time = [_ for _ in range(int(_split[0]), int(_split[1]) + 1)]
        else:
            self.teacher = tmp

        self.mixed_class = get_text()
        self.syllabus = re.findall(r"(?<=go_next\(').+(?='\))", next(cols).attrib['onclick'])[0]

        tmp = next(cols)

        self.notes = tmp.text

        if len(tmp.getchildren()) > 1:
            self.limit = True
        else:
            self.limit = False

    def to_dict(self) -> dict:
        ret: dict = {}
        for _ in [_ for _ in dir(self) if
                  not _.startswith('_') and
                  not hasattr(getattr(self, _), '__call__')]:
            ret[_] = getattr(self, _)
        return ret
