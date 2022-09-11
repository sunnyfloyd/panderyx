from dataclasses import asdict

import pytest

from rest_framework import exceptions
from rest_framework.test import APITestCase

from panderyx.workflows.tools.dtos.input_tools import InputUrl
from panderyx.workflows.tools.serializers.input_tools import InputUrlSerializer


class TestInputUrlSerializer:
    valid_data = asdict(InputUrl(url="http://www.mock.com"))

    def test_serializer_with_valid_data(self):
        serializer = InputUrlSerializer(data=self.valid_data)
        assert serializer.is_valid() == True

    @pytest.mark.parametrize(
        "number_of_inputs,err_msg",
        [
            (
                10,
                {
                    "max_number_of_inputs": "Ensure this value is less than or equal to 0."
                },
            ),
            (
                -3,
                {
                    "max_number_of_inputs": "Ensure this value is more than or equal to 0."
                },
            ),
        ],
    )
    def test_serializer_with_data_overriding_max_number_of_inputs(
        self, number_of_inputs, err_msg
    ):
        data = self.valid_data.copy()
        data["max_number_of_inputs"] = number_of_inputs
        serializer = InputUrlSerializer(data=data)

        with pytest.raises(exceptions.ValidationError) as err:
            serializer.is_valid(raise_exception=True)
            assert err.value == err_msg
