from dataclasses import asdict
import pandas as pd

from django.test import TestCase
from pyfakefs.fake_filesystem_unittest import Patcher

from panderyx.workflows.test.factories import WorkflowFactory
from panderyx.workflows.tools.test.factories import ToolFactory
from panderyx.workflows.tools.dtos.input_tools import InputUrlConfig
from panderyx.workflows.tools.services.input_tools import InputUrlService
from panderyx.test_helpers.data_sets import test_dataset


class TestInputUrlService(TestCase):
    def setUp(self):
        self.workflow = WorkflowFactory.build()
        self.path = "/foo/bar.txt"
        self.contents = test_dataset

    def test_input_url(self):
        with Patcher() as patcher:
            patcher.fs.create_file(self.path, contents=self.contents)
            config = asdict(InputUrlConfig(type="input_url", url=self.path))
            tool = ToolFactory.build(config=config, workflow=self.workflow)
            service = InputUrlService(tool)

            df = pd.read_csv(self.path)
            assert df.equals(service.run_tool({}))
