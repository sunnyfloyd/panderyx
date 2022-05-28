import json
from typing import List, Union

import numpy as np
import pandas as pd

from panderyx.workflows.tools.helpers import DataTypes
from panderyx.workflows.tools.services.tool import ToolService


class DescribeDataService(ToolService):

    data_type_mapping = {
        DataTypes.ALL.value: "all",
        DataTypes.NUMERIC.value: [np.number],
        DataTypes.OBJECT.value: [np.object],
        DataTypes.CATEGORY.value: ["category"],
    }

    def run_tool(self, inputs: Union[List[pd.DataFrame], None] = None) -> pd.DataFrame:
        config = self.tool.config
        data_type = self.data_type_mapping[config["data_type"]]
        df = list(inputs.values())[0]

        return df.describe(include=data_type)
