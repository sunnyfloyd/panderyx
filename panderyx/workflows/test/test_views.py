from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from panderyx.users.test.factories import UserFactory
from panderyx.workflows.models import Workflow
from panderyx.workflows.test.factories import WorkflowFactory


class TestWorkflowListTestCase(APITestCase):
    """
    Tests /workflows list operations.
    """

    def setUp(self) -> None:
        self.url = reverse("workflow-list")
        self.user_1 = UserFactory()
        self.user_2 = UserFactory()
        self.admin = UserFactory(is_staff=True)

        WorkflowFactory.create_batch(3, user=self.user_1)
        WorkflowFactory.create_batch(5, user=self.user_2)
        WorkflowFactory.create_batch(8, user=self.admin)

    def test_get_list_of_user_workflows(self):
        self.client.force_login(self.user_1)
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), self.user_1.workflows.count())

        self.client.force_login(self.user_2)
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), self.user_2.workflows.count())

    def test_get_list_of_users_workflows_as_admin(self):
        self.client.force_login(self.admin)
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), Workflow.objects.count())

    def test_get_list_of_user_workflows_as_unauthenticated_user(self):
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_post_with_no_data(self):
        self.client.force_login(self.user_1)
        response = self.client.post(self.url, {})

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_post_with_read_only_data(self):
        self.client.force_login(self.user_1)
        response = self.client.post(
            self.url, {"name": "test_workflow", "user": self.user_2.id}
        )

        self.assertEqual(self.user_1.id, str(response.data.get("user")))
        self.assertEqual(
            self.user_1.workflows.filter(name=response.data.get("name")).exists(), True
        )

    def test_post_with_valid_data(self):
        self.client.force_login(self.user_1)
        response = self.client.post(self.url, {"name": "test_workflow"})

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(
            self.user_1.workflows.filter(name=response.data.get("name")).exists(), True
        )

    def test_post_request_as_unauthenticated_user(self):
        response = self.client.post(self.url, {"name": "test_workflow"})

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(
            self.user_1.workflows.filter(name=response.data.get("name")).exists(), False
        )


class TestWorkflowDetailTestCase(APITestCase):
    """
    Tests /workflows detail operations.
    """

    def setUp(self) -> None:
        self.user_1 = UserFactory()
        self.user_2 = UserFactory()
        self.admin = UserFactory(is_staff=True)

        self.workflow_user_1 = WorkflowFactory(user=self.user_1)
        self.workflow_user_2 = WorkflowFactory(user=self.user_2)

    def test_get_non_existing_workflow(self):
        url = reverse("workflow-detail", kwargs={"pk": "no-such-id"})
        self.client.force_login(self.user_1)
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_get_existing_workflow_as_owner(self):
        url = reverse("workflow-detail", kwargs={"pk": self.workflow_user_1.id})
        self.client.force_login(self.user_1)
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data.get("name"), self.workflow_user_1.name)

    def test_get_existing_workflow_as_admin(self):
        url = reverse("workflow-detail", kwargs={"pk": self.workflow_user_1.id})
        self.client.force_login(self.admin)
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data.get("name"), self.workflow_user_1.name)

    def test_get_existing_workflow_as_other_user(self):
        url = reverse("workflow-detail", kwargs={"pk": self.workflow_user_1.id})
        self.client.force_login(self.user_2)
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_update_existing_workflow_as_owner(self):
        url = reverse("workflow-detail", kwargs={"pk": self.workflow_user_1.id})
        self.client.force_login(self.user_1)
        response = self.client.put(url, {"name": "test_workflow"})
        self.workflow_user_1.refresh_from_db()

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data.get("name"), self.workflow_user_1.name)

    def test_update_existing_workflow_as_admin(self):
        url = reverse("workflow-detail", kwargs={"pk": self.workflow_user_1.id})
        self.client.force_login(self.admin)
        response = self.client.put(url, {"name": "test_workflow"})
        self.workflow_user_1.refresh_from_db()

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data.get("name"), self.workflow_user_1.name)

    def test_update_existing_workflow_as_other_user(self):
        url = reverse("workflow-detail", kwargs={"pk": self.workflow_user_1.id})
        self.client.force_login(self.user_2)
        response = self.client.put(url, {"name": "test_workflow"})
        self.workflow_user_1.refresh_from_db()

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertNotEqual("test_workflow", self.workflow_user_1.name)
