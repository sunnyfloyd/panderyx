from __future__ import annotations
from typing import Optional, Union


class Tool:
    max_number_of_inputs = 1
    inputs = {}
    outputs = {}
    config = None
    config_options = {}

    def add_input(self, input_id: int) -> None:
        self.inputs.add(input_id)

    def remove_input(self, input_id: int) -> None:
        try:
            self.inputs.remove(input_id)
        except KeyError:
            raise Exception

    def add_output(self, output_id: int) -> None:
        self.outputs.add(output_id)

    def remove_output(self, output_id: int) -> None:
        try:
            self.outputs.remove(output_id)
        except KeyError:
            raise Exception

    def __del__(self):
        ...


class RootTool(Tool):
    max_number_of_inputs = 0
    config_options = {}


class InputTool(Tool):
    max_number_of_inputs = 0
    config_options = {
        "path": {"value": "", "is_required": True},
        "extension": {"value": "", "is_required": True},
    }
