from dataclasses import dataclass
from typing import Dict

import numpy as np
import pandas as pd

from panderyx.workflows.tools.helpers import DataTypes
from panderyx.workflows.tools.services.tool import ToolService, ToolServiceException

@dataclass
class DescribeDataException(ToolServiceException):
    message: str = (
        "Describe Tool could not process provided data. "
        "Please make sure that 'describe type' is suitable for your type of data."
    )
    code: str = "describe_error"


class DescribeDataService(ToolService):
    data_type_mapping = {
        DataTypes.ALL.value: "all",
        DataTypes.NUMERIC.value: [np.number],
        DataTypes.OBJECT.value: [np.object],
        DataTypes.CATEGORY.value: ["category"],
    }

    def run_tool(self, inputs: Dict[int, pd.DataFrame]) -> pd.DataFrame:
        config = self.tool.config
        data_type = self.data_type_mapping[config["data_type"]]
        # getting the only input DataFrame
        df = list(inputs.values())[0]

        try:
            return df.describe(include=data_type)
        except ValueError:
            raise DescribeDataException(tool_id=self.tool.id)
