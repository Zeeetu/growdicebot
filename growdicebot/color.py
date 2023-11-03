from colorama import Style, Fore, init
from enum import Enum


class COL(Enum):
    init()

    R = Fore.RED
    B = Fore.BLUE
    G = Fore.GREEN
    X = Style.RESET_ALL

    def __str__(self) -> str:
        return self.value
