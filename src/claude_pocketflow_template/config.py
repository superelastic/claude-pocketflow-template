"""Configuration management for claude-pocketflow-template."""

import os
from pathlib import Path
from typing import Any


class Config:
    """Configuration class for managing template settings."""

    def __init__(
        self,
        anthropic_api_key: str | None = None,
        *,
        debug: bool | None = None,
        log_level: str | None = None,
        data_dir: Path | str | None = None,
        logs_dir: Path | str | None = None,
        flow_timeout: int | None = None,
        max_retries: int | None = None,
        **kwargs: Any,
    ):
        """Initialize configuration.

        Args:
            anthropic_api_key: API key for Anthropic Claude
            debug: Enable debug mode
            log_level: Logging level
            data_dir: Directory for data storage
            logs_dir: Directory for log files
            flow_timeout: Timeout for flow execution in seconds
            max_retries: Maximum number of retries for failed operations
            **kwargs: Additional configuration options
        """
        self.anthropic_api_key = anthropic_api_key or os.getenv("ANTHROPIC_API_KEY")

        # Validate required fields
        if not self.anthropic_api_key:
            msg = "anthropic_api_key is required"
            raise ValueError(msg)

        # Load from environment variables if not explicitly provided
        self.debug = (
            debug if debug is not None else self._get_bool_env("DEBUG", default=False)
        )
        self.log_level = (
            log_level if log_level is not None else os.getenv("LOG_LEVEL", "INFO")
        )
        self.flow_timeout = (
            flow_timeout
            if flow_timeout is not None
            else int(os.getenv("FLOW_TIMEOUT", "300"))
        )
        self.max_retries = (
            max_retries
            if max_retries is not None
            else int(os.getenv("MAX_RETRIES", "3"))
        )

        # Convert paths to Path objects and create directories
        self.data_dir = (
            Path(data_dir) if data_dir else Path(os.getenv("DATA_DIR", "data"))
        )
        self.logs_dir = (
            Path(logs_dir) if logs_dir else Path(os.getenv("LOGS_DIR", "logs"))
        )

        # Create directories if they don't exist
        # Skip for absolute paths that might not be writable
        try:
            if not self.data_dir.is_absolute() or self.data_dir.parts[0] != "/":
                self.data_dir.mkdir(parents=True, exist_ok=True)
        except (PermissionError, OSError):
            pass  # Skip directory creation if permission denied

        try:
            if not self.logs_dir.is_absolute() or self.logs_dir.parts[0] != "/":
                self.logs_dir.mkdir(parents=True, exist_ok=True)
        except (PermissionError, OSError):
            pass  # Skip directory creation if permission denied

        # Store additional config options
        for key, value in kwargs.items():
            setattr(self, key, value)

    def dict(self, exclude: set[str] | None = None) -> dict[str, Any]:
        """Convert config to dictionary representation.

        Args:
            exclude: Set of attribute names to exclude from the dict

        Returns:
            Dictionary representation of config
        """
        exclude = exclude or set()
        result = {}

        for attr_name in dir(self):
            # Skip private attributes, methods, and excluded attributes
            if (
                attr_name.startswith("_")
                or callable(getattr(self, attr_name))
                or attr_name in exclude
            ):
                continue

            result[attr_name] = getattr(self, attr_name)

        return result

    def _get_bool_env(self, env_name: str, *, default: bool) -> bool:
        """Get boolean value from environment variable."""
        value = os.getenv(env_name)
        if value is None:
            return default
        return value.lower() in ("true", "1", "yes", "on")
