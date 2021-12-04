from unittest import TestCase
from workflows import workflow


class TestWorkflow(TestCase):
    def setUp(self) -> None:
        self.workflow = workflow.Workflow()

    def test_inserting_proper_tool(self):
        ...

    def test_inserting_improper_tool(self):
        ...

    def test_removing_proper_tool(self):
        ...

    def test_removing_improper_tool(self):
        ...

    def test_adding_proper_input(self):
        ...

    def test_adding_improper_input(self):
        ...

    def test_removing_proper_input(self):
        ...

    def test_removing_improper_input(self):
        ...
