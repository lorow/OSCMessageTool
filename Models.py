import dataclasses
from typing import List


@dataclasses.dataclass
class SendingConfiguration:
    repeat: str
    address_value_map: List[List[str | int]]
    message_timeout: int
