from dataclasses import dataclass


@dataclass
class InputUrl:
    type: str = ""
    url: str = ""
    extension: str = ""
