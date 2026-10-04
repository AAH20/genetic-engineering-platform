"""TDD tests for pipeline metrics and observability."""
import time

from src.pipeline.pipeline import Pipeline, PipelineResult, PipelineStep


class TestPipelineResultDurationMs:
    def test_result_has_duration_ms_field(self):
        r = PipelineResult()
        assert hasattr(r, "duration_ms")
        assert r.duration_ms == 0.0

    def test_result_duration_ms_explicit(self):
        r = PipelineResult(output=42, duration_ms=15.0)
        assert r.duration_ms == 15.0


class TestPipelineRunDuration:
    def test_run_sets_duration_ms(self):
        p = Pipeline("test")
        p.add_step(PipelineStep("s1", lambda x: x + 1))
        result = p.run(5)
        assert result.duration_ms > 0.0

    def test_run_duration_ms_measures_elapsed_time(self):
        p = Pipeline("slow")
        p.add_step(PipelineStep("slow", lambda x: time.sleep(0.01)))
        result = p.run(0)
        assert result.duration_ms >= 1.0  # at least 1ms for 10ms sleep


class TestPipelineGetMetrics:
    def test_get_metrics_returns_dict_with_required_keys(self):
        p = Pipeline("test")
        p.add_step(PipelineStep("s1", lambda x: x + 1))
        metrics = p.get_metrics()
        assert isinstance(metrics, dict)
        assert "total_steps" in metrics
        assert "successful_steps" in metrics
        assert "failed_steps" in metrics
        assert "duration_ms" in metrics

    def test_get_metrics_after_run_correct_counts(self):
        p = Pipeline("test")
        p.add_step(PipelineStep("s1", lambda x: x + 1))
        p.add_step(PipelineStep("s2", lambda x: x * 2))
        p.run(5)
        metrics = p.get_metrics()
        assert metrics["total_steps"] == 2
        assert metrics["successful_steps"] == 2
        assert metrics["failed_steps"] == 0
        assert metrics["duration_ms"] > 0.0

    def test_get_metrics_tracks_failed_steps(self):
        p = Pipeline("test")
        p.add_step(PipelineStep("s1", lambda x: x + 1))
        p.add_step(PipelineStep("s2", lambda x: 1 / 0))
        p.run(5)
        metrics = p.get_metrics()
        assert metrics["total_steps"] == 2
        assert metrics["successful_steps"] == 1
        assert metrics["failed_steps"] == 1


class TestPipelineResetMetrics:
    def test_reset_metrics_resets_all_metrics(self):
        p = Pipeline("test")
        p.add_step(PipelineStep("s1", lambda x: x + 1))
        p.run(5)
        p.reset_metrics()
        metrics = p.get_metrics()
        assert metrics["total_steps"] == 0
        assert metrics["successful_steps"] == 0
        assert metrics["failed_steps"] == 0
        assert metrics["duration_ms"] == 0.0

    def test_get_metrics_after_run_after_reset(self):
        p = Pipeline("test")
        p.add_step(PipelineStep("s1", lambda x: x + 1))
        p.run(5)
        p.reset_metrics()
        p.run(10)
        metrics = p.get_metrics()
        assert metrics["total_steps"] == 1
        assert metrics["successful_steps"] == 1
        assert metrics["failed_steps"] == 0
