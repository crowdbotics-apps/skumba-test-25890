from enum import Enum


class AppTypeChoices(Enum):
    WEB = "Web"
    MOBILE = "Mobile"


class AppFrameWorkChoices(Enum):
    DJANGO = "Django"
    REACT_NATIVE = "React Native"


class PlanPriceChoices(Enum):
    FREE = "$0"
    STANDARD = "$10"
    PRO = "$25"
