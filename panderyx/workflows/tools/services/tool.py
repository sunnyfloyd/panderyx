from abc import ABC, abstractmethod
from dataclasses import dataclass
import typing

import pandas as pd

from panderyx.workflows.tools.models import Tool


@dataclass
class ToolServiceException(Exception):
    tool_id: typing.Union[int, None] = None
    message: typing.Union[str, None] = None
    code: typing.Union[str, None] = None

    @property
    def detail(self):
        return {
            "tool_id": self.tool_id,
            "message": self.message,
        }


class ToolService(ABC):
    def __init__(self, tool: Tool) -> None:
        self.tool = tool

    @abstractmethod
    def run_tool(self, inputs: typing.Dict[int, pd.DataFrame]) -> pd.DataFrame:
        """Returns a DataFrame after data manipulation specific for this tool has finished."""
