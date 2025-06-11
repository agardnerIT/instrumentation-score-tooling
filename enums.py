from enum import StrEnum, IntEnum

class Score(IntEnum):
    LOWEST = 10
    HIGHEST = 100
class Target(StrEnum):
    LOG = "LOG"
    METRIC = "MET"
    RESOURCE = "RES"
    SDK = "SDK"
    SPAN = "SPA"

class Impact(StrEnum):
    CRITICAL = "Critical"
    VERY_IMPORTANT = "Very Important"
    IMPORTANT = "Important"
    NORMAL = "Normal"
    LOW = "Low"

class Type(StrEnum):
    POSITIVE = "Positive"
    NEGATIVE = "Negative"