"""Test-driven development: model versioning and registry."""
import pytest

from src.aiml.protein_lm import ModelRegistry, ProteinLanguageModel


class TestModelVersioning:
    """Test ProteinLanguageModel version field and methods."""

    def test_default_version(self):
        """Default model should have version '1.0.0'."""
        model = ProteinLanguageModel()
        assert model.version == "1.0.0"

    def test_get_version_returns_string(self):
        """get_version() should return a string."""
        model = ProteinLanguageModel()
        result = model.get_version()
        assert isinstance(result, str)
        assert result == "1.0.0"

    def test_set_version_updates_version(self):
        """set_version() should update the version."""
        model = ProteinLanguageModel()
        model.set_version("2.0.0")
        assert model.version == "2.0.0"
        assert model.get_version() == "2.0.0"

    def test_set_version_multiple_times(self):
        """set_version() should work multiple times."""
        model = ProteinLanguageModel()
        model.set_version("2.0.0")
        model.set_version("3.0.0")
        assert model.get_version() == "3.0.0"


class TestModelRegistry:
    """Test ModelRegistry class."""

    def test_register_adds_model(self):
        """register() should add a model to the registry."""
        registry = ModelRegistry()
        model = ProteinLanguageModel(name="test-model")
        registry.register("test-model", model)
        assert "test-model" in registry.list_models()

    def test_get_returns_model(self):
        """get() should return the registered model."""
        registry = ModelRegistry()
        model = ProteinLanguageModel(name="test-model")
        registry.register("test-model", model)
        result = registry.get("test-model")
        assert result is model

    def test_list_models_returns_list(self):
        """list_models() should return a list of names."""
        registry = ModelRegistry()
        model1 = ProteinLanguageModel(name="model-a")
        model2 = ProteinLanguageModel(name="model-b")
        registry.register("model-a", model1)
        registry.register("model-b", model2)
        result = registry.list_models()
        assert isinstance(result, list)
        assert "model-a" in result
        assert "model-b" in result

    def test_remove_removes_model(self):
        """remove() should remove a model from the registry."""
        registry = ModelRegistry()
        model = ProteinLanguageModel(name="test-model")
        registry.register("test-model", model)
        registry.remove("test-model")
        assert "test-model" not in registry.list_models()

    def test_get_invalid_name_raises_value_error(self):
        """get() with invalid name should raise ValueError."""
        registry = ModelRegistry()
        with pytest.raises(ValueError):
            registry.get("nonexistent-model")

    def test_remove_invalid_name_raises_value_error(self):
        """remove() with invalid name should raise ValueError."""
        registry = ModelRegistry()
        with pytest.raises(ValueError):
            registry.remove("nonexistent-model")

    def test_list_models_empty(self):
        """list_models() on empty registry should return empty list."""
        registry = ModelRegistry()
        assert registry.list_models() == []
