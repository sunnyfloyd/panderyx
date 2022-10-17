import typing
from panderyx.workflows.exceptions import WorkflowServiceException

from panderyx.workflows.models import Workflow
from panderyx.workflows.tools.mappings import ToolMapping


class WorkflowService:
    def __init__(self, workflow: Workflow) -> None:
        self.workflow = workflow
        self.tool_result_dfs = {}

    def run_workflow(self) -> None:
        try:
            execution_order = self.workflow.tool_execution_order
        except ValueError:
            raise WorkflowServiceException(
                workflow_id=self.workflow.id,
                message="Workflow cannot be run without any input files.",
                code="workflow_no_inputs",
            )

        for tool in execution_order:
            # TODO
            # below can be replaced with a single DB query using filtering
            # and then I can loop over the inputs
            input_ids = tool.inputs.values_list("id", flat=True)
            # In cases where input order matters it will be handled by proper config fields
            # that will indicate input IDs and their order (depending on the tool logic)
            input_dfs = {
                input_id: self.tool_result_dfs[input_id] for input_id in input_ids
            }

            tool_service_class = ToolMapping[tool.config["type"]].value["service"]
            tool_service = tool_service_class(tool=tool)
            self.tool_result_dfs[tool.id] = tool_service.run_tool(inputs=input_dfs)

    def get_outputs(self) -> typing.List[typing.Dict]:
        json_output = [
            {"tool_id": tool_id, "data": tool.to_json()}
            for tool_id, tool in self.tool_result_dfs.items()
        ]

        return json_output
