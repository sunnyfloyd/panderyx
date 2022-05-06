from enum import Enum

from panderyx.workflows.tools.dtos.input_tools import InputUrl
from panderyx.workflows.tools.serializers.input_tools import InputUrlSerializer


class ToolMapping(Enum):
    input_url = {"dto": InputUrl, "serializer": InputUrlSerializer}
