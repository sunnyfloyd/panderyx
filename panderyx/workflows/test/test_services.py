import pytest
from django.test import TestCase
from panderyx.workflows.exceptions import WorkflowServiceException

from panderyx.workflows.test.factories import WorkflowFactory
from panderyx.workflows.services import WorkflowService


class TestWorkflowService(TestCase):
    def setUp(self):
        self.workflow = WorkflowFactory.build()

    def test_run_workflow_with_empty_workflow(self):
        service = WorkflowService(self.workflow)

        with pytest.raises(WorkflowServiceException) as exc:
            service.run_workflow()
            assert {
                "detail": {
                    "workflow_id": self.workflow.id,
                    "message": "Workflow cannot be run without any input files.",
                }
            } == exc.value
