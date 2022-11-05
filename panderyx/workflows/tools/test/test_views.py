import unittest
from django.forms import model_to_dict

import pytest
from django.urls import reverse
from rest_framework import status

from panderyx.users.test.factories import UserFactory
from panderyx.workflows.models import Workflow
from panderyx.workflows.test.factories import WorkflowFactory
from panderyx.workflows.tools.models import Tool
from panderyx.workflows.tools.test.factories import ToolFactory


@pytest.mark.django_db()
class TestToolListTestCase:
    """
    Tests /tools list operations.
    """

    @pytest.fixture()
    def setUp(self) -> None:
        self.user_1 = UserFactory()
        self.user_2 = UserFactory()
        self.admin = UserFactory(is_staff=True)

        self.workflow_1 = WorkflowFactory(user=self.user_1)
        self.workflow_2 = WorkflowFactory(user=self.user_2)

        ToolFactory.create_batch(5, workflow=self.workflow_1)
        ToolFactory.create_batch(9, workflow=self.workflow_2)

    def test_get_list_of_tools_for_user_workflow(self, setUp, apiclient):
        apiclient.force_authenticate(self.user_1)
        url = reverse("workflow-tools-list", kwargs={"workflow_pk": self.workflow_1.id})
        response = apiclient.get(url)

        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == self.workflow_1.tools.count()

        apiclient.force_authenticate(self.user_2)
        url = reverse("workflow-tools-list", kwargs={"workflow_pk": self.workflow_2.id})
        response = apiclient.get(url)

        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == self.workflow_2.tools.count()

    def test_get_list_of_tools_for_user_workflow_as_admin(self, setUp, apiclient):
        apiclient.force_authenticate(self.admin)
        url = reverse("workflow-tools-list", kwargs={"workflow_pk": self.workflow_1.id})
        response = apiclient.get(url)

        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == self.workflow_1.tools.count()

        url = reverse("workflow-tools-list", kwargs={"workflow_pk": self.workflow_2.id})
        response = apiclient.get(url)

        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == self.workflow_2.tools.count()

    def test_get_list_of_tools_for_user_workflow_as_unauthenticated_user(
        self, setUp, apiclient
    ):
        url = reverse("workflow-tools-list", kwargs={"workflow_pk": self.workflow_1.id})
        response = apiclient.get(url)

        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_post_with_valid_data(self, setUp, apiclient):
        apiclient.force_authenticate(self.user_1)
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
        response = apiclient.post(url, data, format="json")
        tool_id = response.data.get("id")

        assert response.status_code == status.HTTP_201_CREATED
        assert self.workflow_1.id == response.data.get("workflow")
        assert self.workflow_1.tools.filter(pk=tool_id).exists() is True

    @unittest.skip("skip until automated naming is not implemented for tools")
    def test_post_with_no_data(self, setUp, apiclient):
        apiclient.force_authenticate(self.user_1)
        url = reverse("workflow-tools-list", kwargs={"workflow_pk": self.workflow_1.id})
        response = apiclient.post(url, {})

        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_post_with_type_only_config(self, setUp, apiclient):
        url = reverse("workflow-tools-list", kwargs={"workflow_pk": self.workflow_1.id})
        apiclient.force_authenticate(self.user_1)
        data = {
            "config": {"type": "input_url"},
            "name": "test_tool",
            "type": "input_url",
        }
        response = apiclient.post(url, data, format="json")
        tool_id = response.data.get("id")

        assert response.status_code == status.HTTP_201_CREATED
        assert self.workflow_1.id == response.data.get("workflow")
        assert self.workflow_1.tools.filter(pk=tool_id).exists() is True

    def test_post_request_as_unauthenticated_user(self, setUp, apiclient):
        url = reverse("workflow-tools-list", kwargs={"workflow_pk": self.workflow_1.id})
        response = apiclient.post(url, {"name": "test_tool"})

        assert response.status_code == status.HTTP_403_FORBIDDEN
        assert (
            self.workflow_1.tools.filter(name=response.data.get("name")).exists()
            is False
        )

    def test_post_request_with_input_from_different_workflow(self, setUp, apiclient):
        url = reverse("workflow-tools-list", kwargs={"workflow_pk": self.workflow_1.id})
        apiclient.force_authenticate(self.user_1)
        data = {
            "config": {"type": "input_url"},
            "name": "test_tool",
            "type": "input_url",
            "inputs": [self.workflow_2.tools.first().id],
        }
        response = apiclient.post(url, data, format="json")

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert (
            "Provided input tool is not a part of this workflow."
            in response.data.get("inputs")
        )

    def test_post_with_non_unique_workflow_and_tool_names(self, setUp, apiclient):
        url = reverse("workflow-tools-list", kwargs={"workflow_pk": self.workflow_1.id})
        apiclient.force_authenticate(self.user_1)
        data = {
            "config": {"type": "input_url"},
            "name": "test_tool",
            "type": "input_url",
        }
        ToolFactory(workflow=self.workflow_1, name="test_tool")

        response = apiclient.post(url, data, format="json")
        assert response.status_code, status.HTTP_400_BAD_REQUEST
        assert "Tool's name must be unique in the workflow." in response.data.get(
            "workflow"
        )

    def test_post_with_valid_tool_to_other_user_workflow(self, setUp, apiclient):
        apiclient.force_authenticate(self.user_2)
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
        response = apiclient.post(url, data, format="json")

        assert response.status_code == status.HTTP_404_NOT_FOUND
        assert self.workflow_1.tools.count() == 6


