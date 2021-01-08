import unittest
from unittest.mock import patch
import os
from dokerc.config import config


class TestConfig(unittest.TestCase):
    @patch("os.path.exists")
    def test_check_for_default_config_fail(self, path_patch):
        path_patch.return_value = False
        self.assertFalse(config.check_for_default_config())
        path_patch.assert_called_once_with(
            os.path.join(config.DEFAULT_CONFIG_LOCATION, config.DEFAULT_CONFIG_NAME)
        )

    @patch("os.path.exists")
    def test_check_for_default_config_success(self, path_patch):
        path_patch.return_value = True
        self.assertTrue(config.check_for_default_config())
        path_patch.assert_called_once_with(
            os.path.join(config.DEFAULT_CONFIG_LOCATION, config.DEFAULT_CONFIG_NAME)
        )

    @patch("os.path.exists")
    def test_get_config_fails_due_to_no_default_config(self, path_patch):
        path_patch.return_value = False

        with self.assertRaises(config.ConfigError) as ce:
            config.get_config()
        self.assertEqual("Unable to read default config", str(ce.exception))

        path_patch.assert_called_once_with(
            os.path.join(config.DEFAULT_CONFIG_LOCATION, config.DEFAULT_CONFIG_NAME)
        )

    @patch("os.path.exists")
    def test_get_config_fails_due_to_no_valid_config(self, path_patch):
        path_patch.return_value = False

        with self.assertRaises(config.ConfigError) as ce:
            config.get_config(file="config.ini")
        self.assertEqual("Unable to read provided config", str(ce.exception))

        path_patch.assert_called_once_with("config.ini")
