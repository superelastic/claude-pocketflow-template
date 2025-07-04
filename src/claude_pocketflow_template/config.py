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
        debug: bool = False,
        log_level: str = "INFO",
        data_dir: Path | str | None = None,
        logs_dir: Path | str | None = None,
        flow_timeout: int = 60,
        max_retries: int = 3,
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
        self.debug = debug
        self.log_level = log_level
        self.flow_timeout = flow_timeout
        self.max_retries = max_retries

        # Convert paths to Path objects and create directories
        self.data_dir = Path(data_dir) if data_dir else Path("data")
        self.logs_dir = Path(logs_dir) if logs_dir else Path("logs")

        # Create directories if they don't exist
        self.data_dir.mkdir(parents=True, exist_ok=True)
        self.logs_dir.mkdir(parents=True, exist_ok=True)

        # Store additional config options
        for key, value in kwargs.items():
            setattr(self, key, value)

        # Validate configuration
        self._validate()

    def _validate(self) -> None:
        """Validate configuration values."""
        if self.log_level not in ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]:
            msg = f"Invalid log_level: {self.log_level}"
            raise ValueError(msg)

        if self.flow_timeout <= 0:
            msg = f"flow_timeout must be positive, got: {self.flow_timeout}"
            raise ValueError(msg)

        if self.max_retries < 0:
            msg = f"max_retries must be non-negative, got: {self.max_retries}"
            raise ValueError(msg)

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
