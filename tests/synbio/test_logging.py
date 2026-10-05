"""Test-driven development: CircuitLogger and circuit evaluation logging."""
import json

from src.synbio.genetic_circuits import CircuitLogger, GeneticCircuit


class TestLogEvent:
    """Test CircuitLogger.log_event adds entries to logs."""

    def test_log_event_adds_entry(self):
        """log_event should add an entry to the logs list."""
        logger = CircuitLogger()
        logger.log_event("test_event", {"key": "value"})
        assert len(logger.get_logs()) == 1

    def test_log_event_stores_type(self):
        """log_event should store the event type."""
        logger = CircuitLogger()
        logger.log_event("my_event", {"data": 123})
        logs = logger.get_logs()
        assert logs[0]["event_type"] == "my_event"

    def test_log_event_stores_data(self):
        """log_event should store the data dict."""
        logger = CircuitLogger()
        logger.log_event("my_event", {"data": 123})
        logs = logger.get_logs()
        assert logs[0]["data"] == {"data": 123}

    def test_log_event_stores_timestamp(self):
        """log_event should store a timestamp."""
        logger = CircuitLogger()
        logger.log_event("my_event", {})
        logs = logger.get_logs()
        assert "timestamp" in logs[0]


class TestGetLogs:
    """Test CircuitLogger.get_logs returns logs with optional filtering."""

    def test_get_logs_returns_all(self):
        """get_logs with no filter should return all logs."""
        logger = CircuitLogger()
        logger.log_event("event_a", {"x": 1})
        logger.log_event("event_b", {"y": 2})
        logger.log_event("event_a", {"z": 3})
        logs = logger.get_logs()
        assert len(logs) == 3

    def test_get_logs_filtered(self):
        """get_logs with event_type filter should return only matching logs."""
        logger = CircuitLogger()
        logger.log_event("event_a", {"x": 1})
        logger.log_event("event_b", {"y": 2})
        logger.log_event("event_a", {"z": 3})
        logs = logger.get_logs("event_a")
        assert len(logs) == 2
        assert all(log["event_type"] == "event_a" for log in logs)

    def test_get_logs_no_match_returns_empty(self):
        """get_logs with a filter that matches nothing should return empty list."""
        logger = CircuitLogger()
        logger.log_event("event_a", {"x": 1})
        logs = logger.get_logs("nonexistent")
        assert logs == []

    def test_get_logs_empty_returns_empty(self):
        """get_logs on a fresh logger should return empty list."""
        logger = CircuitLogger()
        assert logger.get_logs() == []


class TestClearLogs:
    """Test CircuitLogger.clear_logs empties logs."""

    def test_clear_logs_empties(self):
        """clear_logs should remove all entries."""
        logger = CircuitLogger()
        logger.log_event("event_a", {"x": 1})
        logger.log_event("event_b", {"y": 2})
        assert len(logger.get_logs()) == 2
        logger.clear_logs()
        assert logger.get_logs() == []

    def test_clear_logs_on_empty_is_noop(self):
        """clear_logs on an already-empty logger should not raise."""
        logger = CircuitLogger()
        logger.clear_logs()
        assert logger.get_logs() == []


class TestExportLogs:
    """Test CircuitLogger.export_logs writes JSON file."""

    def test_export_logs_creates_file(self, tmp_path):
        """export_logs should create a JSON file at the given path."""
        logger = CircuitLogger()
        logger.log_event("event_a", {"x": 1})
        filepath = str(tmp_path / "logs.json")
        logger.export_logs(filepath)
        with open(filepath) as f:
            data = json.load(f)
        assert len(data) == 1
        assert data[0]["event_type"] == "event_a"

    def test_export_logs_contains_all_entries(self, tmp_path):
        """export_logs should write all log entries to the file."""
        logger = CircuitLogger()
        logger.log_event("event_a", {"x": 1})
        logger.log_event("event_b", {"y": 2})
        filepath = str(tmp_path / "logs.json")
        logger.export_logs(filepath)
        with open(filepath) as f:
            data = json.load(f)
        assert len(data) == 2

    def test_export_logs_empty(self, tmp_path):
        """export_logs with no logs should write an empty JSON array."""
        logger = CircuitLogger()
        filepath = str(tmp_path / "logs.json")
        logger.export_logs(filepath)
        with open(filepath) as f:
            data = json.load(f)
        assert data == []


class TestInstanceIndependence:
    """Test that CircuitLogger instances are independent."""

    def test_instances_are_independent(self):
        """Two CircuitLogger instances should not share logs."""
        logger1 = CircuitLogger()
        logger2 = CircuitLogger()
        logger1.log_event("event_a", {"x": 1})
        assert len(logger1.get_logs()) == 1
        assert len(logger2.get_logs()) == 0

    def test_clear_does_not_affect_other_instance(self):
        """Clearing one logger should not affect another."""
        logger1 = CircuitLogger()
        logger2 = CircuitLogger()
        logger1.log_event("event_a", {"x": 1})
        logger2.log_event("event_b", {"y": 2})
        logger1.clear_logs()
        assert len(logger1.get_logs()) == 0
        assert len(logger2.get_logs()) == 1


class TestCircuitEvaluationLogging:
    """Test that GeneticCircuit.evaluate() logs 'circuit_evaluated' event."""

    def test_evaluate_logs_event(self):
        """evaluate() should log a 'circuit_evaluated' event."""
        logger = CircuitLogger()
        circuit = GeneticCircuit(
            name="TestCircuit",
            inputs=["A", "B"],
            outputs=["Y"],
        )
        circuit.add_gate("AND", ["A", "B"], "Y")
        circuit.evaluate({"A": True, "B": True}, logger=logger)
        logs = logger.get_logs("circuit_evaluated")
        assert len(logs) == 1

    def test_evaluate_log_contains_circuit_name(self):
        """The logged event should contain the circuit name."""
        logger = CircuitLogger()
        circuit = GeneticCircuit(
            name="MyCircuit",
            inputs=["A"],
            outputs=["Y"],
        )
        circuit.add_gate("NOT", ["A"], "Y")
        circuit.evaluate({"A": True}, logger=logger)
        logs = logger.get_logs("circuit_evaluated")
        assert logs[0]["data"]["circuit_name"] == "MyCircuit"

    def test_evaluate_log_contains_result(self):
        """The logged event should contain the evaluation result."""
        logger = CircuitLogger()
        circuit = GeneticCircuit(
            name="TestCircuit",
            inputs=["A", "B"],
            outputs=["Y"],
        )
        circuit.add_gate("AND", ["A", "B"], "Y")
        circuit.evaluate({"A": True, "B": False}, logger=logger)
        logs = logger.get_logs("circuit_evaluated")
        assert logs[0]["data"]["result"] == {"Y": False}

    def test_evaluate_without_logger_does_not_raise(self):
        """evaluate() without a logger should work normally."""
        circuit = GeneticCircuit(
            name="TestCircuit",
            inputs=["A", "B"],
            outputs=["Y"],
        )
        circuit.add_gate("AND", ["A", "B"], "Y")
        result = circuit.evaluate({"A": True, "B": True})
        assert result["Y"] is True
