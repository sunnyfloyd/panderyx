import pytest
from django.test import TestCase

from panderyx.workflows.test.factories import WorkflowFactory
from panderyx.workflows.services import WorkflowService


class TestWorkflowService(TestCase):
    def setUp(self):
        self.workflow = WorkflowFactory.build()

    def test_run_workflow_with_empty_workflow(self):
        service = WorkflowService(self.workflow)

        with pytest.raises(ValueError) as exc:
            service.run_workflow()
            assert "Workflow cannot be run without any input files." == str(exc.value)
