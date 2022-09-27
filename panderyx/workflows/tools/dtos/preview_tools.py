from dataclasses import dataclass


@dataclass
class DescribeData:
    type: str = "describe_data"
    max_number_of_inputs: int = 1
    data_type: int = 1
