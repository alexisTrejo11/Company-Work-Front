from enum import Enum

class TheaterType(str, Enum):
    TWO_D = '2D'
    THREE_D = '3D'
    IMAX = 'IMAX'
    FOUR_DX = '4DX'
    VIP = 'V'

