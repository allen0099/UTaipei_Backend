import re
from collections import Iterator
from re import Match

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
        # todo: close classes
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

        if '/' in tmp:
            tmp = tmp.split('/')
            self.teachers = [tmp[0]]
            self.times = [{
                "day": tmp[1],
                "time": [""],
            }]
        else:
            reg: list[Match] = [_ for _ in re.finditer(
                r'(?P<teacher>.*?) ?\(?(?P<day>(?<=\().(?=\))|時間未定)\)?(?P<time>\d{1,3}(?:-\d{1,3})?)?(?:\((?P<location>.*?)\))?',
                tmp)]

            if reg:
                self.teachers = [
                    _.group('teacher') for _ in reg if _.group('teacher') != ''
                ]

                self.times = [{
                    "day": _.group('day'),
                    "time": list(
                        range(*map(lambda t: int(t[1]) + t[0], enumerate(_.group('time').split('-', maxsplit=1))))) \
                        if _.group('time') is not None and '-' in _.group('time') else [] \
                        if _.group('time') is None else [_.group('time')],
                } for _ in reg]

                # remove duplicate dict from https://stackoverflow.com/a/9428041
                self.times = [i for n, i in enumerate(self.times) if i not in self.times[n + 1:]]
            else:
                self.teachers = tmp
                self.times = [{
                    "day": "",
                    "time": [""],
                }]

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
