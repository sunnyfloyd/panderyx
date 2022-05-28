from typing import List, Union

import pandas as pd

from panderyx.workflows.tools.services.tool import ToolService


class InputUrlService(ToolService):
    def run_tool(self, inputs: Union[List[pd.DataFrame], None] = None) -> pd.DataFrame:
        config = self.tool.config
        df = pd.read_csv(config["url"])

        return df
