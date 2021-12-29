from unittest import TestCase

from pydantic import ValidationError

from workflows import workflow
from exceptions import workflow_exceptions
from exceptions import config_exceptions

from rich import print


class TestToolInsertion(TestCase):
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

        self.workflow.insert_tool("generic", input_ids=[tool_1.id, tool_2.id])
        self.assertEqual(len(self.workflow), 3)

    def test_inserting_tool_with_multiple_outputs(self) -> None:
        tool_1 = self.workflow.insert_tool("input")
        tool_2 = self.workflow.insert_tool("input")

        self.workflow.insert_tool("generic", output_ids=[tool_1.id, tool_2.id])
        self.assertEqual(len(self.workflow), 3)

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

        tool_4 = self.workflow.insert_tool(
            "generic", input_ids=[tool_1.id, tool_2.id, tool_3.id]
        )
        self.assertEqual(len(self.workflow), 4)
        self.assertEqual(len(tool_4.errors["input"]), 1)


class TestToolRemoval(TestCase):
    def setUp(self) -> None:
        self.workflow = workflow.Workflow()

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


class TestToolInputAddition(TestCase):
    def setUp(self) -> None:
        self.workflow = workflow.Workflow()

    def test_adding_proper_input(self) -> None:
        tool_1 = self.workflow.insert_tool("input")
        tool_2 = self.workflow.insert_tool("input")
        tool_3 = self.workflow.insert_tool("large_generic")
        tool_4 = self.workflow.insert_tool("generic")

        self.workflow.add_tool_input(
            tool_id=tool_3.id, input_ids=[tool_1.id, tool_2.id]
        )
        self.assertEqual(tool_3.number_of_inputs, 2)

        self.workflow.add_tool_input(tool_id=tool_3.id, input_ids=tool_4.id)
        self.assertEqual(tool_3.number_of_inputs, 3)

    def test_adding_improper_input(self) -> None:
        tool_1 = self.workflow.insert_tool("input")
        tool_2 = self.workflow.insert_tool("input")
        tool_3 = self.workflow.insert_tool("large_generic")

        self.assertRaises(
            workflow_exceptions.ToolDoesNotExist,
            self.workflow.add_tool_input,
            tool_id=42,
            input_ids=[tool_1.id, tool_2.id],
        )

        self.assertRaises(
            workflow_exceptions.ToolDoesNotExist,
            self.workflow.add_tool_input,
            tool_id=tool_3.id,
            input_ids=[tool_1.id, 42],
        )
        self.assertEqual(tool_3.number_of_inputs, 0)


class TestToolInputRemoval(TestCase):
    def setUp(self) -> None:
        self.workflow = workflow.Workflow()

    def test_removing_proper_input(self) -> None:
        tool_1 = self.workflow.insert_tool("input")
        tool_2 = self.workflow.insert_tool("input")
        tool_3 = self.workflow.insert_tool("large_generic")
        tool_4 = self.workflow.insert_tool("generic")

        self.workflow.add_tool_input(
            tool_id=tool_3.id, input_ids=[tool_1.id, tool_2.id, tool_4.id]
        )
        self.workflow.add_tool_input(tool_id=tool_4.id, input_ids=[tool_2.id])

        self.workflow.remove_tool_input(
            tool_id=tool_3.id, input_ids=[tool_1.id, tool_4.id]
        )
        self.assertEqual(tool_3.number_of_inputs, 1)
        self.assertEqual(set(tool_3.inputs) & {tool_1.id, tool_4.id}, set())

        self.workflow.remove_tool_input(tool_id=tool_4.id, input_ids=tool_2.id)
        self.assertEqual(tool_4.number_of_inputs, 0)
        self.assertEqual(set(tool_4.inputs), set())

    def test_removing_improper_input(self) -> None:
        tool_1 = self.workflow.insert_tool("input")
        tool_2 = self.workflow.insert_tool("input")
        tool_3 = self.workflow.insert_tool("large_generic")
        tool_4 = self.workflow.insert_tool("generic")

        self.workflow.add_tool_input(
            tool_id=tool_3.id, input_ids=[tool_1.id, tool_2.id]
        )
        self.workflow.add_tool_input(tool_id=tool_4.id, input_ids=[tool_2.id])

        self.assertRaises(
            workflow_exceptions.ToolDoesNotExist,
            self.workflow.remove_tool_input,
            tool_id=42,
            input_ids=[tool_1.id, tool_4.id],
        )


