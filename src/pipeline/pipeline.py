"""Unified pipeline module for composing multi-step workflows.

Provides a declarative way to chain processing steps with error handling,
context propagation, and intermediate result tracing.
"""

from __future__ import annotations

import inspect
import json
import time
from concurrent.futures import ThreadPoolExecutor
from dataclasses import dataclass, field
from typing import Any, Callable, Optional


@dataclass
class PipelineStep:
    """A single processing step in a pipeline.

    Attributes:
        name: Human-readable step identifier.
        func: Callable that transforms the input (and optionally context).
        metadata: Arbitrary key-value metadata for the step.
        retry_count: Number of times to retry on failure (default 0).
        retry_delay: Seconds to wait between retries (default 0.0).
    """

    name: str
    func: Callable[..., Any]
    metadata: dict[str, Any] = field(default_factory=dict)
    retry_count: int = 0
    retry_delay: float = 0.0
    retries_used: int = 0

    def to_dict(self) -> dict[str, Any]:
        return {"name": self.name, "metadata": self.metadata}

    def execute(self, value: Any, context: dict[str, Any] | None = None) -> Any:
        """Execute the step with retry logic, passing context if the function accepts it."""
        import inspect
        sig = inspect.signature(self.func)
        params = list(sig.parameters.keys())
        self.retries_used = 0
        for attempt in range(self.retry_count + 1):
            try:
                if len(params) >= 2:
                    return self.func(value, context)
                return self.func(value)
            except Exception:
                if attempt < self.retry_count:
                    self.retries_used += 1
                    if self.retry_delay > 0:
                        time.sleep(self.retry_delay)
                else:
                    raise
        return None  # unreachable


@dataclass
class AsyncPipelineStep:
    """An async processing step in a pipeline.

    Wraps an async (or sync) function and executes it asynchronously.

    Attributes:
        name: Human-readable step identifier.
        func: Async callable that transforms the input (and optionally context).
        metadata: Arbitrary key-value metadata for the step.
    """

    name: str
    func: Callable[..., Any]
    metadata: dict[str, Any] = field(default_factory=dict)

    async def execute(self, value: Any, context: dict[str, Any] | None = None) -> Any:
        """Execute the async step, passing context if the function accepts it."""
        sig = inspect.signature(self.func)
        params = list(sig.parameters.keys())
        if len(params) >= 2:
            result = self.func(value, context)
        else:
            result = self.func(value)
        if inspect.isawaitable(result):
            result = await result
        return result


@dataclass
class ConditionalStep(PipelineStep):
    """A step that branches based on a predicate.

    Attributes:
        predicate: Callable(value, context) -> bool that selects the branch.
        if_true: PipelineStep executed when predicate returns True.
        if_false: PipelineStep executed when predicate returns False.
    """

    name: str = "conditional"
    func: Callable[..., Any] = field(default=lambda v, ctx: None)
    predicate: Callable[..., bool] = field(default=lambda v, ctx: True)
    if_true: Optional[PipelineStep] = None
    if_false: Optional[PipelineStep] = None

    def __post_init__(self) -> None:
        self.func = lambda v, ctx: self._branch(v, ctx)

    def _branch(self, value: Any, context: dict[str, Any] | None = None) -> Any:
        if self.predicate(value, context):
            return self.if_true.execute(value, context)
        return self.if_false.execute(value, context)

    def execute(self, value: Any, context: dict[str, Any] | None = None) -> Any:
        """Evaluate predicate and run the appropriate branch."""
        return self._branch(value, context)


@dataclass
class ParallelStep:
    """A step that runs multiple PipelineSteps concurrently.

    Attributes:
        name: Human-readable step identifier.
        steps: List of PipelineStep to execute in parallel.
    """

    name: str
    steps: list[PipelineStep]

    def execute(self, value: Any, context: dict[str, Any] | None = None) -> list[Any]:
        """Execute all steps in parallel using ThreadPoolExecutor.

        Returns:
            List of results from each step, in the same order as the input steps.
        """
        with ThreadPoolExecutor() as executor:
            futures = [
                executor.submit(step.execute, value, context)
                for step in self.steps
            ]
            return [f.result() for f in futures]


@dataclass
class PipelineResult:
    """Result of running a pipeline.

    Attributes:
        output: Final output value (None if pipeline errored).
        steps_run: Number of steps successfully executed.
        intermediate: List of intermediate values after each step.
        error: Error message if pipeline failed, None otherwise.
        retries_used: Dict mapping step name to number of retries used.
        errors: List of all errors collected (used by run_continue_on_error).
        duration_ms: Execution time in milliseconds.
    """

    output: Any = None
    steps_run: int = 0
    intermediate: list[Any] = field(default_factory=list)
    error: Optional[str] = None
    retries_used: dict[str, int] = field(default_factory=dict)
    errors: list[str] = field(default_factory=list)
    duration_ms: float = 0.0


