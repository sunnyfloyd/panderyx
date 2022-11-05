from rest_framework.test import APIClient
import pytest
from pyfakefs.fake_filesystem_unittest import Patcher

from panderyx.test_helpers.data_sets import test_dataset

@pytest.fixture
def apiclient():
    return APIClient()


@pytest.fixture()
def test_dataset_path():
    with Patcher() as patcher:
        path = "/foo/bar.txt"
        contents = test_dataset
        patcher.fs.create_file(path, contents=contents)
        yield path
