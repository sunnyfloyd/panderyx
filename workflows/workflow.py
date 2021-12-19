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
        """Inserts a new tool to the current workflow.

        Args:
            tool_choice (str): determines what tool is created (based on the available choices defined within the
                Workflow class).
            input_ids (list[int], int]): starting input or inputs for the tool identified by their IDs.
                Defaults to None.
            output_ids (list[int], int): starting output or outputs for the tool identified by their IDs.
                Defaults to None.
            coordinates (tuple[int, int]): coordinates for the tool on canvas. Defaults to None.

        Raises:
            workflow_exceptions.ToolNotAvailable: indicates that provided string does not refer to an available tool
                from the Workflow class.

        Returns:
            tools.Tool: instance of a Tool's class.
        """
        try:
            tool_class = self.TOOL_CHOICES[tool_choice]
        except KeyError:
            raise workflow_exceptions.ToolNotAvailable

        next_id = self._get_next_tool_id()
        tool = tool_class(id=next_id)

        self._tools[next_id] = tool
        self._add_tool_id(next_id)

        if input_ids is not None:
            self.add_tool_input(tool_id=tool.id, input_ids=input_ids)

        if output_ids is not None:
            output_ids = self._clean_tool_ids(output_ids)
            for output_id in output_ids:
                self.add_tool_input(tool_id=output_id, input_ids=tool.id)

        if coordinates is not None:
            self.set_tool_coordinates(tool_id=tool.id, coordinates=coordinates)

        return tool

    def remove_tool(self, tool_ids: Union[list[int], int]) -> None:
        """Removes existing tool from the current workflow and updates inputs and outputs of the linked tool instances.

        Args:
            tool_ids (list[int], int): tool ID or IDs that ought to be removed.

        Raises:
            workflow_exceptions.RootCannotBeDeleted: indicates that selected tool for removal is a root which
                cannot be deleted.
        """
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
        """Adds new input(s) for the tool existing in the current workflow.

        Args:
            tool_id (int): tool ID to which input(s) should be added.
            input_ids (list[int], int]): input(s) to be added to the tool identified by their IDs.

        Returns:
            tools.Tool: instance of a Tool's class.
        """
        tool = self._get_tool_by_id(tool_id)
        input_ids = self._clean_tool_ids(input_ids)

        for input_id in input_ids:
            tool.add_input(input_id)
            self._tools[input_id].add_output(tool_id)

        return tool

    def remove_tool_input(
        self, tool_id: int, input_ids: Union[list[int], int]
    ) -> tools.Tool:
        """Removes an input or inputs from the tool existing in the current workflow.

        Args:
            tool_id (int): tool ID from which input(s) should be removed.
            input_ids (list[int], int]): input(s) to be removed from the tool identified by their IDs.

        Returns:
            tools.Tool: instance of a Tool's class.
        """
        tool = self._get_tool_by_id(tool_id)
        input_ids = self._clean_tool_ids(input_ids)

        for input_id in input_ids:
            tool.remove_input(input_id)
            self._tools[input_id].remove_output(tool_id)

        return tool

    def set_tool_config(self, tool_id: int, config: dict) -> tools.Tool:
        NotImplementedError

    def set_tool_coordinates(
        self, tool_id: int, coordinates: Optional[tuple[int, int]] = None
    ) -> tools.Tool:
        """Sets coordinates for the tool existing in the current workflow. If no coordinates are passed to this method
        default coordinates will be calculated using _get_default_coordinates() internal method.

        Args:
            tool_id (int): tool ID for which coordinates are to be set.
            coordinates (tuple[int, int]): tuple of X, Y coordinates. Defaults to None.

        Returns:
            tools.Tool: instance of a Tool's class.
        """
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
        """Returns an instance of a Tool class selected by its ID from the current workflow.

        Args:
            tool_id (int): tool ID.

        Raises:
            workflow_exceptions.ToolDoesNotExist: indicates that for provided ID there is no tool in this workflow.

        Returns:
            tools.Tool: instance of a Tool's class.
        """
        try:
            tool = self._tools[tool_id]
        except KeyError:
            raise workflow_exceptions.ToolDoesNotExist
        return tool

    def _clean_tool_ids(self, tool_ids: Union[list[int], int]) -> list[int]:
        """Checks whether passed tool ID(s) exist in the current workflow and returns the list of tool IDs.
        If at least one of the provided tool IDs is not found it raises an exception.

        Args:
            tool_ids (list[int], int): tool ID(s) to be cleaned.

        Raises:
            workflow_exceptions.ToolDoesNotExist: indicates that at least one of the provided tool IDs is not present
                in the current workflow.

        Returns:
            list[int]: list of checked tool IDs.
        """
        cleaned_tool_ids = (
            list(set(tool_ids)) if isinstance(tool_ids, list) else [tool_ids]
        )
        if any(tool_id not in self._tools for tool_id in cleaned_tool_ids):
            raise workflow_exceptions.ToolDoesNotExist

        return cleaned_tool_ids

    def _add_tool_id(self, tool_id: int) -> None:
        """Add an ID to the used ID pool.

        Args:
            tool_id (int): ID to be added to the used ID pool.
        """
        self._used_ids.add(tool_id)

    def _get_next_tool_id(self) -> int:
        """Returns a next available ID to be used for a tool instance.

        Returns:
            int: next available tool ID.
        """
        return max(self._used_ids) + 1

    def _build_flow(self) -> None:
        ...

    def __len__(self) -> int:
        return len(self._tools) - 1
