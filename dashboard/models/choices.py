from enum import Enum


class ChoiceEnum(Enum):

    @classmethod
    def list_values(cls):
        return [tag.value for tag in cls]


class AppTypeChoices(ChoiceEnum):
    WEB = "Web"
    MOBILE = "Mobile"


class AppFrameWorkChoices(ChoiceEnum):
    DJANGO = "Django"
    REACT_NATIVE = "React Native"


class PlanPriceChoices(ChoiceEnum):
    FREE = "$0"
    STANDARD = "$10"
    PRO = "$25"


class PlanNameChoices(ChoiceEnum):
    FREE = "Free"
    STANDARD = "Standard"
    PRO = "Pro"
