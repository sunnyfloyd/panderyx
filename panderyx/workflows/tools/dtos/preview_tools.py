from dataclasses import dataclass

from panderyx.workflows.tools.dtos.tool import ToolConfig

@dataclass
class DescribeDataConfig(ToolConfig):
    type: str = "describe_data"
    max_number_of_inputs: int = 1
    data_type: int = 1
