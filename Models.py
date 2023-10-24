import dataclasses


@dataclasses.dataclass
class SendingConfiguration:
    repeat: str
    address_value_map: dict[str, str | int]
    message_timeout: int
