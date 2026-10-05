"""Configuration system for the genetic engineering platform."""
import json
from typing import Any


class Config:
    """Configuration store with JSON serialization support."""

    _DEFAULTS = {
        "biosecurity.framework": "NIH",
        "pipeline.default_timeout": 300,
        "aiml.default_model": "kmer_bag_of_words",
        "crispr.default_pam": "NGG",
    }

    def __init__(self) -> None:
        self._data: dict[str, Any] = dict(self._DEFAULTS)

    def get(self, key: str, default: Any = None) -> Any:
        """Get a configuration value, returning default if key is missing."""
        return self._data.get(key, default)

    def set(self, key: str, value: Any) -> None:
        """Set a configuration value."""
        self._data[key] = value

    def to_dict(self) -> dict:
        """Return a copy of the configuration as a dict."""
        return dict(self._data)

    @classmethod
    def from_dict(cls, data: dict) -> "Config":
        """Create a Config instance from a dict."""
        config = cls()
        config._data = dict(data)
        return config

    def save_to_file(self, filepath: str) -> None:
        """Save configuration to a JSON file."""
        with open(filepath, "w") as f:
            json.dump(self._data, f, indent=2)

    @classmethod
    def load_from_file(cls, filepath: str) -> "Config":
        """Load configuration from a JSON file."""
        with open(filepath) as f:
            data = json.load(f)
        return cls.from_dict(data)
