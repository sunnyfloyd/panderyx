from abc import ABC, abstractmethod
from typing import List, Union

import pandas as pd

from panderyx.workflows.tools.models import Tool


class ToolService(ABC):
    def __init__(self, tool: Tool) -> None:
        self.tool = tool

    @abstractmethod
    def run_tool(self, inputs: Union[List[pd.DataFrame], None] = None) -> pd.DataFrame:
        """Returns a DataFrame after data manipulation specific for this tool has finished."""
