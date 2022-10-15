from dataclasses import asdict

import pytest

from rest_framework import exceptions

from panderyx.workflows.tools.dtos.preview_tools import DescribeDataConfig
from panderyx.workflows.tools.serializers.preview_tools import (
    DescribeDataConfigSerializer,
)


class TestDescribeDataConfigSerializer:
    valid_data = asdict(DescribeDataConfig())

    def test_serializer_with_valid_data(self):
        serializer = DescribeDataConfigSerializer(data=self.valid_data)
        assert serializer.is_valid() is True

    @pytest.mark.parametrize("number_of_inputs", [10, -3, 1, 2])
    def test_serializer_with_data_overriding_max_number_of_inputs(
        self, number_of_inputs
    ):
        data = self.valid_data.copy()
        data["max_number_of_inputs"] = number_of_inputs
        serializer = DescribeDataConfigSerializer(data=data)

        assert serializer.is_valid() is True
        # None since max_number_of_inputs is injected
        # in ConfigField to_internal_value method
        assert serializer.validated_data.get("max_number_of_inputs") is None

    @pytest.mark.parametrize("data_type", [-1, 4, 10, 232])
    def test_serializer_with_out_of_range_data_type(self, data_type):
        data = self.valid_data.copy()
        data["data_type"] = data_type
        serializer = DescribeDataConfigSerializer(data=data)

        with pytest.raises(exceptions.ValidationError) as exc:
            serializer.is_valid(raise_exception=True)
        if data_type >= 0:
            assert "Ensure this value is less than or equal to 3." in str(
                exc.value.detail.get("data_type")
            )
        else:
            assert "Ensure this value is greater than or equal to 0." in str(
                exc.value.detail.get("data_type")
            )
