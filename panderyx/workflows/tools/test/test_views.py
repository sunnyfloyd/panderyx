import unittest
from django.forms import model_to_dict

from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from panderyx.users.test.factories import UserFactory
from panderyx.workflows.models import Workflow
from panderyx.workflows.test.factories import WorkflowFactory
from panderyx.workflows.tools.models import Tool
from panderyx.workflows.tools.test.factories import ToolFactory


class TestToolListTestCase(APITestCase):
    """
    Tests /tools list operations.
    """

    def setUp(self) -> None:
        self.user_1 = UserFactory()
        self.user_2 = UserFactory()
        self.admin = UserFactory(is_staff=True)

        self.workflow_1 = WorkflowFactory(user=self.user_1)
        self.workflow_2 = WorkflowFactory(user=self.user_2)
        # self.workflow_3 = WorkflowFactory.create_batch(8, user=self.admin)

        ToolFactory.create_batch(5, workflow=self.workflow_1)
        ToolFactory.create_batch(9, workflow=self.workflow_2)

    def test_get_list_of_tools_for_user_workflow(self):
        self.client.force_login(self.user_1)
        url = reverse("workflow-tools-list", kwargs={"workflow_pk": self.workflow_1.id})
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), self.workflow_1.tools.count())

        self.client.force_login(self.user_2)
        url = reverse("workflow-tools-list", kwargs={"workflow_pk": self.workflow_2.id})
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), self.workflow_2.tools.count())

    def test_get_list_of_tools_for_user_workflow_as_admin(self):
        self.client.force_login(self.admin)
        url = reverse("workflow-tools-list", kwargs={"workflow_pk": self.workflow_1.id})
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), self.workflow_1.tools.count())

        url = reverse("workflow-tools-list", kwargs={"workflow_pk": self.workflow_2.id})
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), self.workflow_2.tools.count())

    def test_get_list_of_tools_for_user_workflow_as_unauthenticated_user(self):
        url = reverse("workflow-tools-list", kwargs={"workflow_pk": self.workflow_1.id})
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_post_with_valid_data(self):
        self.client.force_login(self.user_1)
        url = reverse("workflow-tools-list", kwargs={"workflow_pk": self.workflow_1.id})
        input_tool = ToolFactory(workflow=self.workflow_1)
        data = model_to_dict(input_tool)
        data.update(
            {
                "name": "test_tool",
                "config": {"type": "describe_data"},
                "inputs": [input_tool.id],
            }
        )
        response = self.client.post(url, data, format="json")
        tool_id = response.data.get("id")

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(self.workflow_1.id, response.data.get("workflow"))
        self.assertEqual(self.workflow_1.tools.filter(pk=tool_id).exists(), True)

    @unittest.skip("skip until automated naming is not implemented for tools")
    def test_post_with_no_data(self):
        self.client.force_login(self.user_1)
        url = reverse("workflow-tools-list", kwargs={"workflow_pk": self.workflow_1.id})
        response = self.client.post(url, {})

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_post_with_type_only_config(self):
        url = reverse("workflow-tools-list", kwargs={"workflow_pk": self.workflow_1.id})
        self.client.force_login(self.user_1)
        data = {
            "config": {"type": "input_url"},
            "name": "test_tool",
            "type": "input_url",
        }
        response = self.client.post(url, data, format="json")
        tool_id = response.data.get("id")

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(self.workflow_1.id, response.data.get("workflow"))
        self.assertEqual(self.workflow_1.tools.filter(pk=tool_id).exists(), True)

    def test_post_request_as_unauthenticated_user(self):
        url = reverse("workflow-tools-list", kwargs={"workflow_pk": self.workflow_1.id})
        response = self.client.post(url, {"name": "test_tool"})

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(
            self.workflow_1.tools.filter(name=response.data.get("name")).exists(), False
        )

    def test_post_request_with_input_from_different_workflow(self):
        url = reverse("workflow-tools-list", kwargs={"workflow_pk": self.workflow_1.id})
        self.client.force_login(self.user_1)
        data = {
            "config": {"type": "input_url"},
            "name": "test_tool",
            "type": "input_url",
            "inputs": [self.workflow_2.tools.first().id],
        }
        response = self.client.post(url, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn(
            "Provided input tool is not a part of this workflow.",
            response.data.get("inputs"),
        )

    def test_post_with_non_unique_workflow_and_tool_names(self):
        url = reverse("workflow-tools-list", kwargs={"workflow_pk": self.workflow_1.id})
        self.client.force_login(self.user_1)
        data = {
            "config": {"type": "input_url"},
            "name": "test_tool",
            "type": "input_url",
        }
        ToolFactory(workflow=self.workflow_1, name="test_tool")

        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn(
            "Tool's name must be unique in the workflow.", response.data.get("workflow")
        )

    def test_post_with_valid_tool_to_other_user_workflow(self):
        ...


class TestToolDetailTestCase(APITestCase):
    """
    Tests /tools detail operations.
    """

    def setUp(self) -> None:
        self.user_1 = UserFactory()
        self.user_2 = UserFactory()
        self.admin = UserFactory(is_staff=True)

        self.workflow_1 = WorkflowFactory(user=self.user_1)
        self.workflow_2 = WorkflowFactory(user=self.user_2)
        # self.workflow_3 = WorkflowFactory.create_batch(8, user=self.admin)

        self.tool_user_1 = ToolFactory(workflow=self.workflow_1)
        self.tool_user_2 = ToolFactory(workflow=self.workflow_2)

    def test_get_non_existing_tool(self):
        url = reverse(
            "workflow-tools-detail", kwargs={"workflow_pk": self.workflow_1.id, "pk": 0}
        )
        self.client.force_login(self.user_1)
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_get_existing_tool_as_owner(self):
        url = reverse(
            "workflow-tools-detail",
            kwargs={"workflow_pk": self.workflow_1.id, "pk": self.tool_user_1.id},
        )
        self.client.force_login(self.user_1)
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data.get("name"), self.tool_user_1.name)

    def test_get_existing_tool_as_admin(self):
        url = reverse(
            "workflow-tools-detail",
            kwargs={"workflow_pk": self.workflow_1.id, "pk": self.tool_user_1.id},
        )
        self.client.force_login(self.admin)
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data.get("name"), self.tool_user_1.name)

    def test_get_existing_tool_as_other_user(self):
        url = reverse(
            "workflow-tools-detail",
            kwargs={"workflow_pk": self.workflow_1.id, "pk": self.tool_user_1.id},
        )
        self.client.force_login(self.user_2)
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_update_existing_tool_as_owner(self):
        url = reverse(
            "workflow-tools-detail",
            kwargs={"workflow_pk": self.workflow_1.id, "pk": self.tool_user_1.id},
        )
        self.client.force_login(self.user_1)
        data = {"name": "test_tool", "config": {"type": "input_url"}}
        response = self.client.put(url, data, format="json")
        self.tool_user_1.refresh_from_db()

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data.get("name"), self.tool_user_1.name)

    def test_update_existing_tool_as_admin(self):
        url = reverse(
            "workflow-tools-detail",
            kwargs={"workflow_pk": self.workflow_1.id, "pk": self.tool_user_1.id},
        )
        self.client.force_login(self.admin)
        data = {"name": "test_tool", "config": {"type": "input_url"}}
        response = self.client.put(url, data, format="json")
        self.tool_user_1.refresh_from_db()

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data.get("name"), self.tool_user_1.name)

    def test_update_existing_tool_as_other_user(self):
        url = reverse(
            "workflow-tools-detail",
            kwargs={"workflow_pk": self.workflow_1.id, "pk": self.tool_user_1.id},
        )
        self.client.force_login(self.user_2)
        response = self.client.put(url, {"name": "test_tool"})
        self.tool_user_1.refresh_from_db()

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertNotEqual("test_tool", self.tool_user_1.name)
