from __future__ import annotations
from typing import Optional, Union
from exceptions import tool_exceptions


class Tool:
    max_number_of_inputs = 1
    # inputs = set()
    # outputs = set()
    # config = {}
    is_root = False

    def __init__(self, id=None) -> None:
        self._id = id
        # self.max_number_of_inputs = 1
        self.inputs = set()
        self.outputs = set()
        self.config = {}
        # self.is_root = False


    def add_input(self, input_id: int) -> None:
        if len(self.inputs) >= self.max_number_of_inputs:
            raise tool_exceptions.TooManyInputs
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

    @property
    def id(self):
        return self._id

    # def __del__(self):
    #     if self.is_root:
    #         raise Exception


class RootTool(Tool):
    max_number_of_inputs = 0
    # config = {}
    is_root = True

    def __init__(self, id=None) -> None:
        super().__init__(id=id)
        # self.max_number_of_inputs = 0
        self.config = {}
        # self.is_root = True


class InputTool(Tool):
    max_number_of_inputs = 0
    # config = {
    #     "path": {"value": "", "is_required": True},
    #     "extension": {"value": "", "is_required": True},
    # }

    def __init__(self, id=None) -> None:
        super().__init__(id=id)
        # self.max_number_of_inputs = 0
        self.config = {
            "path": {"value": "", "is_required": True},
            "extension": {"value": "", "is_required": True},
        }


class GenericTool(Tool):
    max_number_of_inputs = 2
    # config = {}

    def __init__(self, id=None) -> None:
        super().__init__(id=id)
        # self.max_number_of_inputs = 2
        self.config = {}

class LargeGenericTool(GenericTool):
    max_number_of_inputs = 10
