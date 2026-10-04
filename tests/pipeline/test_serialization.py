"""TDD tests for pipeline serialization."""
import json

from src.pipeline.pipeline import Pipeline, PipelineStep


class TestPipelineStepToDict:
    def test_to_dict_returns_correct_structure(self):
        step = PipelineStep(
            name="test_step",
            func=lambda x: x * 2,
            metadata={"author": "test", "version": 1},
        )
        result = step.to_dict()
        assert result == {
            "name": "test_step",
            "metadata": {"author": "test", "version": 1},
        }

    def test_to_dict_with_empty_metadata(self):
        step = PipelineStep(name="test", func=lambda x: x)
        result = step.to_dict()
        assert result == {"name": "test", "metadata": {}}


class TestPipelineToDict:
    def test_to_dict_returns_correct_structure(self):
        p = Pipeline("test_pipeline", description="A test pipeline")
        p.add_step(PipelineStep("s1", lambda x: x + 1, metadata={"order": 1}))
        p.add_step(PipelineStep("s2", lambda x: x * 2, metadata={"order": 2}))

        result = p.to_dict()
        assert result["name"] == "test_pipeline"
        assert result["description"] == "A test pipeline"
        assert len(result["steps"]) == 2
        assert result["steps"][0]["name"] == "s1"
        assert result["steps"][0]["metadata"] == {"order": 1}
        assert result["steps"][1]["name"] == "s2"
        assert result["steps"][1]["metadata"] == {"order": 2}

    def test_to_dict_empty_pipeline(self):
        p = Pipeline("empty")
        result = p.to_dict()
        assert result == {"name": "empty", "description": "", "steps": []}


class TestPipelineFromDict:
    def test_from_dict_reconstructs_pipeline(self):
        data = {
            "name": "test_pipeline",
            "description": "A test pipeline",
            "steps": [
                {"name": "s1", "metadata": {"order": 1}},
                {"name": "s2", "metadata": {"order": 2}},
            ],
        }
        p = Pipeline.from_dict(data)
        assert p.name == "test_pipeline"
        assert p.description == "A test pipeline"
        assert len(p.steps) == 2
        assert p.steps[0].name == "s1"
        assert p.steps[0].metadata == {"order": 1}
        assert p.steps[1].name == "s2"
        assert p.steps[1].metadata == {"order": 2}

    def test_from_dict_with_empty_steps(self):
        data = {"name": "empty", "description": "", "steps": []}
        p = Pipeline.from_dict(data)
        assert p.name == "empty"
        assert p.steps == []


class TestPipelineRoundtrip:
    def test_roundtrip_preserves_data(self):
        p = Pipeline("roundtrip_test", description="Testing roundtrip")
        p.add_step(PipelineStep("s1", lambda x: x + 1, metadata={"order": 1}))
        p.add_step(PipelineStep("s2", lambda x: x * 2, metadata={"order": 2}))

        data = p.to_dict()
        p2 = Pipeline.from_dict(data)

        assert p2.name == p.name
        assert p2.description == p.description
        assert len(p2.steps) == len(p.steps)
        for s1, s2 in zip(p.steps, p2.steps):
            assert s1.name == s2.name
            assert s1.metadata == s2.metadata


class TestPipelineJson:
    def test_to_json_returns_valid_json_string(self):
        p = Pipeline("json_test", description="JSON test")
        p.add_step(PipelineStep("s1", lambda x: x + 1, metadata={"order": 1}))

        json_str = p.to_json()
        assert isinstance(json_str, str)
        parsed = json.loads(json_str)
        assert parsed["name"] == "json_test"
        assert parsed["description"] == "JSON test"
        assert len(parsed["steps"]) == 1

    def test_from_json_reconstructs_pipeline(self):
        p = Pipeline("json_test", description="JSON test")
        p.add_step(PipelineStep("s1", lambda x: x + 1, metadata={"order": 1}))

        json_str = p.to_json()
        p2 = Pipeline.from_json(json_str)

        assert p2.name == p.name
        assert p2.description == p.description
        assert len(p2.steps) == len(p.steps)
        assert p2.steps[0].name == p.steps[0].name
        assert p2.steps[0].metadata == p.steps[0].metadata

    def test_json_roundtrip(self):
        p = Pipeline("json_roundtrip", description="JSON roundtrip test")
        p.add_step(PipelineStep("s1", lambda x: x + 1, metadata={"order": 1}))
        p.add_step(PipelineStep("s2", lambda x: x * 2, metadata={"order": 2}))

        json_str = p.to_json()
        p2 = Pipeline.from_json(json_str)

        assert p2.name == p.name
        assert p2.description == p.description
        assert len(p2.steps) == len(p.steps)
        for s1, s2 in zip(p.steps, p2.steps):
            assert s1.name == s2.name
            assert s1.metadata == s2.metadata
