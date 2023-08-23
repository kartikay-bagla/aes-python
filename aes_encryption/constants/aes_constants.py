from dataclasses import dataclass
from enum import Enum


@dataclass
class AES_Attributes:
    key_length: int
    num_round_keys: int


class AES_Type(Enum):
    AES_128 = AES_Attributes(4, 11)
    AES_192 = AES_Attributes(6, 13)
    AES_256 = AES_Attributes(8, 15)
