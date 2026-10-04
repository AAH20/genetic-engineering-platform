"""Test-driven development: Synthetic Biology genetic circuits module."""

import pytest

from src.synbio.genetic_circuits import (
    DNASynthesis,
    GeneticCircuit,
    LogicGate,
    PathwayOptimizer,
)

# ---------------------------------------------------------------------------
# GeneticCircuit – construction & metadata
# ---------------------------------------------------------------------------


class TestGeneticCircuitConstruction:
    """Test GeneticCircuit initialization and attribute storage."""

    def test_basic_attributes(self):
        """Circuit should store name, inputs, and outputs."""
        circuit = GeneticCircuit(
            name="AND_Gate",
            inputs=["A", "B"],
            outputs=["Y"],
        )
        assert circuit.name == "AND_Gate"
        assert circuit.inputs == ["A", "B"]
        assert circuit.outputs == ["Y"]
        assert circuit.gates == []

    def test_empty_circuit(self):
        """Circuit with no inputs or outputs should be constructible."""
        circuit = GeneticCircuit(name="Empty", inputs=[], outputs=[])
        assert circuit.name == "Empty"
        assert circuit.inputs == []
        assert circuit.outputs == []

    def test_multiple_outputs(self):
        """Circuit should support multiple outputs."""
        circuit = GeneticCircuit(
            name="MultiOut",
            inputs=["A", "B", "C"],
            outputs=["Y1", "Y2"],
        )
        assert len(circuit.outputs) == 2
        assert "Y1" in circuit.outputs
        assert "Y2" in circuit.outputs


# ---------------------------------------------------------------------------
# GeneticCircuit – add_gate
# ---------------------------------------------------------------------------


class TestAddGate:
    """Test adding logic gates to a circuit."""

    def test_add_single_gate(self):
        """Adding one gate should increase gate count by 1."""
        circuit = GeneticCircuit(name="Test", inputs=["A", "B"], outputs=["Y"])
        circuit.add_gate("AND", ["A", "B"], "Y")
        assert len(circuit.gates) == 1

    def test_add_multiple_gates(self):
        """Adding multiple gates should preserve order."""
        circuit = GeneticCircuit(name="Test", inputs=["A", "B"], outputs=["Y1", "Y2"])
        circuit.add_gate("AND", ["A", "B"], "Y1")
        circuit.add_gate("OR", ["A", "B"], "Y2")
        assert len(circuit.gates) == 2

    def test_gate_stores_type_inputs_output(self):
        """Gate should store its type, inputs, and output."""
        circuit = GeneticCircuit(name="Test", inputs=["A", "B"], outputs=["Y"])
        circuit.add_gate("NOR", ["A", "B"], "Y")
        gate = circuit.gates[0]
        assert gate.gate_type == "NOR"
        assert gate.inputs == ["A", "B"]
        assert gate.output == "Y"

    def test_add_gate_invalid_type_raises(self):
        """Adding an unsupported gate type should raise ValueError."""
        circuit = GeneticCircuit(name="Test", inputs=["A"], outputs=["Y"])
        with pytest.raises(ValueError, match="Unsupported gate type"):
            circuit.add_gate("XOR", ["A"], "Y")

    def test_add_gate_not_type(self):
        """NOT gate should accept exactly one input."""
        circuit = GeneticCircuit(name="Test", inputs=["A"], outputs=["Y"])
        circuit.add_gate("NOT", ["A"], "Y")
        assert circuit.gates[0].gate_type == "NOT"

    def test_add_gate_and_requires_two_inputs(self):
        """AND gate should require exactly two inputs."""
        circuit = GeneticCircuit(name="Test", inputs=["A"], outputs=["Y"])
        with pytest.raises(ValueError, match="AND gate requires 2 inputs"):
            circuit.add_gate("AND", ["A"], "Y")


# ---------------------------------------------------------------------------
# GeneticCircuit – evaluate
# ---------------------------------------------------------------------------


