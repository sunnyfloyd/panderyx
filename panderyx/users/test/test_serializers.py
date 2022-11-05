import pytest
from django.contrib.auth.hashers import check_password
from django.forms.models import model_to_dict

from ..serializers import CreateUserSerializer
from .factories import UserFactory


@pytest.mark.django_db()
class TestCreateUserSerializer:
    @pytest.fixture()
    def setUp(self):
        self.user_data = model_to_dict(UserFactory.build())

    def test_serializer_with_empty_data(self, setUp):
        serializer = CreateUserSerializer(data={})
        assert serializer.is_valid() is False

    def test_serializer_with_valid_data(self, setUp):
        serializer = CreateUserSerializer(data=self.user_data)
        assert serializer.is_valid() is True

    def test_serializer_hashes_password(self, setUp):
        serializer = CreateUserSerializer(data=self.user_data)
        assert serializer.is_valid() is True

        user = serializer.save()
        assert check_password(self.user_data.get("password"), user.password) is True
