from dataclasses import dataclass

# TODO Make sure to use @dataclass(slots=True) after upgrading to Python 3.10
@dataclass
class ToolConfig:
    type: str = ""
    max_number_of_inputs: int = 0
