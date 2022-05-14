from rest_framework.test import APITestCase

from panderyx.users.test.factories import UserFactory
from panderyx.workflows.test.factories import WorkflowFactory
from panderyx.workflows.tools.test.factories import ToolFactory


class TestWorkflowModel(APITestCase):
    def setUp(self) -> None:
        self.user = UserFactory()
        self.workflow = WorkflowFactory(user=self.user)

    def test_tool_execution_order_linear_sequence(self):
        # tool_1 -> tool_2 -> tool_3
        tool_1 = ToolFactory(workflow=self.workflow)
        tool_3 = ToolFactory(workflow=self.workflow)
        tool_2 = ToolFactory(workflow=self.workflow)
        tool_2.inputs.add(tool_1)
        tool_3.inputs.add(tool_2)

        order = self.workflow.tool_execution_order
        expected_order = [tool_1, tool_2, tool_3]
        self.assertCountEqual(order, expected_order)
        self.assertEqual(order, expected_order)

    def test_tool_execution_order_linear_double_branch_sequence(self):
        # tool_1 -> tool_2 -> tool_3
        #      \
        #       tool_4 -> tool_5

        # 1st sequence
        tool_1 = ToolFactory(workflow=self.workflow)
        tool_3 = ToolFactory(workflow=self.workflow)
        tool_2 = ToolFactory(workflow=self.workflow)
        tool_2.inputs.add(tool_1)
        tool_3.inputs.add(tool_2)

        # 2nd sequence
        tool_5 = ToolFactory(workflow=self.workflow)
        tool_4 = ToolFactory(workflow=self.workflow)
        tool_4.inputs.add(tool_1)
        tool_5.inputs.add(tool_2)

        order = self.workflow.tool_execution_order
        self.assertCountEqual(order, [tool_1, tool_2, tool_3, tool_4, tool_5])
        self.assertEqual(order[0], tool_1)
        self.assertCountEqual(order[1:3], [tool_2, tool_4])
        self.assertCountEqual(order[3:], [tool_3, tool_5])

    def test_tool_execution_order_linear_double_origin_detached_sequence(self):
        # tool_1 -> tool_2 -> tool_3
        # tool_4 -> tool_5 -> tool_6

        # 1st sequence
        tool_1 = ToolFactory(workflow=self.workflow)
        tool_3 = ToolFactory(workflow=self.workflow)
        tool_2 = ToolFactory(workflow=self.workflow)
        tool_2.inputs.add(tool_1)
        tool_3.inputs.add(tool_2)

        # 2nd sequence
        tool_4 = ToolFactory(workflow=self.workflow)
        tool_6 = ToolFactory(workflow=self.workflow)
        tool_5 = ToolFactory(workflow=self.workflow)
        tool_5.inputs.add(tool_4)
        tool_6.inputs.add(tool_5)

        order = self.workflow.tool_execution_order
        self.assertCountEqual(order, [tool_1, tool_2, tool_3, tool_4, tool_5, tool_6])
        self.assertCountEqual(order[:2], [tool_1, tool_4])
        self.assertCountEqual(order[2:4], [tool_2, tool_5])
        self.assertCountEqual(order[4:], [tool_3, tool_6])

    def test_tool_execution_order_non_linear_double_origin_sequence(self):
        #      tool_2
        #      /    \
        # tool_1    tool_4 -> tool_5
        #      \    /   \     /
        #      tool_3    \   /
        #                tool_8
        #               /
        # tool_6 -> tool_7
        tool_1 = ToolFactory(workflow=self.workflow)
        tool_3 = ToolFactory(workflow=self.workflow)
        tool_2 = ToolFactory(workflow=self.workflow)
        tool_4 = ToolFactory(workflow=self.workflow)
        tool_2.inputs.add(tool_1)
        tool_3.inputs.add(tool_1)
        tool_4.inputs.add(tool_2)
        tool_4.inputs.add(tool_3)

        tool_5 = ToolFactory(workflow=self.workflow)
        tool_6 = ToolFactory(workflow=self.workflow)
        tool_7 = ToolFactory(workflow=self.workflow)
        tool_8 = ToolFactory(workflow=self.workflow)
        tool_5.inputs.add(tool_4)
        tool_5.inputs.add(tool_8)
        tool_7.inputs.add(tool_6)
        tool_8.inputs.add(tool_7)
        tool_8.inputs.add(tool_4)

        order = self.workflow.tool_execution_order
        self.assertCountEqual(
            order, [tool_1, tool_2, tool_3, tool_4, tool_5, tool_6, tool_7, tool_8]
        )
        self.assertCountEqual(order[:2], [tool_1, tool_6])
        self.assertCountEqual(order[2:5], [tool_2, tool_3, tool_7])
        self.assertCountEqual(order[5:6], [tool_4])
        self.assertCountEqual(order[6:7], [tool_8])
        self.assertCountEqual(order[7:], [tool_5])

    def test_tool_execution_order_non_linear_sequence(self):
        #      tool_2
        #      /    \
        # tool_1    tool_4
        #      \    /
        #      tool_3
        tool_1 = ToolFactory(workflow=self.workflow)
        tool_3 = ToolFactory(workflow=self.workflow)
        tool_2 = ToolFactory(workflow=self.workflow)
        tool_4 = ToolFactory(workflow=self.workflow)
        tool_2.inputs.add(tool_1)
        tool_3.inputs.add(tool_1)
        tool_4.inputs.add(tool_2)
        tool_4.inputs.add(tool_3)

        order = self.workflow.tool_execution_order
        self.assertCountEqual(order, [tool_1, tool_2, tool_3, tool_4])
        self.assertEqual(order[0], tool_1)
        self.assertCountEqual(order[1:3], [tool_2, tool_3])
        self.assertCountEqual(order[3:], [tool_4])

    def test_tool_execution_order_without_starting_nodes(self):
        tool_1 = ToolFactory(workflow=self.workflow)
        tool_2 = ToolFactory(workflow=self.workflow)
        tool_3 = ToolFactory(workflow=self.workflow)
        tool_1.inputs.add(tool_3)
        tool_2.inputs.add(tool_1)
        tool_3.inputs.add(tool_2)

        with self.assertRaisesMessage(
            ValueError, "Workflow cannot be run without any input files."
        ):
            self.workflow.tool_execution_order
