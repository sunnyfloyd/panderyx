from __future__ import annotations
from typing import Optional, Union
from tools import tools
from exceptions import workflow_exceptions


class Workflow:
    TOOL_CHOICES = {
        "generic": tools.GenericTool,
        "large_generic": tools.LargeGenericTool,
        "input": tools.InputTool,
    }

    def __init__(self) -> None:
        self._root = tools.RootTool(id=0)
        self._tools = {0: self._root}
        self._used_ids = {0}

    def insert_tool(
        self,
        tool_choice: str,
        input_ids: Optional[Union[list[int], int]] = None,
        output_ids: Optional[Union[list[int], int]] = None,
        coordinates: Optional[tuple[int, int]] = None,
    ) -> tools.Tool:
        try:
            tool_class = self.TOOL_CHOICES[tool_choice]
            next_id = self._get_next_tool_id()
            tool = tool_class(id=next_id)
        except KeyError:
            raise workflow_exceptions.ToolNotAvailable

        self._tools[next_id] = tool
        self._add_tool_id(next_id)

        if input_ids is not None:
            self.add_tool_input(tool_id=tool.id, input_ids=input_ids)

        if output_ids is not None:
            output_ids = self._clean_tool_ids(output_ids)
            for output_id in output_ids:
                self.add_tool_input(tool_id=output_id, input_ids=tool.id)

        if coordinates is not None:
            self.set_tool_coordinates(coordinates)

        return tool

    def remove_tool(self, tool_ids: Union[list[int], int]) -> None:
        tool_ids = self._clean_tool_ids(tool_ids)

        for tool_id in tool_ids:
            tool = self._get_tool_by_id(tool_id)
            if tool.is_root:
                raise workflow_exceptions.RootCannotBeDeleted

            # remove tool from linked tools' inputs
            tool_outputs = tool.outputs
            for output_id in tool_outputs:
                self.remove_tool_input(tool_id=output_id, input_ids=tool.id)

            # remove tool from linked tools' outputs
            tool_inputs = tool.inputs
            for input_id in tool_inputs:
                self.remove_tool_input(tool_id=tool.id, input_ids=input_id)

            del self._tools[tool_id]

    def add_tool_input(
        self, tool_id: int, input_ids: Union[list[int], int]
    ) -> tools.Tool:
        tool = self._get_tool_by_id(tool_id)
        input_ids = self._clean_tool_ids(input_ids)

        for input_id in input_ids:
            tool.add_input(input_id)
            self._tools[input_id].add_output(tool_id)

        return tool

    def remove_tool_input(
        self, tool_id: int, input_ids: Union[list[int], int]
    ) -> tools.Tool:
        tool = self._get_tool_by_id(tool_id)
        input_ids = self._clean_tool_ids(input_ids)

        for input_id in input_ids:
            tool.remove_input(input_id)
            self._tools[input_id].remove_output(tool_id)

        return tool

    def edit_tool_config(self, tool_id: int, config: dict) -> tools.Tool:
        NotImplementedError

    def set_tool_coordinates(
        self, tool_id: int, coordinates: Optional[tuple[int, int]] = None
    ) -> tools.Tool:
        # I need to decide where to fit a check if coordinates will fit canvas
        tool = self._get_tool_by_id(tool_id)
        coordinates = (
            coordinates if coordinates is not None else self._get_default_coordinates()
        )
        tool.coordinates = coordinates

        return tool

    def _get_default_coordinates(self) -> tuple[int, int]:
        # might require more sophisticated logic in the future
        return (0, 0)

    def _get_tool_by_id(self, tool_id: int) -> tools.Tool:
        try:
            tool = self._tools[tool_id]
        except KeyError:
            raise workflow_exceptions.ToolDoesNotExist
        return tool

    def _clean_tool_ids(self, input_ids: Union[list[int], int]) -> list[int]:
        input_ids = list(set(input_ids)) if isinstance(input_ids, list) else [input_ids]
        if any(input_id not in self._tools for input_id in input_ids):
            raise workflow_exceptions.ToolDoesNotExist

        return input_ids

    def _add_tool_id(self, tool_id: int) -> None:
        self._used_ids.add(tool_id)

    def _get_next_tool_id(self) -> int:
        return max(self._used_ids) + 1

    def _build_flow(self) -> None:
        ...

    def __len__(self) -> int:
        return len(self._tools) - 1
