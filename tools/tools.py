from __future__ import annotations
from typing import Optional, Tuple, Union
from pydantic import ValidationError
from exceptions import tool_exceptions
from workflows import workflow_constants
from configs import configs


class Tool:
    max_number_of_inputs = 1
    is_root = False
    config_class = None

    def __init__(self, id=None) -> None:
        self._id = id
        self._inputs = set()
        self._outputs = set()
        self._config = None
        self._x = None
        self._y = None
        self.errors = {}

    def add_input(self, input_id: int) -> None:
        """Adds tool ID to the inputs set if addition will not exceed number of maximum possible inputs
        (max_number_of_inputs).

        Args:
            input_id (int): tool ID to be added to the inputs set.
        """
        if self.number_of_inputs >= self.max_number_of_inputs:
            self.errors.setdefault("input", []).append(
                f"Skipped input addition for {input_id} - max number of inputs ({self.max_number_of_inputs}) reached."
            )
        else:
            self._inputs.add(input_id)

    def remove_input(self, input_id: int) -> None:
        """Removes tool ID from the inputs set.

        Args:
            input_id (int): tool ID to be removed from the inputs set.
        """
        try:
            self._inputs.remove(input_id)
        except KeyError:
            pass
            # raise tool_exceptions.InputDoesNotExist

    def add_output(self, output_id: int) -> None:
        """Adds tool ID to the outputs set.

        Args:
            output_id (int): tool ID to be added to the outputs set.
        """
        self._outputs.add(output_id)

    def remove_output(self, output_id: int) -> None:
        """Removes tool ID from the outputs set.

        Args:
            output_id (int): tool ID to be removed from the outputs set.
        """
        try:
            self._outputs.remove(output_id)
        except KeyError:
            pass
            # raise tool_exceptions.OutputDoesNotExist

    def clean_errors(self):
        """Cleans errors from the tool."""
        self.errors = {}

    @property
    def id(self) -> int:
        return self._id

    @property
    def inputs(self) -> list:
        return self._inputs

    @property
    def outputs(self) -> list:
        return self._outputs

    @property
    def number_of_inputs(self) -> int:
        return len(self._inputs)

    @property
    def number_of_outputs(self) -> int:
        return len(self._outputs)

    @property
    def coordinates(self) -> Tuple[int, int]:
        return (self._x, self._y)

    @coordinates.setter
    def coordinates(self, coordinates: tuple[int, int]) -> None:
        try:
            x, y = map(int, coordinates)
        except ValueError:
            raise TypeError("Coordinates need to be a tuple of integers.")

        if any(
            [
                x < 0,
                x > workflow_constants.MAX_CANVAS_SIZE,
                y < 0,
                y > workflow_constants.MAX_CANVAS_SIZE,
            ]
        ):
            raise ValueError(
                f"Both coordinates must fall in the [0, {workflow_constants.MAX_CANVAS_SIZE}] range."
            )

        self._x, self._y = x, y

    @property
    def config(self):
        return self._config

    @config.setter
    def config(self, data):
        try:
            self._config = self.config_class(**data)
        except ValidationError as e:
            self.errors["config"] = e.json()


class RootTool(Tool):
    max_number_of_inputs = 0
    is_root = True

    def __init__(self, id=None) -> None:
        super().__init__(id=id)


class InputTool(Tool):
    max_number_of_inputs = 0
    config_class = configs.InputConfig

    def __init__(self, id=None) -> None:
        super().__init__(id=id)


class GenericTool(Tool):
    max_number_of_inputs = 2

    def __init__(self, id=None) -> None:
        super().__init__(id=id)


class LargeGenericTool(GenericTool):
    max_number_of_inputs = 10
