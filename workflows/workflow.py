from __future__ import annotations
from typing import Optional, Union
import tools


class Workflow:
    TOOL_CHOICES = {
        "root": tools.RootTool,
    }

    def __init__(self) -> None:
        self._root = tools.RootTool()
        self._tools = {0: self._root}
        self._used_ids = {0}

    def insert_tool(
        self,
        tool_choice: str,
        input_ids: Optional[Union[list[int], int]],
        output_ids: Optional[Union[list[int], int]],
    ) -> int:
        try:
            tool = self.TOOL_CHOICES[tool_choice]()
        except KeyError:
            raise Exception

        if input_ids is not None:
            input_ids = self._clean_tool_ids(input_ids)
            for input_id in input_ids:
                tool.add_input(input_id)

        if output_ids is not None:
            output_ids = self._clean_tool_ids(output_ids)
            for output_id in output_ids:
                tool.add_output(output_id)

        next_id = self._get_next_tool_id()
        self._tools[next_id] = tool
        self._add_tool_id(next_id)

        return next_id

    def remove_tool(self, tool_ids: Union[list[int], int]) -> None:
        tool_ids = self._clean_input_ids(tool_ids)

        for tool_id in tool_ids:
            for tool in self._tools[tool_id]:
                for output_id in tool.outputs:
                    self._tools[output_id].remove_input(
                        output_id
                    )  # remove tool from linked tools' inputs
                for input_id in tool.inputs:
                    self._tools[input_id].remove_output(
                        input_id
                    )  # remove tool from linked tools' outputs

            del self._tools[tool_id]

    def add_tool_input(self, tool_id: int, input_ids: Union[list[int], int]) -> None:
        tool = self._get_tool_by_id(tool_id)
        input_ids = self._clean_tool_ids(input_ids)

        for input_id in input_ids:
            tool.add_input(input_id)
            self._tools[input_id].add_output(tool_id)

    def remove_tool_input(self, tool_id: int, input_ids: Union[list[int], int]) -> None:
        tool = self._get_tool_by_id(tool_id)
        input_ids = self._clean_input_ids(input_ids)

        for input_id in input_ids:
            tool.remove_input(input_id)
            self._tools[input_id].remove_output(tool_id)

    def _get_tool_by_id(self, tool_id: int) -> tools.Tool:
        try:
            tool = self._tools[tool_id]
        except KeyError:
            raise Exception
        return tool

    def _clean_tool_ids(self, input_ids: Union[list[int], int]) -> list[int]:
        input_ids = input_ids if isinstance(input_ids, list) else [input_ids]
        if any(input_id not in self._tools for input_id in input_ids):
            raise Exception

        return input_ids

    def _add_tool_id(self, tool_id: int) -> None:
        self._used_ids.add(tool_id)

    def _get_next_tool_id(self) -> int:
        return max(self._used_ids) + 1

    def _build_flow(self) -> None:
        ...

    def __len__(self) -> int:
        return len(self._tools) - 1
