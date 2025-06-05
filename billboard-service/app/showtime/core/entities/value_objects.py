from enum import Enum
from pydantic import BaseModel

class ShowtimeType(str, Enum):
    TWO_D = 'TRADITIONAL_2D'
    THREE_3D = 'TRADITIONAL_3D'
    IMAX_2D = 'IMAX_2D'
    IMAX_3D = 'IMAX_3D'
    FOUR_D = '4D'
    FOUR_DX = '4DX'
    VIP_2D = 'VIP_2D'
    VIP_3D = 'VIP_3D'


class ShowtimeLanguage(str, Enum):
    ORIGINAL_ENGLISH = "ORIGINAL_ENGLISH"
    ORIGINAL_SPANISH = "ORIGINAL_SPANISH"
    ORIGINAL_JAPANESE = "ORIGINAL_JAPANESE"
    ORIGINAL_KOREAN = "ORIGINAL_KOREAN"

    DUBBED_ENGLISH = "DUBBED_ENGLISH"


class Seats(BaseModel):
    seat_id: str
    is_taken: bool = False