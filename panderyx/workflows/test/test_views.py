from pprint import pprint

from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, force_authenticate

from panderyx.users.models import User
from panderyx.users.test.factories import UserFactory
from panderyx.workflows.models import Workflow
from panderyx.workflows.test.factories import WorkflowFactory


class TestWorkflowListTestCase(APITestCase):
    def setUp(self) -> None:
        self.url = reverse("workflow-list")
        self.user_1 = UserFactory(username="user_1")
        self.user_2 = UserFactory(username="user_2")
        self.admin = UserFactory(username="admin", is_staff=True)

        WorkflowFactory.create_batch(3, user=self.user_1)
        WorkflowFactory.create_batch(5, user=self.user_2)
        WorkflowFactory.create_batch(8, user=self.admin)

    def test_get_list_of_user_workflows(self):
        self.client.force_login(self.user_1)
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(self.user_1.workflows.count(), len(response.data))

        self.client.force_login(self.user_2)
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(self.user_2.workflows.count(), len(response.data))

    def test_get_list_of_user_workflows_as_admin(self):
        self.client.force_login(self.admin)
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Workflow.objects.count(), len(response.data))