@pytest.mark.django_db()
class TestToolDetailTestCase:
    """
    Tests /tools detail operations.
    """

    @pytest.fixture()
    def setUp(self) -> None:
        self.user_1 = UserFactory()
        self.user_2 = UserFactory()
        self.admin = UserFactory(is_staff=True)

        self.workflow_1 = WorkflowFactory(user=self.user_1)
        self.workflow_2 = WorkflowFactory(user=self.user_2)
        # self.workflow_3 = WorkflowFactory.create_batch(8, user=self.admin)

        self.tool_user_1 = ToolFactory(workflow=self.workflow_1)
        self.tool_user_2 = ToolFactory(workflow=self.workflow_2)

    def test_get_non_existing_tool(self, setUp, apiclient):
        url = reverse(
            "workflow-tools-detail", kwargs={"workflow_pk": self.workflow_1.id, "pk": 0}
        )
        apiclient.force_authenticate(self.user_1)
        response = apiclient.get(url)

        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_get_existing_tool_as_owner(self, setUp, apiclient):
        url = reverse(
            "workflow-tools-detail",
            kwargs={"workflow_pk": self.workflow_1.id, "pk": self.tool_user_1.id},
        )
        apiclient.force_authenticate(self.user_1)
        response = apiclient.get(url)

        assert response.status_code == status.HTTP_200_OK
        assert response.data.get("name") == self.tool_user_1.name

    def test_get_existing_tool_as_admin(self, setUp, apiclient):
        url = reverse(
            "workflow-tools-detail",
            kwargs={"workflow_pk": self.workflow_1.id, "pk": self.tool_user_1.id},
        )
        apiclient.force_authenticate(self.admin)
        response = apiclient.get(url)

        assert response.status_code == status.HTTP_200_OK
        assert response.data.get("name") == self.tool_user_1.name

    def test_get_existing_tool_as_other_user(self, setUp, apiclient):
        url = reverse(
            "workflow-tools-detail",
            kwargs={"workflow_pk": self.workflow_1.id, "pk": self.tool_user_1.id},
        )
        apiclient.force_authenticate(self.user_2)
        response = apiclient.get(url)

        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_update_existing_tool_as_owner(self, setUp, apiclient):
        url = reverse(
            "workflow-tools-detail",
            kwargs={"workflow_pk": self.workflow_1.id, "pk": self.tool_user_1.id},
        )
        apiclient.force_authenticate(self.user_1)
        data = {"name": "test_tool", "config": {"type": "input_url"}}
        response = apiclient.put(url, data, format="json")
        self.tool_user_1.refresh_from_db()

        assert response.status_code == status.HTTP_200_OK
        assert response.data.get("name") == self.tool_user_1.name

    def test_update_existing_tool_as_admin(self, setUp, apiclient):
        url = reverse(
            "workflow-tools-detail",
            kwargs={"workflow_pk": self.workflow_1.id, "pk": self.tool_user_1.id},
        )
        apiclient.force_authenticate(self.admin)
        data = {"name": "test_tool", "config": {"type": "input_url"}}
        response = apiclient.put(url, data, format="json")
        self.tool_user_1.refresh_from_db()

        assert response.status_code == status.HTTP_200_OK
        assert response.data.get("name") == self.tool_user_1.name

    def test_update_existing_tool_as_other_user(self, setUp, apiclient):
        url = reverse(
            "workflow-tools-detail",
            kwargs={"workflow_pk": self.workflow_1.id, "pk": self.tool_user_1.id},
        )
        apiclient.force_authenticate(self.user_2)
        response = apiclient.put(url, {"name": "test_tool"})
        self.tool_user_1.refresh_from_db()

        assert response.status_code == status.HTTP_404_NOT_FOUND
        assert "test_tool" != self.tool_user_1.name
