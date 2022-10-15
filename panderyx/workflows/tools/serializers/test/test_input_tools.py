from dataclasses import asdict

import pytest

from panderyx.workflows.tools.dtos.input_tools import InputUrlConfig
from panderyx.workflows.tools.serializers.input_tools import InputUrlConfigSerializer


class TestInputUrlConfigSerializer:
    valid_data = asdict(InputUrlConfig(url="http://www.mock.com"))

    def test_serializer_with_valid_data(self):
        serializer = InputUrlConfigSerializer(data=self.valid_data)
        assert serializer.is_valid() is True

    @pytest.mark.parametrize("number_of_inputs", [10, -3, 1, 2])
    def test_serializer_with_data_overriding_max_number_of_inputs(
        self, number_of_inputs
    ):
        data = self.valid_data.copy()
        data["max_number_of_inputs"] = number_of_inputs
        serializer = InputUrlConfigSerializer(data=data)

        assert serializer.is_valid() is True
        # None since max_number_of_inputs is injected
        # in ConfigField to_internal_value method
        assert serializer.validated_data.get("max_number_of_inputs") is None

    def test_serializer_with_incorrect_url(self):
        ...
