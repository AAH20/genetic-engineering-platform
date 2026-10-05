"""Tests for Config class — strict TDD."""
import json
import os
import tempfile

from src.integration.config import Config


class TestConfigGet:
    def test_get_existing_key_returns_value(self):
        config = Config()
        assert config.get("biosecurity.framework") == "NIH"

    def test_get_missing_key_returns_default(self):
        config = Config()
        assert config.get("nonexistent.key") is None

    def test_get_missing_key_returns_custom_default(self):
        config = Config()
        assert config.get("nonexistent.key", "fallback") == "fallback"


class TestConfigSet:
    def test_set_updates_value(self):
        config = Config()
        config.set("biosecurity.framework", "FDA")
        assert config.get("biosecurity.framework") == "FDA"

    def test_set_new_key(self):
        config = Config()
        config.set("custom.key", "custom_value")
        assert config.get("custom.key") == "custom_value"


class TestConfigToDict:
    def test_to_dict_returns_correct_dict(self):
        config = Config()
        result = config.to_dict()
        assert isinstance(result, dict)
        assert result["biosecurity.framework"] == "NIH"
        assert result["pipeline.default_timeout"] == 300
        assert result["aiml.default_model"] == "kmer_bag_of_words"
        assert result["crispr.default_pam"] == "NGG"


class TestConfigFromDict:
    def test_from_dict_creates_config(self):
        data = {"test.key": "test_value", "another.key": 42}
        config = Config.from_dict(data)
        assert config.get("test.key") == "test_value"
        assert config.get("another.key") == 42

    def test_from_dict_does_not_mutate_input(self):
        data = {"test.key": "test_value"}
        Config.from_dict(data)
        assert data == {"test.key": "test_value"}


class TestConfigSaveLoad:
    def test_save_to_file_creates_json(self):
        config = Config()
        with tempfile.NamedTemporaryFile(suffix=".json", delete=False) as f:
            filepath = f.name
        try:
            config.save_to_file(filepath)
            assert os.path.exists(filepath)
            with open(filepath) as f:
                data = json.load(f)
            assert data["biosecurity.framework"] == "NIH"
            assert data["pipeline.default_timeout"] == 300
        finally:
            os.unlink(filepath)

    def test_load_from_file_loads_json(self):
        data = {"biosecurity.framework": "FDA", "custom.key": "value"}
        with tempfile.NamedTemporaryFile(
            mode="w", suffix=".json", delete=False
        ) as f:
            json.dump(data, f)
            filepath = f.name
        try:
            config = Config.load_from_file(filepath)
            assert config.get("biosecurity.framework") == "FDA"
            assert config.get("custom.key") == "value"
        finally:
            os.unlink(filepath)

    def test_save_load_roundtrip_preserves_values(self):
        config = Config()
        config.set("custom.key", "custom_value")
        config.set("numeric.key", 99)
        with tempfile.NamedTemporaryFile(suffix=".json", delete=False) as f:
            filepath = f.name
        try:
            config.save_to_file(filepath)
            loaded = Config.load_from_file(filepath)
            assert loaded.get("biosecurity.framework") == "NIH"
            assert loaded.get("pipeline.default_timeout") == 300
            assert loaded.get("aiml.default_model") == "kmer_bag_of_words"
            assert loaded.get("crispr.default_pam") == "NGG"
            assert loaded.get("custom.key") == "custom_value"
            assert loaded.get("numeric.key") == 99
        finally:
            os.unlink(filepath)
