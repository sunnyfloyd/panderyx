from enum import Enum

from panderyx.workflows.tools.dtos.input_tools import InputUrlConfig
from panderyx.workflows.tools.dtos.preview_tools import DescribeDataConfig
from panderyx.workflows.tools.serializers.input_tools import InputUrlConfigSerializer
from panderyx.workflows.tools.serializers.preview_tools import DescribeDataConfigSerializer
from panderyx.workflows.tools.services.input_tools import InputUrlService
from panderyx.workflows.tools.services.preview_tools import DescribeDataService


class ToolMapping(Enum):
    input_url = {
        "dto": InputUrlConfig,
        "serializer": InputUrlConfigSerializer,
        "service": InputUrlService,
        "max_number_of_inputs": 0,
    }
    describe_data = {
        "dto": DescribeDataConfig,
        "serializer": DescribeDataConfigSerializer,
        "service": DescribeDataService,
        "max_number_of_inputs": 1,
    }