class TestSettingToolCoordinates(TestCase):
    def setUp(self) -> None:
        self.workflow = workflow.Workflow()
        self.tool = self.workflow.insert_tool("input")

    def test_setting_proper_coordinates(self) -> None:
        tool = self.workflow.set_tool_coordinates(
            tool_id=self.tool.id, coordinates=(100, 200)
        )

        self.assertEqual(tool._x, 100)
        self.assertEqual(tool._y, 200)

    def test_inserting_tool_with_out_of_range_coordinates(self) -> None:
        # negative x
        self.assertRaises(
            ValueError,
            self.workflow.set_tool_coordinates,
            tool_id=self.tool.id,
            coordinates=(100, -200),
        )
        # negative y
        self.assertRaises(
            ValueError,
            self.workflow.set_tool_coordinates,
            tool_id=self.tool.id,
            coordinates=(-100, 200),
        )
        # negative x and y
        self.assertRaises(
            ValueError,
            self.workflow.set_tool_coordinates,
            tool_id=self.tool.id,
            coordinates=(-100, -200),
        )

    def test_inserting_tool_with_valid_non_int_coordinates(self) -> None:
        # float
        tool = self.workflow.insert_tool("input", coordinates=(100.0, 200.0))
        self.assertEqual(tool._x, 100)
        self.assertEqual(tool._y, 200)

        # int
        tool = self.workflow.insert_tool("input", coordinates=("100", "200"))
        self.assertEqual(tool._x, 100)
        self.assertEqual(tool._y, 200)

    def test_inserting_tool_with_invalid_non_int_coordinates(self) -> None:
        self.assertRaises(
            TypeError,
            self.workflow.insert_tool,
            tool_choice="input",
            coordinates=(100, "200a"),
        )

    def test_inserting_tool_with_proper_coordinates(self) -> None:
        tool = self.workflow.insert_tool("input", coordinates=(100, 200))

        self.assertEqual(tool._x, 100)
        self.assertEqual(tool._y, 200)


class TestSettingToolConfig(TestCase):
    def setUp(self) -> None:
        self.workflow = workflow.Workflow()
        self.tool = self.workflow.insert_tool("input")

    def test_setting_config_with_valid_parameters(self) -> None:
        data = {"path": "http://www.example.com/file.csv", "extension": "csv"}
        self.workflow.set_tool_config(tool_id=self.tool.id, data=data)

        self.assertEqual(self.tool.config.path, "http://www.example.com/file.csv")
        self.assertEqual(self.tool.config.extension, "csv")

    def test_setting_config_with_invalid_parameters(self) -> None:
        data = {"path": "invalid_url", "extension": "csv"}
        self.workflow.set_tool_config(tool_id=self.tool.id, data=data)
        self.assertEqual(
            self.tool.errors["config"][0]["type"], "value_error.url.scheme"
        )

        data = {"path": "http://www.example.com/file.csv"}
        self.workflow.set_tool_config(tool_id=self.tool.id, data=data)
        self.assertEqual(self.tool.errors["config"][0]["type"], "value_error.missing")

        data = {"extension": "csv"}
        self.workflow.set_tool_config(tool_id=self.tool.id, data=data)
        self.assertEqual(self.tool.errors["config"][0]["type"], "value_error.missing")

    def test_setting_config_on_non_config_tool(self) -> None:
        tool = self.workflow._tools[0]
        data = {"path": "http://www.example.com/file.csv", "extension": "csv"}
        self.assertRaises(
            config_exceptions.ConfigClassIsNotDefined,
            self.workflow.set_tool_config,
            tool_id=tool.id,
            data=data,
        )
        self.assertEqual(tool.config, None)
