from unittest import TestCase
from workflows import workflow
from exceptions import workflow_exceptions, tool_exceptions
from rich import print


class TestWorkflow(TestCase):
    def setUp(self) -> None:
        self.workflow = workflow.Workflow()

    def test_inserting_existing_tool(self) -> None:
        self.workflow.insert_tool("input")
        self.workflow.insert_tool("input")
        self.workflow.insert_tool("generic")
        self.workflow.insert_tool("generic")

        self.assertEqual(len(self.workflow), 4)

    def test_inserting_non_existing_tool(self) -> None:
        self.assertRaises(
            workflow_exceptions.ToolNotAvailable,
            self.workflow.insert_tool,
            tool_choice="inputs",
        )
        self.assertRaises(
            workflow_exceptions.ToolNotAvailable,
            self.workflow.insert_tool,
            tool_choice="non_existing_tool",
        )

        self.assertEqual(len(self.workflow), 0)

    def test_inserting_root_tool(self) -> None:
        self.assertRaises(
            workflow_exceptions.ToolNotAvailable,
            self.workflow.insert_tool,
            tool_choice="root",
        )

        self.assertEqual(len(self.workflow), 0)

    def test_inserting_tool_with_multiple_inputs(self) -> None:
        tool_1 = self.workflow.insert_tool("input")
        tool_2 = self.workflow.insert_tool("input")
        tool_3 = self.workflow.insert_tool("generic")

        self.workflow.insert_tool("generic", input_ids=[tool_1.id, tool_2.id])
        self.assertEqual(len(self.workflow), 4)

    def test_inserting_tool_with_multiple_outputs(self) -> None:
        tool_1 = self.workflow.insert_tool("input")
        tool_2 = self.workflow.insert_tool("input")
        tool_3 = self.workflow.insert_tool("generic")

        self.workflow.insert_tool("generic", output_ids=[tool_1.id, tool_2.id])
        self.assertEqual(len(self.workflow), 4)

    def test_inserting_tool_with_single_input(self) -> None:
        tool_1 = self.workflow.insert_tool("input")

        self.workflow.insert_tool("generic", input_ids=tool_1.id)
        self.assertEqual(len(self.workflow), 2)

    def test_inserting_tool_with_single_output(self) -> None:
        tool_1 = self.workflow.insert_tool("input")

        self.workflow.insert_tool("generic", output_ids=tool_1.id)
        self.assertEqual(len(self.workflow), 2)

    def test_inserting_tool_with_multiple_inputs_and_single_output(self) -> None:
        tool_1 = self.workflow.insert_tool("input")
        tool_2 = self.workflow.insert_tool("input")
        tool_3 = self.workflow.insert_tool("generic")

        self.workflow.insert_tool(
            "generic", input_ids=[tool_1.id, tool_2.id], output_ids=tool_3.id
        )
        self.assertEqual(len(self.workflow), 4)

    def test_inserting_tool_with_single_input_and_multiple_outputs(self) -> None:
        tool_1 = self.workflow.insert_tool("input")
        tool_2 = self.workflow.insert_tool("generic")
        tool_3 = self.workflow.insert_tool("generic")

        self.workflow.insert_tool(
            "generic", input_ids=tool_1.id, output_ids=[tool_2.id, tool_3.id]
        )
        self.assertEqual(len(self.workflow), 4)

    def test_inserting_tool_with_multiple_inputs_and_multiple_outputs(self) -> None:
        tool_1 = self.workflow.insert_tool("input")
        tool_2 = self.workflow.insert_tool("generic")
        tool_3 = self.workflow.insert_tool("generic")
        tool_4 = self.workflow.insert_tool("generic")

        self.workflow.insert_tool(
            "generic",
            input_ids=[tool_1.id, tool_2.id],
            output_ids=[tool_2.id, tool_3.id, tool_4.id],
        )
        self.assertEqual(len(self.workflow), 5)

    def test_inserting_tool_with_too_many_inputs(self) -> None:
        tool_1 = self.workflow.insert_tool("input")
        tool_2 = self.workflow.insert_tool("generic")
        tool_3 = self.workflow.insert_tool("generic")

        self.assertRaises(
            tool_exceptions.TooManyInputs,
            self.workflow.insert_tool,
            tool_choice="generic",
            input_ids=[tool_1.id, tool_2.id, tool_3.id],
        )
        self.assertEqual(len(self.workflow), 3)

    def test_removing_existing_tool(self) -> None:
        tool_id = self.workflow.insert_tool("input").id
        self.workflow.remove_tool(tool_ids=tool_id)

        self.assertEqual(len(self.workflow), 0)

    def test_removing_non_existing_tool(self) -> None:
        self.assertRaises(
            workflow_exceptions.ToolDoesNotExist, self.workflow.remove_tool, tool_ids=42
        )
        self.assertRaises(
            workflow_exceptions.ToolDoesNotExist, self.workflow.remove_tool, tool_ids=-1
        )

        self.assertEqual(len(self.workflow), 0)

    def test_removing_root_tool(self) -> None:
        self.assertRaises(
            workflow_exceptions.ToolDoesNotExist, self.workflow.remove_tool, tool_ids=42
        )
        self.assertRaises(
            workflow_exceptions.RootCannotBeDeleted,
            self.workflow.remove_tool,
            tool_ids=-0,
        )

        self.assertEqual(len(self.workflow), 0)

    def test_adding_proper_input(self) -> None:
        tool_1 = self.workflow.insert_tool("input")
        tool_2 = self.workflow.insert_tool("input")
        tool_3 = self.workflow.insert_tool("large_generic")
        tool_4 = self.workflow.insert_tool("generic")

        self.workflow.add_tool_input(
            tool_id=tool_3.id, input_ids=[tool_1.id, tool_2.id]
        )
        self.assertEqual(len(tool_3.inputs), 2)

        self.workflow.add_tool_input(
            tool_id=tool_3.id, input_ids=tool_4.id
        )
        self.assertEqual(len(tool_3.inputs), 3)

    def test_adding_improper_input(self) -> None:
        ...

    def test_removing_proper_input(self) -> None:
        ...

    def test_removing_improper_input(self) -> None:
        ...
