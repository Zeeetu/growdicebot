from colored import fore_rgb as rgb, Style
from enum import Enum


class COL(Enum):
    R = rgb(254, 0, 0)
    G = rgb(34, 219, 0)
    B = rgb(0, 51, 191)
    Y = rgb(219, 165, 11)
    C = rgb(144, 221, 231)
    X = Style.reset

    def __str__(self) -> str:
        return self.value


class RLT(Enum):
    RED = 1
    GREEN = 2
    BLACK = 3
