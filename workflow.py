from __future__ import annotations
from typing import Optional


class Tool:
    is_root = False
    max_number_of_parents = 1

    def __init__(self, parents: Optional[list[Tool]] = None) -> None:
        self.parents = parents

    @property
    def number_of_parents(self) -> int:
        return len(self.parents) if self.parents is not None else 0


class RootTool(Tool):
    is_root = True
    max_number_of_parents = 0

    def __init__(self, parents: Optional[list[Tool]] = None) -> None:
        super().__init__(parents=parents)


class InputTool(Tool):
    max_number_of_parents = 1

    def __init__(self) -> None:
        super().__init__(parents=parents)


class Workflow:
    def __init__(self) -> None:
        self._root = RootTool(parents=None)
        self.workflow_custom_contants = {}

    def insert_tool(self, tool_option):
        ...

    def add_tool_parent(self, tool: Tool, parent: Tool = None) -> None:
        if tool.number_of_parents < tool.max_number_of_parents:
            tool.parents.append(parent)
        elif parent is None:
            tool.parents.append(self._root)
        else:
            raise Exception

    def remove_tool_parent(self, tool: Tool, parent: Tool) -> None:
        if tool.is_root:
            raise Exception
        if parent not in tool.parents:
            raise Exception
        tool.parents.pop(parent)

    def remove_tool(self, tool: Tool) -> None:
        if tool.is_root:
            raise Exception
        del tool


w = Workflow()
print(w._root.is_root)

# each tool should have a position defined by a integer
# all tools stored in the workflow in dict
# parents should converted to inputs and outputs should be added (?)
# workflow or somewhere in the code should be a dict with names indicating tool and value being specific tool class
