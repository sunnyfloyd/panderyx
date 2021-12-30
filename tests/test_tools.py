from unittest import TestCase

from workflows import workflow
from tools import tools

import pathlib


class TestInputTool(TestCase):
    def setUp(self) -> None:
        self.workflow = workflow.Workflow()

    def test_csv_url_path_input(self):
        tool = self.workflow.insert_tool("input")
        path = "https://raw.githubusercontent.com/sunnyfloyd/panderyx/main/test_datasets/cov-19_ts_global.csv"
        data = {
            "path": path,
            "extension": "csv",
        }
        self.workflow.set_tool_config(tool_id=tool.id, data=data)
        df = tool.run()

        self.assertEqual(df.shape[0], 280)
        self.assertEqual(df.shape[1], 712)

    def test_csv_file_path_input(self):
        tool = self.workflow.insert_tool("input")
        path = pathlib.Path("test_datasets/cov-19_ts_global.csv")
        data = {
            "path": path,
            "extension": "csv",
        }
        self.workflow.set_tool_config(tool_id=tool.id, data=data)
        df = tool.run()

        self.assertEqual(df.shape[0], 280)
        self.assertEqual(df.shape[1], 712)
