from __future__ import annotations
from typing import Optional, Tuple, Union

from pydantic import ValidationError

from exceptions import tool_exceptions
from workflows import workflow_constants
from configs import configs
from configs import config_exceptions


class Tool:
    """A class that represents a single tool in the workflow.

    Tool class provides attributes that describe tool and define tool's relation
    to other tools within the workflow.

    Tool class methods allow for tool configuration and provide means to change
    tool's relations with other tools in the workflow.

    Attributes:
        max_number_of_inputs (int): defines the maximum number of tool's inputs.
        is_root (bool): indicates whether a tool is a root tool.
        _config_class (configs.Config): determines class in which configuration
            fields reside together with their validation methods.
    """    
    max_number_of_inputs = 1
    is_root = False
    _config_class = None

    def __init__(self, id: int) -> None:
        """Initializes Tool class based on the provided ID.

        Args:
            id (int): tool ID assigned in the Workflow class.
        """
        self._id = id
        self._inputs = set()
        self._outputs = set()
        self._config = None
        self._x = None
        self._y = None
        self.errors = {}

    def add_input(self, input_id: int) -> None:
        """Adds tool ID to the inputs set.

        New input will be added if addition would not exceed number of maximum
        possible inputs defined in `max_number_of_inputs` class attribute.

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

    def clean_errors(self) -> None:
        """Cleans errors from the tool's instance."""
        self.errors = {}

    @property
    def id(self) -> int:
        """The tool ID."""
        return self._id

    @property
    def inputs(self) -> set:
        """The tool inputs."""
        return self._inputs

    @property
    def outputs(self) -> set:
        """The tool outputs."""
        return self._outputs

    @property
    def number_of_inputs(self) -> int:
        """Number of elements in the tool's inputs."""
        return len(self._inputs)

    @property
    def number_of_outputs(self) -> int:
        """Number of elements in the tool's outputs."""
        return len(self._outputs)

    @property
    def coordinates(self) -> tuple:
        """(x, y) coordinates of the tool."""
        return (self._x, self._y)

    @coordinates.setter
    def coordinates(self, coordinates: tuple[int, int]) -> None:
        """Sets (x, y) coordinates of the tool.

        Args:
            coordinates (tuple[int, int]): tuple of (x, y) coordinates.

        Raises:
            TypeError: indicates that passed value(s) for `coordinates`
                are not ints and/or cannot be casted into integers.
            ValueError: indicates that at least one of the provided coordinates
                falls out of valid range.
        """
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
        """The tool config."""
        return self._config

    @config.setter
    def config(self, data: dict):
        """Sets `_config` to an instance of `_config_class` initialized with passed data.

        Args:
            data (dict): config dict defining tool's configuration.

        Raises:
            config_exceptions.ConfigClassIsNotDefined: indicates that for given
                tool config class has not been defined.
        """
        if self._config_class is None:
            raise config_exceptions.ConfigClassIsNotDefined
        try:
            self._config = self._config_class(**data)
        except ValidationError as e:
            self.errors["config"] = e.json()


class RootTool(Tool):
    max_number_of_inputs = 0
    is_root = True

    def __init__(self, id: int) -> None:
        super().__init__(id=id)


class InputTool(Tool):
    max_number_of_inputs = 0
    _config_class = configs.InputConfig

    def __init__(self, id: int) -> None:
        super().__init__(id=id)


class GenericTool(Tool):
    max_number_of_inputs = 2

    def __init__(self, id: int) -> None:
        super().__init__(id=id)


class LargeGenericTool(GenericTool):
    max_number_of_inputs = 10