class Pipeline:
    """A composable pipeline of processing steps.

    Usage:
        p = Pipeline("my_pipeline")
        p.add_step(PipelineStep("double", lambda x: x * 2))
        result = p.run(5)
        assert result.output == 10
    """

    def __init__(self, name: str, description: str = "") -> None:
        self.name = name
        self.description = description
        self.steps: list[Any] = []
        self._total_steps: int = 0
        self._successful_steps: int = 0
        self._failed_steps: int = 0
        self._duration_ms: float = 0.0

    def add_step(self, step: PipelineStep) -> Pipeline:
        """Add a step and return self for chaining."""
        self.steps.append(step)
        return self

    def insert_step(self, step: PipelineStep, index: int) -> Pipeline:
        """Insert a step at the given index and return self for chaining."""
        if index < 0 or index > len(self.steps):
            raise IndexError(
                f"Index {index} out of range for pipeline with {len(self.steps)} steps"
            )
        self.steps.insert(index, step)
        return self

    def remove_step(self, step_name: str) -> Pipeline:
        """Remove a step by name and return self for chaining."""
        for i, s in enumerate(self.steps):
            if s.name == step_name:
                self.steps.pop(i)
                return self
        raise ValueError(f"Step '{step_name}' not found in pipeline")

    def replace_step(self, step_name: str, new_step: PipelineStep) -> Pipeline:
        """Replace a step by name and return self for chaining."""
        for i, s in enumerate(self.steps):
            if s.name == step_name:
                self.steps[i] = new_step
                return self
        raise ValueError(f"Step '{step_name}' not found in pipeline")

    def get_step(self, step_name: str) -> PipelineStep:
        """Return the step with the given name."""
        for s in self.steps:
            if s.name == step_name:
                return s
        raise ValueError(f"Step '{step_name}' not found in pipeline")

    def add_conditional_step(
        self,
        predicate: Callable[..., bool],
        if_true: PipelineStep,
        if_false: PipelineStep,
    ) -> Pipeline:
        """Add a conditional branching step and return self for chaining."""
        self.steps.append(
            ConditionalStep(
                name="conditional",
                predicate=predicate,
                if_true=if_true,
                if_false=if_false,
            )
        )
        return self

    def add_parallel_step(self, step: ParallelStep) -> Pipeline:
        """Add a parallel step and return self for chaining."""
        self.steps.append(step)
        return self

    def compose(self, other: Pipeline) -> Pipeline:
        """Compose two pipelines into one, appending other's steps.

        Returns a new Pipeline with all steps from both. Does not modify
        either original pipeline.
        """
        import copy

        result = Pipeline(self.name, self.description)
        result.steps = copy.deepcopy(self.steps) + copy.deepcopy(other.steps)
        return result

    def split(self, step_name: str) -> tuple[Pipeline, Pipeline]:
        """Split pipeline at a named step.

        Returns a tuple of (before, after) pipelines. The step itself is
        excluded from both. Raises ValueError if step_name is not found.
        """
        import copy

        idx = None
        for i, step in enumerate(self.steps):
            if step.name == step_name:
                idx = i
                break

        if idx is None:
            raise ValueError(f"Step '{step_name}' not found in pipeline")

        before = Pipeline(self.name, self.description)
        before.steps = copy.deepcopy(self.steps[:idx])

        after = Pipeline(self.name, self.description)
        after.steps = copy.deepcopy(self.steps[idx + 1:])

        return before, after

    def clone(self) -> Pipeline:
        """Create a deep copy of the pipeline.

        Returns a new Pipeline with deep-copied steps. Modifications to the
        clone do not affect the original.
        """
        import copy

        result = Pipeline(self.name, self.description)
        result.steps = copy.deepcopy(self.steps)
        return result

    def to_dict(self) -> dict[str, Any]:
        return {
            "name": self.name,
            "description": self.description,
            "steps": [step.to_dict() for step in self.steps],
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> Pipeline:
        p = cls(name=data["name"], description=data.get("description", ""))
        for step_data in data.get("steps", []):
            p.add_step(PipelineStep(
                name=step_data["name"],
                func=lambda x: x,
                metadata=step_data.get("metadata", {}),
            ))
        return p

    def to_json(self) -> str:
        return json.dumps(self.to_dict())

    @classmethod
    def from_json(cls, json_str: str) -> Pipeline:
        return cls.from_dict(json.loads(json_str))

    def run(self, initial_value: Any, context: dict[str, Any] | None = None) -> PipelineResult:
        """Execute all steps in order, threading output through.

        Stops on first error and returns the error in PipelineResult.
        """
        start = time.perf_counter()
        value = initial_value
        intermediate: list[Any] = []
        steps_run = 0
        retries_used: dict[str, int] = {}

        for step in self.steps:
            try:
                value = step.execute(value, context)
                intermediate.append(value)
                steps_run += 1
                retries_used[step.name] = getattr(step, "retries_used", 0)
            except Exception as exc:
                retries_used[step.name] = getattr(step, "retries_used", 0)
                duration_ms = (time.perf_counter() - start) * 1000
                self._total_steps += len(self.steps)
                self._successful_steps += steps_run
                self._failed_steps += 1
                self._duration_ms += duration_ms
                return PipelineResult(
                    output=None,
                    steps_run=steps_run,
                    intermediate=intermediate,
                    error=f"{step.name}: {exc}",
                    retries_used=retries_used,
                    duration_ms=duration_ms,
                )

        duration_ms = (time.perf_counter() - start) * 1000
        self._total_steps += len(self.steps)
        self._successful_steps += steps_run
        self._duration_ms += duration_ms
        return PipelineResult(
            output=value,
            steps_run=steps_run,
            intermediate=intermediate,
            retries_used=retries_used,
            duration_ms=duration_ms,
        )

    async def run_async(
        self, initial_value: Any, context: dict[str, Any] | None = None
    ) -> PipelineResult:
        """Execute all steps in order, awaiting async steps.

        Stops on first error and returns the error in PipelineResult.
        """
        value = initial_value
        intermediate: list[Any] = []
        steps_run = 0
        retries_used: dict[str, int] = {}

        for step in self.steps:
            try:
                if isinstance(step, AsyncPipelineStep):
                    value = await step.execute(value, context)
                else:
                    value = step.execute(value, context)
                intermediate.append(value)
                steps_run += 1
                retries_used[step.name] = getattr(step, "retries_used", 0)
            except Exception as exc:
                retries_used[step.name] = getattr(step, "retries_used", 0)
                return PipelineResult(
                    output=None,
                    steps_run=steps_run,
                    intermediate=intermediate,
                    error=f"{step.name}: {exc}",
                    retries_used=retries_used,
                )

        return PipelineResult(
            output=value,
            steps_run=steps_run,
            intermediate=intermediate,
            retries_used=retries_used,
        )

    def get_metrics(self) -> dict[str, Any]:
        """Return pipeline execution metrics.

        Returns:
            Dict with total_steps, successful_steps, failed_steps, duration_ms.
        """
        return {
            "total_steps": self._total_steps,
            "successful_steps": self._successful_steps,
            "failed_steps": self._failed_steps,
            "duration_ms": self._duration_ms,
        }

    def reset_metrics(self) -> None:
        """Reset all pipeline metrics to zero."""
        self._total_steps = 0
        self._successful_steps = 0
        self._failed_steps = 0
        self._duration_ms = 0.0

    def run_continue_on_error(
        self, initial_value: Any, context: dict[str, Any] | None = None
    ) -> PipelineResult:
        """Execute all steps, collecting errors but continuing on failure.

        Returns PipelineResult with all errors in the 'errors' list.
        """
        value = initial_value
        intermediate: list[Any] = []
        steps_run = 0
        retries_used: dict[str, int] = {}
        errors: list[str] = []

        for step in self.steps:
            try:
                value = step.execute(value, context)
                intermediate.append(value)
                steps_run += 1
                retries_used[step.name] = getattr(step, "retries_used", 0)
            except Exception as exc:
                retries_used[step.name] = getattr(step, "retries_used", 0)
                errors.append(f"{step.name}: {exc}")

        return PipelineResult(
            output=value if steps_run > 0 else None,
            steps_run=steps_run,
            intermediate=intermediate,
            error=errors[0] if errors else None,
            retries_used=retries_used,
            errors=errors,
        )


def run_pipeline(
    steps: list[PipelineStep],
    initial_value: Any,
    context: dict[str, Any] | None = None,
) -> PipelineResult:
    """Convenience function: build a pipeline from steps and run it."""
    p = Pipeline("anonymous")
    for step in steps:
        p.add_step(step)
    return p.run(initial_value, context)
