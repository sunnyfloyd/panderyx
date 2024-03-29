from typing import Dict

import numpy as np
import pandas as pd

from panderyx.workflows.exceptions import MissingToolInput, ToolServiceException
from panderyx.workflows.tools.helpers import DataTypes
from panderyx.workflows.tools.services.tool import ToolService


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
        try:
            df = list(inputs.values())[0]
        except IndexError:
            raise MissingToolInput(tool_id=self.tool.id)

        try:
            return df.describe(include=data_type)
        except ValueError:
            raise ToolServiceException(
                tool_id=self.tool.id,
                message=(
                    "Describe Tool could not process provided data. "
                    "Please make sure that 'describe type' is suitable for your type of data."
                ),
                code="describe_error",
            )
