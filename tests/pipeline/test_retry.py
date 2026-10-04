"""TDD tests for pipeline step retry logic."""
import time

from src.pipeline.pipeline import Pipeline, PipelineStep


class TestRetryDefaults:
    def test_retry_count_defaults_to_zero(self):
        step = PipelineStep(name="s", func=lambda x: x)
        assert step.retry_count == 0

    def test_retry_delay_defaults_to_zero(self):
        step = PipelineStep(name="s", func=lambda x: x)
        assert step.retry_delay == 0.0


class TestRetryFailures:
    def test_retry_count_zero_fails_immediately(self):
        attempts = []

        def always_fail(x):
            attempts.append(1)
            raise ValueError("boom")

        step = PipelineStep(name="fail", func=always_fail, retry_count=0)
        try:
            step.execute(1)
            assert False, "Should have raised"
        except ValueError:
            pass
        assert len(attempts) == 1

    def test_retry_count_three_retries_three_times(self):
        attempts = []

        def always_fail(x):
            attempts.append(1)
            raise ValueError("boom")

        step = PipelineStep(name="fail", func=always_fail, retry_count=3)
        try:
            step.execute(1)
            assert False, "Should have raised"
        except ValueError:
            pass
        # 1 initial + 3 retries = 4 total attempts
        assert len(attempts) == 4

    def test_retry_reraises_original_exception(self):
        def always_fail(x):
            raise RuntimeError("original error")

        step = PipelineStep(name="fail", func=always_fail, retry_count=2)
        try:
            step.execute(1)
            assert False, "Should have raised"
        except RuntimeError as e:
            assert str(e) == "original error"


class TestRetrySuccess:
    def test_succeeds_first_try_no_retries(self):
        attempts = []

        def succeed(x):
            attempts.append(1)
            return x * 2

        step = PipelineStep(name="ok", func=succeed, retry_count=3)
        result = step.execute(5)
        assert result == 10
        assert len(attempts) == 1

    def test_succeeds_on_second_try(self):
        attempts = []

        def fail_once(x):
            attempts.append(1)
            if len(attempts) == 1:
                raise ValueError("first attempt fails")
            return x + 100

        step = PipelineStep(name="flaky", func=fail_once, retry_count=3)
        result = step.execute(5)
        assert result == 105
        assert len(attempts) == 2

    def test_succeeds_on_last_retry(self):
        attempts = []

        def fail_twice(x):
            attempts.append(1)
            if len(attempts) < 3:
                raise ValueError("not yet")
            return "success"

        step = PipelineStep(name="flaky", func=fail_twice, retry_count=3)
        result = step.execute(1)
        assert result == "success"
        assert len(attempts) == 3


class TestRetryDelay:
    def test_retry_delay_is_respected(self):
        attempts = []

        def always_fail(x):
            attempts.append(1)
            raise ValueError("boom")

        step = PipelineStep(
            name="slow", func=always_fail, retry_count=2, retry_delay=0.05
        )
        start = time.monotonic()
        try:
            step.execute(1)
        except ValueError:
            pass
        elapsed = time.monotonic() - start
        # 2 retries with 0.05s delay each = at least 0.1s
        assert elapsed >= 0.09  # small tolerance for timing

    def test_no_delay_when_retry_delay_is_zero(self):
        attempts = []

        def always_fail(x):
            attempts.append(1)
            raise ValueError("boom")

        step = PipelineStep(
            name="fast", func=always_fail, retry_count=2, retry_delay=0.0
        )
        start = time.monotonic()
        try:
            step.execute(1)
        except ValueError:
            pass
        elapsed = time.monotonic() - start
        assert elapsed < 0.5  # should be near-instant


class TestPipelineRetryTracking:
    def test_pipeline_result_has_retries_used(self):
        p = Pipeline("test")
        p.add_step(PipelineStep("s1", lambda x: x + 1))
        result = p.run(5)
        assert hasattr(result, "retries_used")
        assert result.retries_used == {"s1": 0}

    def test_pipeline_tracks_retries_per_step(self):
        call_counts = {"a": 0, "b": 0}

        def flaky_a(x):
            call_counts["a"] += 1
            if call_counts["a"] == 1:
                raise ValueError("a fails once")
            return x + 1

        def flaky_b(x):
            call_counts["b"] += 1
            if call_counts["b"] <= 2:
                raise ValueError("b fails twice")
            return x * 2

        p = Pipeline("test")
        p.add_step(PipelineStep("a", flaky_a, retry_count=3))
        p.add_step(PipelineStep("b", flaky_b, retry_count=3))
        result = p.run(5)
        assert result.output == 12  # (5+1)*2
        assert result.retries_used == {"a": 1, "b": 2}

    def test_pipeline_retries_used_on_error(self):
        def always_fail(x):
            raise ValueError("boom")

        p = Pipeline("test")
        p.add_step(PipelineStep("ok", lambda x: x + 1))
        p.add_step(PipelineStep("fail", always_fail, retry_count=2))
        result = p.run(5)
        assert result.error is not None
        assert result.retries_used == {"ok": 0, "fail": 2}

    def test_pipeline_no_retries_on_success(self):
        p = Pipeline("test")
        p.add_step(PipelineStep("s1", lambda x: x + 1))
        p.add_step(PipelineStep("s2", lambda x: x * 2))
        result = p.run(5)
        assert result.output == 12
        assert result.retries_used == {"s1": 0, "s2": 0}
