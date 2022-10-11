from dataclasses import asdict
import pytest
from parameterized import parameterized
import pandas as pd

from django.test import TestCase
from pyfakefs.fake_filesystem_unittest import Patcher

from panderyx.workflows.test.factories import WorkflowFactory
from panderyx.workflows.tools.helpers import DataTypes
from panderyx.workflows.tools.test.factories import ToolFactory
from panderyx.workflows.tools.dtos.preview_tools import DescribeData
from panderyx.workflows.tools.services.preview_tools import (
    DescribeDataException,
    DescribeDataService,
)
from panderyx.test_helpers.data_sets import test_dataset


class TestInputUrlService(TestCase):
    def setUp(self):
        self.workflow = WorkflowFactory.build()
        self.path = "/foo/bar.txt"
        self.contents = test_dataset

    def test_preview_tool_with_default_data_type(self):
        with Patcher() as patcher:
            patcher.fs.create_file(self.path, contents=self.contents)
            config = asdict(DescribeData(type="describe_data"))
            tool = ToolFactory.build(config=config, workflow=self.workflow)
            service = DescribeDataService(tool)

            df = pd.read_csv(self.path)
            assert df.describe().equals(service.run_tool({0: df}))

    @parameterized.expand(list((t.value,) for t in DataTypes))
    def test_preview_tool_with_different_data_types(self, data_type):
        with Patcher() as patcher:
            patcher.fs.create_file(self.path, contents=self.contents)
            config = asdict(DescribeData(type="describe_data", data_type=data_type))
            tool = ToolFactory.build(config=config, workflow=self.workflow)
            service = DescribeDataService(tool)

            df = pd.read_csv(self.path)
            data_type = DescribeDataService.data_type_mapping[data_type]
            if data_type != ["category"]:
                assert df.describe(include=data_type).equals(service.run_tool({0: df}))
            else:
                with pytest.raises(DescribeDataException):
                    service.run_tool({0: df})