class TestEvaluate:
    """Test circuit evaluation for various input combinations."""

    def test_and_gate_true(self):
        """AND gate should return True when both inputs are True."""
        circuit = GeneticCircuit(name="AND", inputs=["A", "B"], outputs=["Y"])
        circuit.add_gate("AND", ["A", "B"], "Y")
        result = circuit.evaluate({"A": True, "B": True})
        assert result["Y"] is True

    def test_and_gate_false(self):
        """AND gate should return False when any input is False."""
        circuit = GeneticCircuit(name="AND", inputs=["A", "B"], outputs=["Y"])
        circuit.add_gate("AND", ["A", "B"], "Y")
        result = circuit.evaluate({"A": True, "B": False})
        assert result["Y"] is False

    def test_or_gate_true(self):
        """OR gate should return True when at least one input is True."""
        circuit = GeneticCircuit(name="OR", inputs=["A", "B"], outputs=["Y"])
        circuit.add_gate("OR", ["A", "B"], "Y")
        result = circuit.evaluate({"A": False, "B": True})
        assert result["Y"] is True

    def test_or_gate_false(self):
        """OR gate should return False when both inputs are False."""
        circuit = GeneticCircuit(name="OR", inputs=["A", "B"], outputs=["Y"])
        circuit.add_gate("OR", ["A", "B"], "Y")
        result = circuit.evaluate({"A": False, "B": False})
        assert result["Y"] is False

    def test_not_gate(self):
        """NOT gate should invert its input."""
        circuit = GeneticCircuit(name="NOT", inputs=["A"], outputs=["Y"])
        circuit.add_gate("NOT", ["A"], "Y")
        assert circuit.evaluate({"A": True})["Y"] is False
        assert circuit.evaluate({"A": False})["Y"] is True

    def test_nor_gate(self):
        """NOR gate should return True only when both inputs are False."""
        circuit = GeneticCircuit(name="NOR", inputs=["A", "B"], outputs=["Y"])
        circuit.add_gate("NOR", ["A", "B"], "Y")
        assert circuit.evaluate({"A": False, "B": False})["Y"] is True
        assert circuit.evaluate({"A": True, "B": False})["Y"] is False
        assert circuit.evaluate({"A": False, "B": True})["Y"] is False
        assert circuit.evaluate({"A": True, "B": True})["Y"] is False

    def test_missing_input_raises(self):
        """Evaluating with missing inputs should raise ValueError."""
        circuit = GeneticCircuit(name="AND", inputs=["A", "B"], outputs=["Y"])
        circuit.add_gate("AND", ["A", "B"], "Y")
        with pytest.raises(ValueError, match="Missing input"):
            circuit.evaluate({"A": True})

    def test_chained_gates(self):
        """Circuit with chained gates should evaluate correctly."""
        circuit = GeneticCircuit(
            name="Chained",
            inputs=["A", "B"],
            outputs=["Y"],
        )
        # Y = NOT (A AND B)  →  NAND
        circuit.add_gate("AND", ["A", "B"], "intermediate")
        circuit.add_gate("NOT", ["intermediate"], "Y")
        assert circuit.evaluate({"A": True, "B": True})["Y"] is False
        assert circuit.evaluate({"A": True, "B": False})["Y"] is True

    def test_multiple_outputs_evaluate(self):
        """Circuit with multiple outputs should return all of them."""
        circuit = GeneticCircuit(
            name="MultiOut",
            inputs=["A", "B"],
            outputs=["Y1", "Y2"],
        )
        circuit.add_gate("AND", ["A", "B"], "Y1")
        circuit.add_gate("OR", ["A", "B"], "Y2")
        result = circuit.evaluate({"A": True, "B": False})
        assert result["Y1"] is False
        assert result["Y2"] is True


# ---------------------------------------------------------------------------
# GeneticCircuit – validate
# ---------------------------------------------------------------------------


class TestValidate:
    """Test circuit validation."""

    def test_valid_circuit(self):
        """A well-formed circuit should pass validation."""
        circuit = GeneticCircuit(name="Valid", inputs=["A", "B"], outputs=["Y"])
        circuit.add_gate("AND", ["A", "B"], "Y")
        assert circuit.validate() is True

    def test_empty_circuit_is_invalid(self):
        """A circuit with no gates should fail validation."""
        circuit = GeneticCircuit(name="Empty", inputs=["A"], outputs=["Y"])
        assert circuit.validate() is False

    def test_gate_references_unknown_input(self):
        """Gate referencing an undeclared input should fail validation."""
        circuit = GeneticCircuit(name="Bad", inputs=["A"], outputs=["Y"])
        circuit.add_gate("AND", ["A", "C"], "Y")
        assert circuit.validate() is False

    def test_gate_output_not_in_outputs(self):
        """Gate output not declared in circuit outputs should fail validation."""
        circuit = GeneticCircuit(name="Bad", inputs=["A", "B"], outputs=["Y"])
        circuit.add_gate("AND", ["A", "B"], "Z")
        assert circuit.validate() is False

    def test_no_output_gates(self):
        """Circuit where no gate produces a declared output should fail."""
        circuit = GeneticCircuit(name="Bad", inputs=["A", "B"], outputs=["Y"])
        circuit.add_gate("AND", ["A", "B"], "intermediate")
        assert circuit.validate() is False


