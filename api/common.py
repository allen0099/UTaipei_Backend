import logging
import typing as t
from enum import Enum

from utils import get_year

logger: logging.Logger = logging.getLogger(__name__)


class Grade(str, Enum):
    ALL = "%"
    ZERO = "0"
    ONE = "1"
    TWO = "2"
    THREE = "3"
    FOUR = "4"
    FIVE = "5"
    SIX = "6"


class Degree(str, Enum):
    ALL = "%"
    UNDERGRADUATE = "14"
    MASTER = "16"
    DOCTOR = "17"
    IN_SERVICE_MASTER = "46"
    TEACHER_EDUCATION_CENTER = "71"


class Department(str, Enum):
    ALL = "%"
    TEACHER_EDUCATION_CENTER = "24"
    EXTENSION = "51"
    CITY_ADMINISTRATION = "UZ"
    EDUCATION = "WZ"
    COMMON_SUBJECTS = "XS"
    HUMANITIES_AND_ARTS = "XZ"
    SCIENCE = "YZ"
    PHYSICAL_EDUCATION = "ZZ"


class Unit(str, Enum):
    ALL = "%"
    ELEMENTARY_EDUCATION_PROGRAM = "2410"
    MIDDLE_SPECIAL_EDUCATION_PROGRAM_A = "2421"
    MIDDLE_SPECIAL_EDUCATION_PROGRAM_B = "2422"
    EXTENSION = "2600"
    BALL_SPORTS = "5000"
    TRACK_AND_FIELD = "5100"
    WATER_SPORTS = "5200"
    MARTIAL_ARTS = "5300"
    LEISURE_SPORTS_MANAGEMENT = "5500"
    LEISURE_SPORTS_MANAGEMENT_MASTER = "5510"
    SPORT_HEALTH_SCIENCE_MASTER = "5611"
    DANCE = "5700"
    DANCE_MASTER = "5710"
    SPORT_SCIENCE = "5800"
    SPORT_EDUCATION = "5900"
    SPORT_EQUIPMENT_TECHNOLOGY = "6000"
    MENTAL_AND_PHYSICAL_DISABILITIES_TRANSFER_AND_LEISURE_EDUCATION_MASTER = "6201"
    ATHLETIC_TRAINING = "6400"
    SPORTS_ART = "6600"
    SPORT_HEALTH_SCIENCE = "6700"
    EDUCATION = "7100"
    SPECIAL_EDUCATION = "7200"
    SPECIAL_EDUCATION_MASTER = "7202"
    SPECIAL_EDUCATION_MASTER_LANGUAGE_THERAPY = "7205"
    SPECIAL_EDUCATION_MASTER_SPECIAL_EDUCATION = "7206"
    PRESCHOOL_EDUCATION = "7300"
    PSYCHOLOGY_AND_COUNSELING = "7400"
    LEARNING_AND_MEDIA_DESIGN = "7500"
    EDUCATIONAL_ADMINISTRATION_AND_EVALUATION_MASTER = "7600"
    CHINESE_LANGUAGE_AND_LITERATURE = "7900"
    HISTORY_AND_GEOGRAPHY = "8100"
    MUSIC = "8200"
    VISUAL_ARTS = "8300"
    ENGLISH_TEACHING = "8400"
    SOCIAL_AND_PUBLIC_AFFAIRS = "8500"
    CHINESE_LANGUAGE_TEACHING_MASTER = "8800"
    EARTH_ENVIRONMENT_AND_BIOLOGICAL_RESOURCES = "8900"
    EARTH_ENVIRONMENT_AND_BIOLOGICAL_RESOURCES_MASTER_ENVIRONMENTAL_EDUCATION = "8910"
    APPLIED_PHYSICS_AND_CHEMISTRY_ELECTRONIC_PHYSICS = "9002"
    APPLIED_PHYSICS_AND_CHEMISTRY_APPLIED_CHEMISTRY = "9003"
    APPLIED_PHYSICS_AND_CHEMISTRY_APPLIED_SCIENCE_MASTER = "9004"
    COMPUTER_SCIENCE = "9100"
    MATHEMATICS = "9200"
    PHYSICAL_EDUCATION = "9300"
    CHINESE_LANGUAGE_AND_LITERATURE_MASTER_IN_SERVICE = "9612"
    MUSIC_MASTER_IN_SERVICE = "9634"
    VISUAL_ARTS_MASTER_IN_SERVICE = "9641"
    MATHEMATICS_DATA_SCIENCE_AND_MATHEMATICS_EDUCATION_MASTER = "9668"
    EDUCATIONAL_ADMINISTRATION_AND_EVALUATION_MASTER_IN_SERVICE = "9671"
    PHYSICAL_EDUCATION_MASTER_IN_SERVICE = "9674"
    SOCIAL_AND_PUBLIC_AFFAIRS_MASTER_IN_SERVICE = "9681"
    LEARNING_AND_MEDIA_DESIGN_MASTER_IN_SERVICE = "9689"
    SPECIAL_EDUCATION_SCHOOL_TEACHER_EDUCATION_PROGRAM_NATIONAL_ELEMENTARY_SCHOOL_STAGE_GIFTED = "9705"
    SPECIAL_EDUCATION_SCHOOL_TEACHER_EDUCATION_PROGRAM_NATIONAL_ELEMENTARY_SCHOOL_STAGE_PHYSICAL_AND_MENTAL_DISABILITIES = (
        "9706"
    )
    KINDERGARTEN_TEACHER_EDUCATION_PROGRAM = "9707"
    NATIONAL_ELEMENTARY_SCHOOL_TEACHER_EDUCATION_PROGRAM = "9708"
    NATIONAL_ELEMENTARY_SCHOOL_TEACHER_EDUCATION_PROGRAM_GIFTED_MATHEMATICS_TEACHER_CREDIT_PROGRAM = "9713"
    SPECIAL_EDUCATION_PROGRAM_PRE_SCHOOL_EDUCATION = "9725"
    SPECIAL_EDUCATION_PROGRAM_MIDDLE = "9726"
    DIGITAL_MATHEMATICS_LEARNING_CREDIT_PROGRAM = "9729"
    AUDIO_AND_VIDEO_CREDIT_PROGRAM = "9730"
    ART_ADMINISTRATION_CREDIT_PROGRAM = "9731"
    FINANCIAL_ENGINEERING_CREDIT_PROGRAM = "9735"
    CHILD_DEVELOPMENT_CREDIT_PROGRAM = "9736"
    NATIONAL_ELEMENTARY_SCHOOL_TEACHER_EDUCATION_PROGRAM_COMBINED = "9737"
    MIDDLE_SPECIAL_EDUCATION_PROGRAM_A_NEW = "9738"
    MIDDLE_SPECIAL_EDUCATION_PROGRAM_B_NEW = "9739"
    NATIONAL_ELEMENTARY_SCHOOL_TEACHER_EDUCATION_PROGRAM_TIANMU_NEW = "9741"
    ENGLISH_BUSINESS_CREDIT_PROGRAM = "9743"
    PUBLIC_SERVICE_LAW_CREDIT_PROGRAM = "9745"
    URBAN_DEVELOPMENT = "9747"
    URBAN_INDUSTRY_MANAGEMENT_AND_MARKETING = "9748"
    HEALTH_AND_WELFARE = "9749"
    URBAN_DEVELOPMENT_MASTER = "9751"
    URBAN_INDUSTRY_MANAGEMENT_AND_MARKETING_MASTER = "9752"
    HEALTH_AND_WELFARE_MASTER = "9753"
    MATHEMATICS_DATA_SCIENCE_AND_MATHEMATICS_EDUCATION_MASTER_IN_SERVICE = "9756"
    COMMON_SUBJECTS = "XS00"
    COLLEGE_MAIN_COURSES = "ZZ80"


