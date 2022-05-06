from dataclasses import dataclass


@dataclass
class InputUrl:
    type: str = "input_url"
    url: str = ""
    extension: str = ""
