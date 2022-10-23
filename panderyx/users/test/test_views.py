import factory
import pytest
from django.contrib.auth.hashers import check_password
from django.urls import reverse
from faker import Faker
from rest_framework import status

from ..models import User
from .factories import UserFactory

fake = Faker()


@pytest.mark.django_db()
class TestUserListTestCase:
    """
    Tests /users list operations.
    """

    @pytest.fixture()
    def setUp(self):
        self.url = reverse("user-list")
        self.user_data = factory.build(dict, FACTORY_CLASS=UserFactory)

    def test_post_request_with_no_data_fails(self, setUp, apiclient):
        response = apiclient.post(self.url, {})
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_post_request_with_valid_data_succeeds(self, setUp, apiclient):
        response = apiclient.post(self.url, self.user_data)
        assert response.status_code == status.HTTP_201_CREATED

        user = User.objects.get(pk=response.data.get("id"))
        assert user.username == self.user_data.get("username")
        assert check_password(self.user_data.get("password"), user.password) is True


@pytest.mark.django_db()
class TestUserDetailTestCase:
    """
    Tests /users detail operations.
    """

    @pytest.fixture()
    def setUp(self, apiclient):
        self.user = UserFactory()
        self.url = reverse("user-detail", kwargs={"pk": self.user.pk})
        apiclient.credentials(HTTP_AUTHORIZATION=f"Token {self.user.auth_token}")

    def test_get_request_returns_a_given_user(self, setUp, apiclient):
        response = apiclient.get(self.url)
        assert response.status_code == status.HTTP_200_OK

    def test_put_request_updates_a_user(self, setUp, apiclient):
        new_first_name = fake.first_name()
        payload = {"first_name": new_first_name}
        response = apiclient.put(self.url, payload)
        assert response.status_code == status.HTTP_200_OK

        user = User.objects.get(pk=self.user.id)
        assert user.first_name == new_first_name
