from dataclasses import dataclass


# TODO Make sure to use @dataclass(slots=True) after upgrading to Python 3.10
@dataclass
class InputUrl:
    type: str = "input_url"
    max_number_of_inputs: int = 0
    url: str = ""
    extension: str = ""
    separator: str = ""
