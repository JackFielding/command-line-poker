from aenum import Enum

class Action(Enum):

    _init_ = "value string"

    CHECK = 1, "CHECK"
    BET = 2, "BET"
    RAISE = 3, "RAISE"
    FOLD = 4, "FOLD"
    CALL = 5, "CALL"
    DO_NOTHING = 6, "DO NOTHING"

    def __str__(self):
        return self.string

    def __repr__(self):
        return str(self)