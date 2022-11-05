from dataclasses import dataclass

from panderyx.workflows.tools.dtos.tool import ToolConfig

# TODO Make sure to use @dataclass(slots=True) after upgrading to Python 3.10
@dataclass
class InputUrlConfig(ToolConfig):
    type: str = "input_url"
    max_number_of_inputs: int = 0
    url: str = ""
    extension: str = ""
    separator: str = ""
