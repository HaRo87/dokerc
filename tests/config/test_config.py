import unittest
import pathlib
from unittest.mock import patch
import os
from dokerc.config import config
import tempfile
from configparser import ConfigParser


class TestConfig(unittest.TestCase):
    config_dir = pathlib.Path.cwd() / "tests" / "files"

    @patch("os.path.exists")
    def test_check_for_default_config_fail(self, path_patch):
        path_patch.return_value = False
        self.assertFalse(config.check_for_default_config())
        path_patch.assert_called_once_with(
            os.path.join(
                pathlib.Path.home(),
                config.DEFAULT_CONFIG_LOCATION,
                config.DEFAULT_CONFIG_NAME,
            )
        )

    @patch("os.path.exists")
    def test_check_for_default_config_success(self, path_patch):
        path_patch.return_value = True
        self.assertTrue(config.check_for_default_config())
        path_patch.assert_called_once_with(
            os.path.join(
                pathlib.Path.home(),
                config.DEFAULT_CONFIG_LOCATION,
                config.DEFAULT_CONFIG_NAME,
            )
        )

    @patch("os.path.exists")
    def test_get_config_fails_due_to_no_default_config(self, path_patch):
        path_patch.return_value = False

        with self.assertRaises(config.ConfigError) as ce:
            config.get_config()
        self.assertEqual("Unable to read default config", str(ce.exception))

        path_patch.assert_called_once_with(
            os.path.join(
                pathlib.Path.home(),
                config.DEFAULT_CONFIG_LOCATION,
                config.DEFAULT_CONFIG_NAME,
            )
        )

    @patch("os.path.exists")
    def test_get_config_fails_due_to_no_valid_config(self, path_patch):
        path_patch.return_value = False

        with self.assertRaises(config.ConfigError) as ce:
            config.get_config(file="config.ini")
        self.assertEqual("Unable to read provided config", str(ce.exception))

        path_patch.assert_called_once_with("config.ini")

    def test_get_config_from_provided_file_success(self):
        config_path = self.config_dir / "config.ini"
        conf = config.get_config(file=config_path)
        self.assertEqual("http://localhost", conf.server.address)
        self.assertEqual(5000, int(conf.server.port))
        self.assertEqual("/api", conf.server.endpoint)
        self.assertEqual("Tigger", conf.user.name)

    def test_validate_config_fails_due_to_no_server_address(self):
        conf = config.Config(
            config.Server(
                "",
                5000,
                "/api",
            ),
            config.User(
                "Tigger",
            ),
        )
        with self.assertRaises(config.ConfigError) as ce:
            config.validate_config(conf)
        self.assertEqual("Invalid server address", str(ce.exception))

    def test_validate_config_fails_due_to_invalid_port(self):
        conf = config.Config(
            config.Server(
                "http://localhost",
                -1,
                "/api",
            ),
            config.User(
                "Tigger",
            ),
        )
        with self.assertRaises(config.ConfigError) as ce:
            config.validate_config(conf)
        self.assertEqual("Invalid server port", str(ce.exception))

    def test_validate_config_fails_due_to_no_user_name(self):
        conf = config.Config(
            config.Server(
                "http://localhost",
                5000,
                "/api",
            ),
            config.User(
                "",
            ),
        )
        with self.assertRaises(config.ConfigError) as ce:
            config.validate_config(conf)
        self.assertEqual("Invalid user name", str(ce.exception))

    def test_validate_config_success(self):
        conf = config.Config(
            config.Server(
                "http://localhost",
                5000,
                "/api",
            ),
            config.User(
                "Tigger",
            ),
        )
        config.validate_config(conf)

    def test_write_config_into_existing_dir(self):
        config_parser = ConfigParser()
        conf = config.Config(
            config.Server(
                "http://localhost",
                5000,
                "/api",
            ),
            config.User(
                "Tigger",
            ),
        )

        with tempfile.TemporaryDirectory() as dir:
            config_path = os.path.join(dir, "config.ini")
            config._write_config(conf, config_path)
            self.assertTrue(os.path.exists(config_path))
            config_parser.read(config_path)
            server_info = config_parser["SERVER"]
            user_info = config_parser["USER"]
            self.assertEqual("http://localhost", server_info["address"])
            self.assertEqual(5000, int(server_info["port"]))
            self.assertEqual("/api", server_info["endpoint"])
            self.assertEqual("Tigger", user_info["name"])

    def test_write_config_into_non_existing_dir(self):
        config_parser = ConfigParser()
        conf = config.Config(
            config.Server(
                "http://localhost",
                5000,
                "/api",
            ),
            config.User(
                "Tigger",
            ),
        )

        with tempfile.TemporaryDirectory() as dir:
            config_path = os.path.join(dir, ".config", "config.ini")
            config._write_config(conf, config_path)
            self.assertTrue(os.path.exists(config_path))
            config_parser.read(config_path)
            server_info = config_parser["SERVER"]
            user_info = config_parser["USER"]
            self.assertEqual("http://localhost", server_info["address"])
            self.assertEqual(5000, int(server_info["port"]))
            self.assertEqual("/api", server_info["endpoint"])
            self.assertEqual("Tigger", user_info["name"])

    @patch("os.path.exists")
    def test_create_config_fails_due_to_file_exists_and_no_force(self, path_patch):
        path_patch.return_value = True
        file_path = "test/config.ini"
        conf = config.Config(
            config.Server(
                "http://localhost",
                5000,
                "/api",
            ),
            config.User(
                "Tigger",
            ),
        )

        with self.assertRaises(config.ConfigError) as ce:
            config.create_config(config=conf, file=file_path)
        self.assertEqual(
            "Config file exists and no force arg provided", str(ce.exception)
        )

    @patch("os.path.exists")
    @patch("dokerc.config.config._write_config")
    def test_create_config_at_file_path_success(self, write_patch, path_patch):
        path_patch.return_value = False
        file_path = "test/config.ini"
        conf = config.Config(
            config.Server(
                "http://localhost",
                5000,
                "/api",
            ),
            config.User(
                "Tigger",
            ),
        )

        config.create_config(config=conf, file=file_path)

        write_patch.assert_called_once_with(config=conf, file=file_path)

    @patch("os.path.exists")
    @patch("dokerc.config.config._write_config")
    def test_create_config_at_default_file_path_success(self, write_patch, path_patch):
        path_patch.return_value = False
        file_path = os.path.join(
            pathlib.Path.home(),
            config.DEFAULT_CONFIG_LOCATION,
            config.DEFAULT_CONFIG_NAME,
        )
        conf = config.Config(
            config.Server(
                "http://localhost",
                5000,
                "/api",
            ),
            config.User(
                "Tigger",
            ),
        )

        config.create_config(config=conf)

        write_patch.assert_called_once_with(config=conf, file=file_path)

    @patch("os.path.exists")
    @patch("dokerc.config.config._write_config")
    def test_create_config_at_file_path_with_force_success(
        self, write_patch, path_patch
    ):
        path_patch.return_value = True
        file_path = "test/config.ini"
        conf = config.Config(
            config.Server(
                "http://localhost",
                5000,
                "/api",
            ),
            config.User(
                "Tigger",
            ),
        )

        config.create_config(config=conf, file=file_path, force=True)

        write_patch.assert_called_once_with(config=conf, file=file_path)