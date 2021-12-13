from __future__ import annotations
from typing import Optional, Union
from exceptions import tool_exceptions
from workflows import workflow_constants


class Tool:
    max_number_of_inputs = 1
    is_root = False

    def __init__(self, id=None) -> None:
        self._id = id
        self._inputs = set()
        self._outputs = set()
        self.config = {}
        self._x = None
        self._y = None

    def add_input(self, input_id: int) -> None:
        if self.number_of_inputs >= self.max_number_of_inputs:
            raise tool_exceptions.TooManyInputs
        self._inputs.add(input_id)

    def remove_input(self, input_id: int) -> None:
        try:
            self._inputs.remove(input_id)
        except KeyError:
            raise tool_exceptions.InputDoesNotExist

    def add_output(self, output_id: int) -> None:
        self._outputs.add(output_id)

    def remove_output(self, output_id: int) -> None:
        try:
            self._outputs.remove(output_id)
        except KeyError:
            raise tool_exceptions.OutputDoesNotExist

    @property
    def id(self):
        return self._id

    @property
    def inputs(self):
        return self._inputs

    @property
    def outputs(self):
        return self._outputs

    @property
    def number_of_inputs(self):
        return len(self._inputs)

    @property
    def number_of_outputs(self):
        return len(self._outputs)

    @property
    def coordinates(self):
        return (self._x, self._y)

    @coordinates.setter
    def coordinates(self, coordinates: tuple[int, int]):
        if any(not isinstance(coordinate, int) for coordinate in coordinates):
            raise TypeError("Coordinates need to be a tuple of integers.")

        x, y = coordinates

        if any[x < 0, x > workflow_constants.MAX_CANVAS_SIZE, y < 0, y > workflow_constants.MAX_CANVAS_SIZE]:
            raise ValueError(f"Both coordinates must fall in the [0, {workflow_constants.MAX_CANVAS_SIZE}] range.")

        self._x, self._y = x, y


class RootTool(Tool):
    max_number_of_inputs = 0
    is_root = True

    def __init__(self, id=None) -> None:
        super().__init__(id=id)
        self.config = {}


class InputTool(Tool):
    max_number_of_inputs = 0

    def __init__(self, id=None) -> None:
        super().__init__(id=id)
        self.config = {
            "path": {"value": "", "is_required": True},
            "extension": {"value": "", "is_required": True},
        }


class GenericTool(Tool):
    max_number_of_inputs = 2

    def __init__(self, id=None) -> None:
        super().__init__(id=id)
        self.config = {}


class LargeGenericTool(GenericTool):
    max_number_of_inputs = 10
