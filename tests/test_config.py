"""Tests for configuration management."""

import tempfile
from pathlib import Path

import pytest

from claude_pocketflow_template.config import Config


class TestConfigBasics:
    """Test basic configuration functionality."""

    def test_config_with_required_fields(self):
        """Test config creation with only required fields."""
        config = Config(anthropic_api_key="test_key")
        assert config.anthropic_api_key == "test_key"

    def test_config_defaults(self):
        """Test default configuration values."""
        config = Config(anthropic_api_key="test_key")
        assert config.debug is False
        assert config.log_level == "INFO"
        assert config.flow_timeout == 300
        assert config.max_retries == 3
        assert config.data_dir == Path("data")
        assert config.logs_dir == Path("logs")

    def test_config_custom_values(self):
        """Test config with custom values."""
        config = Config(
            anthropic_api_key="custom_key",
            debug=True,
            log_level="DEBUG",
            flow_timeout=600,
            max_retries=5,
            data_dir=Path("/custom/data"),
            logs_dir=Path("/custom/logs"),
        )
        assert config.anthropic_api_key == "custom_key"
        assert config.debug is True
        assert config.log_level == "DEBUG"
        assert config.flow_timeout == 600
        assert config.max_retries == 5
        assert config.data_dir == Path("/custom/data")
        assert config.logs_dir == Path("/custom/logs")


class TestConfigEnvironment:
    """Test configuration from environment variables."""

    def test_config_from_env_vars(self, monkeypatch):
        """Test loading config from environment variables."""
        monkeypatch.setenv("ANTHROPIC_API_KEY", "env_key")
        monkeypatch.setenv("DEBUG", "true")
        monkeypatch.setenv("LOG_LEVEL", "WARNING")
        monkeypatch.setenv("FLOW_TIMEOUT", "900")
        monkeypatch.setenv("MAX_RETRIES", "10")
        monkeypatch.setenv("DATA_DIR", "/env/data")
        monkeypatch.setenv("LOGS_DIR", "/env/logs")

        config = Config()
        assert config.anthropic_api_key == "env_key"
        assert config.debug is True
        assert config.log_level == "WARNING"
        assert config.flow_timeout == 900
        assert config.max_retries == 10
        assert config.data_dir == Path("/env/data")
        assert config.logs_dir == Path("/env/logs")

    def test_config_env_override(self, monkeypatch):
        """Test that constructor args override environment variables."""
        monkeypatch.setenv("ANTHROPIC_API_KEY", "env_key")
        monkeypatch.setenv("DEBUG", "true")

        config = Config(anthropic_api_key="override_key", debug=False)
        assert config.anthropic_api_key == "override_key"
        assert config.debug is False

    def test_config_boolean_parsing(self, monkeypatch):
        """Test boolean environment variable parsing."""
        test_cases = [
            ("true", True),
            ("True", True),
            ("TRUE", True),
            ("1", True),
            ("false", False),
            ("False", False),
            ("FALSE", False),
            ("0", False),
            ("", False),
        ]

        for env_value, expected in test_cases:
            monkeypatch.setenv("ANTHROPIC_API_KEY", "test")
            monkeypatch.setenv("DEBUG", env_value)
            config = Config()
            assert config.debug is expected


class TestConfigValidation:
    """Test configuration validation."""

    def test_missing_api_key_raises_error(self):
        """Test that missing API key raises validation error."""
        with pytest.raises(ValueError):
            Config()

    def test_empty_api_key_raises_error(self, monkeypatch):
        """Test that empty API key raises validation error."""
        monkeypatch.setenv("ANTHROPIC_API_KEY", "")
        with pytest.raises(ValueError):
            Config()

    def test_invalid_log_level(self):
        """Test handling of invalid log level."""
        # This should not raise an error, but log level should be accepted as-is
        config = Config(anthropic_api_key="test", log_level="INVALID")
        assert config.log_level == "INVALID"

    def test_negative_timeout(self):
        """Test handling of negative timeout."""
        config = Config(anthropic_api_key="test", flow_timeout=-1)
        assert (
            config.flow_timeout == -1
        )  # Should accept but may be handled by application logic

    def test_negative_retries(self):
        """Test handling of negative retries."""
        config = Config(anthropic_api_key="test", max_retries=-1)
        assert config.max_retries == -1


