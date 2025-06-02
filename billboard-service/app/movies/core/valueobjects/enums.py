from enum import Enum

class TheaterType(str, Enum):
    TWO_D = '2D'
    THREE_D = '3D'
    IMAX = 'IMAX'
    FOUR_DX = '4DX'
    VIP = 'VIP'

class MovieGenre(str, Enum):
    ACTION = 'action'
    COMEDY = 'comedy'
    DRAMA = 'drama'
    ROMANCE = 'romance'
    THRILLER = 'thriller'
    SCI_FI = 'sci-fi'

class MovieRating(str, Enum):
    G = 'G'
    PG = 'PG'
    PG_13 = 'PG-13'
    R = 'R'
    NC_17 = 'NC-17'
