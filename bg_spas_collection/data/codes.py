import dataclasses


@dataclasses.dataclass
class Codes:
    pin_code: list[str]
    sms_code: list[str]
