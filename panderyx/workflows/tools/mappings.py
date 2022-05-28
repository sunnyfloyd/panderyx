from enum import Enum

from panderyx.workflows.tools.dtos.input_tools import InputUrl
from panderyx.workflows.tools.dtos.preview_tools import DescribeData
from panderyx.workflows.tools.serializers.input_tools import InputUrlSerializer
from panderyx.workflows.tools.serializers.preview_tools import DescribeDataSerializer
from panderyx.workflows.tools.services.input_tools import InputUrlService
from panderyx.workflows.tools.services.preview_tools import DescribeDataService


class ToolMapping(Enum):
    input_url = {
        "dto": InputUrl,
        "serializer": InputUrlSerializer,
        "service": InputUrlService,
        "max_number_of_inputs": 0,
    }
    describe_data = {
        "dto": DescribeData,
        "serializer": DescribeDataSerializer,
        "service": DescribeDataService,
        "max_number_of_inputs": 1,
    }