class TestConfigDirectories:
    """Test directory creation and management."""

    def test_directory_creation(self):
        """Test that directories are created automatically."""
        with tempfile.TemporaryDirectory() as temp_dir:
            data_dir = Path(temp_dir) / "test_data"
            logs_dir = Path(temp_dir) / "test_logs"

            Config(
                anthropic_api_key="test",
                data_dir=data_dir,
                logs_dir=logs_dir,
            )

            # Directories should be created after config initialization
            assert data_dir.exists()
            assert logs_dir.exists()
            assert data_dir.is_dir()
            assert logs_dir.is_dir()

    def test_nested_directory_creation(self):
        """Test creation of nested directories."""
        with tempfile.TemporaryDirectory() as temp_dir:
            nested_data = Path(temp_dir) / "deep" / "nested" / "data"
            nested_logs = Path(temp_dir) / "deep" / "nested" / "logs"

            Config(
                anthropic_api_key="test",
                data_dir=nested_data,
                logs_dir=nested_logs,
            )

            assert nested_data.exists()
            assert nested_logs.exists()

    def test_existing_directories(self):
        """Test behavior with existing directories."""
        with tempfile.TemporaryDirectory() as temp_dir:
            data_dir = Path(temp_dir) / "existing_data"
            logs_dir = Path(temp_dir) / "existing_logs"

            # Create directories beforehand
            data_dir.mkdir()
            logs_dir.mkdir()

            Config(
                anthropic_api_key="test",
                data_dir=data_dir,
                logs_dir=logs_dir,
            )

            # Should not raise an error
            assert data_dir.exists()
            assert logs_dir.exists()


class TestConfigSerialization:
    """Test configuration serialization and representation."""

    def test_config_repr(self):
        """Test config string representation."""
        config = Config(anthropic_api_key="test_key")
        repr_str = repr(config)
        assert "Config" in repr_str
        # API key should not be in repr for security
        assert "test_key" not in repr_str

    def test_config_dict(self):
        """Test converting config to dictionary."""
        config = Config(
            anthropic_api_key="test_key",
            debug=True,
            log_level="DEBUG",
        )
        config_dict = config.dict()
        assert config_dict["anthropic_api_key"] == "test_key"
        assert config_dict["debug"] is True
        assert config_dict["log_level"] == "DEBUG"

    def test_config_dict_exclude_secrets(self):
        """Test excluding secrets from dictionary representation."""
        config = Config(anthropic_api_key="secret_key")
        config_dict = config.dict(exclude={"anthropic_api_key"})
        assert "anthropic_api_key" not in config_dict
        assert "debug" in config_dict


class TestConfigEdgeCases:
    """Test edge cases and unusual scenarios."""

    def test_config_with_path_objects(self):
        """Test config with Path objects."""
        data_path = Path("/some/data/path")
        logs_path = Path("/some/logs/path")

        config = Config(
            anthropic_api_key="test",
            data_dir=data_path,
            logs_dir=logs_path,
        )

        assert config.data_dir == data_path
        assert config.logs_dir == logs_path
        assert isinstance(config.data_dir, Path)
        assert isinstance(config.logs_dir, Path)

    def test_config_with_string_paths(self):
        """Test config with string paths."""
        config = Config(
            anthropic_api_key="test",
            data_dir="/string/data/path",
            logs_dir="/string/logs/path",
        )

        assert config.data_dir == Path("/string/data/path")
        assert config.logs_dir == Path("/string/logs/path")
        assert isinstance(config.data_dir, Path)
        assert isinstance(config.logs_dir, Path)

    def test_config_case_sensitivity(self, monkeypatch):
        """Test case sensitivity of environment variables."""
        # Set environment variables with different cases
        monkeypatch.setenv("anthropic_api_key", "lowercase")
        monkeypatch.setenv("ANTHROPIC_API_KEY", "uppercase")

        config = Config()
        # Should use the uppercase version (exact match)
        assert config.anthropic_api_key == "uppercase"

    def test_config_unicode_values(self):
        """Test config with unicode values."""
        config = Config(
            anthropic_api_key="test_🔑",
            data_dir="data_📁",
            logs_dir="logs_📝",
        )

        assert config.anthropic_api_key == "test_🔑"
        assert str(config.data_dir) == "data_📁"
        assert str(config.logs_dir) == "logs_📝"