# ---------------------------------------------------------------------------
# PathwayOptimizer – optimize_pathway
# ---------------------------------------------------------------------------


class TestOptimizePathway:
    """Test flux-based pathway optimization."""

    def test_simple_pathway_optimization(self):
        """Simple two-step pathway should optimize without error."""
        optimizer = PathwayOptimizer()
        pathway = {
            "reactions": [
                {"id": "R1", "substrates": ["A"], "products": ["B"], "flux": 1.0},
                {"id": "R2", "substrates": ["B"], "products": ["C"], "flux": 0.8},
            ],
            "target": "C",
        }
        result = optimizer.optimize_pathway(pathway)
        assert "optimal_fluxes" in result
        assert "max_yield" in result

    def test_optimization_improves_yield(self):
        """Optimization should not decrease the maximum yield."""
        optimizer = PathwayOptimizer()
        pathway = {
            "reactions": [
                {"id": "R1", "substrates": ["A"], "products": ["B"], "flux": 0.5},
                {"id": "R2", "substrates": ["B"], "products": ["C"], "flux": 0.5},
            ],
            "target": "C",
        }
        result = optimizer.optimize_pathway(pathway)
        assert result["max_yield"] >= 0.5

    def test_empty_pathway_raises(self):
        """Empty pathway should raise ValueError."""
        optimizer = PathwayOptimizer()
        with pytest.raises(ValueError, match="Empty pathway"):
            optimizer.optimize_pathway({"reactions": [], "target": "C"})

    def test_missing_target_raises(self):
        """Pathway with no target should raise ValueError."""
        optimizer = PathwayOptimizer()
        with pytest.raises(ValueError, match="target"):
            optimizer.optimize_pathway(
                {"reactions": [{"id": "R1", "substrates": ["A"], "products": ["B"], "flux": 1.0}]}
            )


# ---------------------------------------------------------------------------
# PathwayOptimizer – calculate_yield
# ---------------------------------------------------------------------------


class TestCalculateYield:
    """Test theoretical yield calculation."""

    def test_yield_simple_conversion(self):
        """1:1 stoichiometry should give yield of 1.0."""
        optimizer = PathwayOptimizer()
        stoichiometry = {"A": 1, "B": 1}
        result = optimizer.calculate_yield(stoichiometry, substrate="A", product="B")
        assert result == pytest.approx(1.0)

    def test_yield_two_to_one(self):
        """2:1 stoichiometry should give yield of 0.5."""
        optimizer = PathwayOptimizer()
        stoichiometry = {"A": 2, "B": 1}
        result = optimizer.calculate_yield(stoichiometry, substrate="A", product="B")
        assert result == pytest.approx(0.5)

    def test_yield_with_losses(self):
        """Yield with 10% loss should be reduced accordingly."""
        optimizer = PathwayOptimizer()
        stoichiometry = {"A": 1, "B": 1}
        result = optimizer.calculate_yield(
            stoichiometry, substrate="A", product="B", efficiency=0.9
        )
        assert result == pytest.approx(0.9)

    def test_yield_zero_stoichiometry_raises(self):
        """Zero stoichiometry for substrate should raise ValueError."""
        optimizer = PathwayOptimizer()
        with pytest.raises(ValueError, match="stoichiometry"):
            optimizer.calculate_yield({"A": 0, "B": 1}, substrate="A", product="B")


# ---------------------------------------------------------------------------
# DNASynthesis – design_overhangs
# ---------------------------------------------------------------------------