DEGREE_MAP: dict[str, str] = {
    "%": "所有學制",
    "14": "大學部",
    "16": "碩士班",
    "17": "博士班",
    "46": "在職碩士班",
    "71": "師資培育中心",
}
DEPARTMENT_MAP: dict[str, str] = {
    "%": "所有學院",
    "24": "師資培育中心",
    "51": "進修推廣處",
    "UZ": "市政管理學院",
    "WZ": "教育學院",
    "XS": "校共同科目",
    "XZ": "人文藝術學院",
    "YZ": "理學院",
    "ZZ": "體育學院",
}
UNIT_MAP: dict[str, str] = {
    "2410": "國小教育學程",
    "2421": "中等特殊教育學程(A)",
    "2422": "中等特殊教育學程(B)",
    "2600": "進修推廣處",
    "5000": "球類運動學系",
    "5100": "陸上運動學系",
    "5200": "水上運動學系",
    "5300": "技擊運動學系",
    "5500": "休閒運動管理學系",
    "5510": "休閒運動管理學系碩士班",
    "5611": "運動健康科學系碩士班",
    "5700": "舞蹈學系",
    "5710": "舞蹈學系碩士班",
    "5800": "運動科學研究所",
    "5900": "運動教育研究所",
    "6000": "運動器材科技研究所",
    "6201": "身心障礙者轉銜及休閒教育碩士學位學程班",
    "6400": "競技運動訓練研究所",
    "6600": "運動藝術學系",
    "6700": "運動健康科學系",
    "7100": "教育學系",
    "7200": "特殊教育學系",
    "7202": "特殊教育學系碩士在職專班",
    "7205": "特殊教育學系碩士班語言治療組",
    "7206": "特殊教育學系碩士班特殊教育組",
    "7300": "幼兒教育學系",
    "7400": "心理與諮商學系",
    "7500": "學習與媒材設計學系",
    "7600": "教育行政與評鑑研究所",
    "7900": "中國語文學系",
    "8100": "歷史與地理學系",
    "8200": "音樂學系",
    "8300": "視覺藝術學系",
    "8400": "英語教學系",
    "8500": "社會暨公共事務學系",
    "8800": "華語文教學碩士學位學程",
    "8900": "地球環境暨生物資源學系",
    "8910": "地球環境暨生物資源學系環境教育碩士在職專班",
    "9002": "應用物理暨化學系電子物理組",
    "9003": "應用物理暨化學系應用化學組",
    "9004": "應用物理暨化學系應用科學碩士班",
    "9100": "資訊科學系",
    "9200": "數學系",
    "9300": "體育學系",
    "9612": "中國語文學系碩士在職專班",
    "9634": "音樂學系碩士在職專班",
    "9641": "視覺藝術學系碩士在職專班",
    "9668": "數學系數據科學與數學教育碩士班",
    "9671": "教育行政與評鑑研究所碩士在職專班",
    "9674": "體育學系碩士在職專班",
    "9681": "社會暨公共事務學系碩士在職專班",
    "9689": "學習與媒材設計學系課程與教學碩士學位在職專班",
    "9705": "特殊教育學校(班)師資類科教育學程-國民小學階段-資賦優異類",
    "9706": "特殊教育學校(班)師資類科教育學程-國民小學階段-身心障礙類",
    "9707": "幼稚園師資類科教育學程",
    "9708": "國民小學師資類科教育學程",
    "9713": "國小資優數學教師學分學程",
    "9725": "特教學程-學前教育",
    "9726": "特教學程-中等",
    "9729": "數位數學學習學分學程",
    "9730": "錄音與錄影學分學程",
    "9731": "藝術行政學分學程",
    "9735": "財務工程學分學程",
    "9736": "兒童發展學分學程",
    "9737": "國民小學師資類科教育學程(合併)",
    "9738": "中等特殊教育學程(A)_新制",
    "9739": "中等特殊教育學程(B)_新制",
    "9741": "國小教育學程(天母)_新制",
    "9743": "英語商務學分學程",
    "9745": "公務法律學分學程",
    "9747": "城市發展學系",
    "9748": "都會產業經營與行銷學系",
    "9749": "衛生福利學系",
    "9751": "城市發展學系碩士班",
    "9752": "都會產業經營與行銷學系碩士班",
    "9753": "衛生福利學系碩士班",
    "9756": "數學系數據科學與數學教育碩士在職專班",
    "XS00": "校共同科目(1091起)",
    "ZZ80": "院本部開課(博愛)",
    "%": "所有科系",
}
CLASS_YEAR_MAP: dict[str, str] = {
    "0": "0",
    "1": "1",
    "2": "2",
    "3": "3",
    "4": "4",
    "5": "5",
    "6": "6",
    "%": "所有年級",
}
CLASS_TYPE_MAP: dict[str, str] = {
    "": "(所有課程)",
    "1": "全英語授課(English-taught Courses)",
}
VALIDATE_RULES: dict[str, t.Callable[[t.Any], bool]] = {
    "year": lambda x: 98 <= x <= get_year(),
    "semester": lambda x: x in [1, 2, 3, 4, 5],
    "degree": lambda x: x in DEGREE_MAP.keys(),
    "department": lambda x: x in DEPARTMENT_MAP.keys(),
    "unit": lambda x: x in UNIT_MAP.keys(),
    "class_year": lambda x: x in CLASS_YEAR_MAP.keys(),
    "class_type": lambda x: x in CLASS_TYPE_MAP.keys(),
    "sub_name": lambda x: isinstance(x, str),
    "teacher": lambda x: isinstance(x, str),
}
