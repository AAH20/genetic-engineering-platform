"""Tests for BiosecurityGate callback mechanism."""

from src.biosecurity.screening import BiosecurityGate


class TestAddCallback:
    def test_add_callback_adds_to_list(self):
        gate = BiosecurityGate()

        def my_callback(seq, reason):
            pass

        gate.add_callback(my_callback)
        assert len(gate._callbacks) == 1

    def test_add_callback_appends(self):
        gate = BiosecurityGate()

        def cb1(seq, reason):
            pass

        def cb2(seq, reason):
            pass

        gate.add_callback(cb1)
        gate.add_callback(cb2)
        assert len(gate._callbacks) == 2


class TestClearCallbacks:
    def test_clear_callbacks_empties_list(self):
        gate = BiosecurityGate()

        def my_callback(seq, reason):
            pass

        gate.add_callback(my_callback)
        assert len(gate._callbacks) == 1
        gate.clear_callbacks()
        assert len(gate._callbacks) == 0


class TestEvaluateCallbacks:
    THREAT_SEQUENCE = "ATCGAGCTGCTGGACTTCGCT"  # anthrax_lethal_factor

    def test_evaluate_calls_callback_on_failure(self):
        gate = BiosecurityGate()
        called = []

        def on_fail(seq, reason):
            called.append((seq, reason))

        gate.add_callback(on_fail)
        gate.evaluate(self.THREAT_SEQUENCE)
        assert len(called) == 1

    def test_evaluate_does_not_call_callback_on_success(self):
        gate = BiosecurityGate()
        called = []

        def on_fail(seq, reason):
            called.append((seq, reason))

        gate.add_callback(on_fail)
        gate.evaluate("ATGCATGCATGCATGCATGC")
        assert len(called) == 0

    def test_multiple_callbacks_all_called(self):
        gate = BiosecurityGate()
        calls_1 = []
        calls_2 = []

        def cb1(seq, reason):
            calls_1.append(seq)

        def cb2(seq, reason):
            calls_2.append(reason)

        gate.add_callback(cb1)
        gate.add_callback(cb2)
        gate.evaluate(self.THREAT_SEQUENCE)
        assert len(calls_1) == 1
        assert len(calls_2) == 1

    def test_callback_receives_correct_arguments(self):
        gate = BiosecurityGate()
        received = []

        def capture(seq, reason):
            received.append((seq, reason))

        gate.add_callback(capture)
        gate.evaluate(self.THREAT_SEQUENCE)
        assert received[0][0] == self.THREAT_SEQUENCE
        assert isinstance(received[0][1], str)
        assert len(received[0][1]) > 0
