import typing

from rest_framework import status
from rest_framework.exceptions import APIException


class WorkflowServiceException(APIException):
    workflow_id: typing.Union[str, None] = None
    message: typing.Union[str, None] = None
    status_code: int = status.HTTP_400_BAD_REQUEST
    code: str = "workflow_error"

    def __init__(self, workflow_id, detail=None, code=None, message=None):
        self.workflow_id = workflow_id
        self.message = message or self.message
        self.code = code or self.code
        super().__init__(self._error_message, code)

    @property
    def _error_message(self):
        return {
            "workflow_id": self.workflow_id,
            "message": self.message,
        }


class ToolServiceException(APIException):
    tool_id: typing.Union[int, None] = None
    message: typing.Union[str, None] = None
    status_code: int = status.HTTP_400_BAD_REQUEST
    code: str = "tool_error"

    def __init__(self, tool_id, detail=None, code=None, message=None):
        self.tool_id = tool_id
        self.message = message or self.message
        self.code = code or self.code
        super().__init__(self._error_message, code)

    @property
    def _error_message(self):
        return {
            "tool_id": self.tool_id,
            "message": self.message,
        }

# TODO Maybe this kind of a common error should endup in the
# base class wrapper and be populated there instead of being added
# to each tool that is vulnerable for such exception
class MissingToolInput(ToolServiceException):
    message = "Tool is missing input to process."
    code = "missing_input"