class TestDesignOverhangs:
    """Test Golden Gate overhang design."""

    def test_design_overhangs_basic(self):
        """Design overhangs for a list of parts."""
        synthesis = DNASynthesis()
        parts = ["promoter", "cds", "terminator"]
        overhangs = synthesis.design_overhangs(parts)
        assert len(overhangs) == len(parts)
        assert all(isinstance(oh, str) for oh in overhangs)
        assert all(len(oh) == 4 for oh in overhangs)

    def test_overhangs_are_unique(self):
        """All overhangs should be unique to avoid misassembly."""
        synthesis = DNASynthesis()
        parts = ["p1", "p2", "p3", "p4", "p5"]
        overhangs = synthesis.design_overhangs(parts)
        assert len(set(overhangs)) == len(overhangs)

    def test_overhangs_valid_nucleotides(self):
        """Overhangs should only contain valid nucleotides."""
        synthesis = DNASynthesis()
        parts = ["A", "B", "C"]
        overhangs = synthesis.design_overhangs(parts)
        valid = set("ACGT")
        for oh in overhangs:
            assert set(oh).issubset(valid)

    def test_empty_parts_returns_empty(self):
        """Empty parts list should return empty overhangs."""
        synthesis = DNASynthesis()
        assert synthesis.design_overhangs([]) == []

    def test_overhang_gc_content_balanced(self):
        """Overhangs should have GC content between 25% and 75%."""
        synthesis = DNASynthesis()
        parts = ["p1", "p2", "p3", "p4"]
        overhangs = synthesis.design_overhangs(parts)
        for oh in overhangs:
            gc = (oh.count("G") + oh.count("C")) / len(oh)
            assert 0.25 <= gc <= 0.75


# ---------------------------------------------------------------------------
# DNASynthesis – calculate_synthesis_cost
# ---------------------------------------------------------------------------


class TestCalculateSynthesisCost:
    """Test DNA synthesis cost estimation."""

    def test_cost_increases_with_length(self):
        """Longer sequences should cost more."""
        synthesis = DNASynthesis()
        short_cost = synthesis.calculate_synthesis_cost("ATGC" * 10)   # 40 bp
        long_cost = synthesis.calculate_synthesis_cost("ATGC" * 100)  # 400 bp
        assert long_cost > short_cost

    def test_cost_positive(self):
        """Cost should always be positive."""
        synthesis = DNASynthesis()
        cost = synthesis.calculate_synthesis_cost("ATGCGCAT")
        assert cost > 0

    def test_cost_with_gc_content_factor(self):
        """High-GC sequences should cost more than low-GC at same length."""
        synthesis = DNASynthesis()
        low_gc = synthesis.calculate_synthesis_cost("ATATATATATATATATATAT")
        high_gc = synthesis.calculate_synthesis_cost("GCGCGCGCGCGCGCGCGCGC")
        assert high_gc > low_gc

    def test_empty_sequence_zero_cost(self):
        """Empty sequence should have zero cost."""
        synthesis = DNASynthesis()
        assert synthesis.calculate_synthesis_cost("") == 0.0

    def test_cost_per_base_pair_reasonable(self):
        """Cost per base pair should be in a reasonable range ($0.10–$1.00)."""
        synthesis = DNASynthesis()
        seq = "ATGC" * 250  # 1000 bp
        cost = synthesis.calculate_synthesis_cost(seq)
        per_bp = cost / len(seq)
        assert 0.10 <= per_bp <= 1.00


# ---------------------------------------------------------------------------
# LogicGate – standalone gate evaluation
# ---------------------------------------------------------------------------


class TestLogicGate:
    """Test LogicGate as a standalone evaluator."""

    def test_and_gate_evaluation(self):
        """LogicGate AND should evaluate correctly."""
        gate = LogicGate("AND", ["A", "B"], "Y")
        assert gate.evaluate({"A": True, "B": True}) is True
        assert gate.evaluate({"A": True, "B": False}) is False

    def test_or_gate_evaluation(self):
        """LogicGate OR should evaluate correctly."""
        gate = LogicGate("OR", ["A", "B"], "Y")
        assert gate.evaluate({"A": False, "B": True}) is True
        assert gate.evaluate({"A": False, "B": False}) is False

    def test_not_gate_evaluation(self):
        """LogicGate NOT should evaluate correctly."""
        gate = LogicGate("NOT", ["A"], "Y")
        assert gate.evaluate({"A": True}) is False
        assert gate.evaluate({"A": False}) is True

    def test_nor_gate_evaluation(self):
        """LogicGate NOR should evaluate correctly."""
        gate = LogicGate("NOR", ["A", "B"], "Y")
        assert gate.evaluate({"A": False, "B": False}) is True
        assert gate.evaluate({"A": True, "B": True}) is False

    def test_invalid_gate_type_raises(self):
        """Creating a LogicGate with invalid type should raise ValueError."""
        with pytest.raises(ValueError, match="Unsupported gate type"):
            LogicGate("XOR", ["A"], "Y")
