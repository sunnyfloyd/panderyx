import pytest

from panderyx.users.test.factories import UserFactory
from panderyx.workflows.test.factories import WorkflowFactory
from panderyx.workflows.tools.test.factories import ToolFactory


@pytest.mark.django_db()
class TestWorkflowModel:
    @pytest.fixture()
    def setUp(self) -> None:
        self.user = UserFactory()
        self.workflow = WorkflowFactory(user=self.user)

    def test_tool_execution_order_linear_sequence(self, setUp):
        # tool_1 -> tool_2 -> tool_3
        tool_1 = ToolFactory(workflow=self.workflow)
        tool_3 = ToolFactory(workflow=self.workflow)
        tool_2 = ToolFactory(workflow=self.workflow)
        tool_2.inputs.add(tool_1)
        tool_3.inputs.add(tool_2)

        order = self.workflow.tool_execution_order
        expected_order = [tool_1, tool_2, tool_3]

        assert order == expected_order

    def test_tool_execution_order_linear_double_branch_sequence(self, setUp):
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
        expected_tools = [tool_1, tool_2, tool_3, tool_4, tool_5]

        assert len(order) == len(expected_tools)
        assert set(order) == set(expected_tools)

        assert len(order[1:3]) == len([tool_2, tool_4])
        assert set(order[1:3]) == set([tool_2, tool_4])

        assert len(order[1:3]) == len([tool_2, tool_4])
        assert set(order[3:]) == set([tool_3, tool_5])

    def test_tool_execution_order_linear_double_origin_detached_sequence(self, setUp):
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
        expected_tools = [tool_1, tool_2, tool_3, tool_4, tool_5, tool_6]

        assert len(order) == len(expected_tools)
        assert set(order) == set(expected_tools)

        assert len(order[:2]) == len([tool_1, tool_4])
        assert set(order[:2]) == set([tool_1, tool_4])

        assert len(order[2:4]) == len([tool_2, tool_5])
        assert set(order[2:4]) == set([tool_2, tool_5])

        assert len(order[4:]) == len([tool_3, tool_6])
        assert set(order[4:]) == set([tool_3, tool_6])

    def test_tool_execution_order_non_linear_double_origin_sequence(self, setUp):
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
        expected_tools = [
            tool_1,
            tool_2,
            tool_3,
            tool_4,
            tool_5,
            tool_6,
            tool_7,
            tool_8,
        ]

        assert len(order) == len(expected_tools)
        assert set(order) == set(expected_tools)

        assert len(order[:2]) == len([tool_1, tool_6])
        assert set(order[:2]) == set([tool_1, tool_6])

        assert len(order[2:5]) == len([tool_2, tool_3, tool_7])
        assert set(order[2:5]) == set([tool_2, tool_3, tool_7])

        assert len(order[5:6]) == len([tool_4])
        assert set(order[5:6]) == set([tool_4])

        assert len(order[6:7]) == len([tool_8])
        assert set(order[6:7]) == set([tool_8])

        assert len(order[7:]) == len([tool_5])
        assert set(order[7:]) == set([tool_5])

    def test_tool_execution_order_non_linear_sequence(self, setUp):
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
        expected_tools = [tool_1, tool_2, tool_3, tool_4]

        assert len(order) == len(expected_tools)
        assert set(order) == set(expected_tools)

        assert order[0] == tool_1

        assert len(order[1:3]) == len([tool_2, tool_3])
        assert set(order[1:3]) == set([tool_2, tool_3])

        assert len(order[3:]) == len([tool_4])
        assert set(order[3:]) == set([tool_4])

    def test_tool_execution_order_without_starting_nodes(self, setUp):
        tool_1 = ToolFactory(workflow=self.workflow)
        tool_2 = ToolFactory(workflow=self.workflow)
        tool_3 = ToolFactory(workflow=self.workflow)
        tool_1.inputs.add(tool_3)
        tool_2.inputs.add(tool_1)
        tool_3.inputs.add(tool_2)

        with pytest.raises(ValueError) as exc:
            self.workflow.tool_execution_order

            assert exc.value == "Workflow cannot be run without any input files."
