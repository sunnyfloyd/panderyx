from unittest import TestCase

from pydantic import ValidationError

from configs import configs


class TestConfigs(TestCase):
    def test_input_config_with_proper_data(self):
        data = {"path": "http://www.example.com/file.csv", "extension": "csv"}

        config = configs.InputConfig(**data)

        self.assertEqual(config.path, "http://www.example.com/file.csv")
        self.assertEqual(config.extension, "csv")

    def test_input_config_with_improper_data(self):
        data = {"path": "invalid_url", "extension": "csv"}
        self.assertRaises(ValidationError, configs.InputConfig, **data)

    def test_input_config_with_missing_required_field(self):
        data = {"extension": "csv"}
        self.assertRaises(ValidationError, configs.InputConfig, **data)

        data = {"path": "http://www.example.com/file.csv"}
        self.assertRaises(ValidationError, configs.InputConfig, **data)
