"""Test-driven development: Integration module tests."""

import pytest

from src.integration.knowledge_graph import (
    DigitalTwin,
    EventBus,
    KnowledgeGraph,
    Ontology,
)

# =============================================================================
# KnowledgeGraph Tests
# =============================================================================


class TestKnowledgeGraphAddEntity:
    """Test adding entities to the knowledge graph."""

    def test_add_entity_basic(self):
        """Should add an entity with a type."""
        kg = KnowledgeGraph()
        kg.add_entity("gene_1", "Gene")
        assert "gene_1" in kg.entities
        assert kg.entities["gene_1"]["type"] == "Gene"

    def test_add_entity_with_properties(self):
        """Should add an entity with custom properties."""
        kg = KnowledgeGraph()
        kg.add_entity("gene_1", "Gene", {"name": "BRCA1", "organism": "human"})
        assert kg.entities["gene_1"]["properties"]["name"] == "BRCA1"
        assert kg.entities["gene_1"]["properties"]["organism"] == "human"

    def test_add_entity_duplicate_updates(self):
        """Adding same entity ID should update properties."""
        kg = KnowledgeGraph()
        kg.add_entity("gene_1", "Gene", {"name": "BRCA1"})
        kg.add_entity("gene_1", "Gene", {"name": "BRCA2"})
        assert kg.entities["gene_1"]["properties"]["name"] == "BRCA2"

    def test_add_entity_empty_id_raises(self):
        """Empty entity ID should raise ValueError."""
        kg = KnowledgeGraph()
        with pytest.raises(ValueError):
            kg.add_entity("", "Gene")


class TestKnowledgeGraphAddRelation:
    """Test adding relations between entities."""

    def test_add_relation_basic(self):
        """Should create a relation between two entities."""
        kg = KnowledgeGraph()
        kg.add_entity("gene_1", "Gene")
        kg.add_entity("disease_1", "Disease")
        kg.add_relation("gene_1", "associated_with", "disease_1")
        assert ("gene_1", "associated_with", "disease_1", 1.0) in kg.relations

    def test_add_relation_with_weight(self):
        """Should store relation weight."""
        kg = KnowledgeGraph()
        kg.add_entity("gene_1", "Gene")
        kg.add_entity("disease_1", "Disease")
        kg.add_relation("gene_1", "associated_with", "disease_1", weight=0.9)
        rel = [r for r in kg.relations if r[0] == "gene_1"][0]
        assert rel[3] == 0.9

    def test_add_relation_nonexistent_entity_raises(self):
        """Relation with non-existent entity should raise ValueError."""
        kg = KnowledgeGraph()
        kg.add_entity("gene_1", "Gene")
        with pytest.raises(ValueError):
            kg.add_relation("gene_1", "associated_with", "nonexistent")


class TestKnowledgeGraphQuery:
    """Test querying the knowledge graph."""

    def test_query_by_type(self):
        """Should return all entities of a given type."""
        kg = KnowledgeGraph()
        kg.add_entity("gene_1", "Gene")
        kg.add_entity("gene_2", "Gene")
        kg.add_entity("disease_1", "Disease")
        results = kg.query(type="Gene")
        assert len(results) == 2
        assert "gene_1" in results
        assert "gene_2" in results

    def test_query_by_property(self):
        """Should return entities matching property criteria."""
        kg = KnowledgeGraph()
        kg.add_entity("gene_1", "Gene", {"organism": "human"})
        kg.add_entity("gene_2", "Gene", {"organism": "mouse"})
        results = kg.query(type="Gene", properties={"organism": "human"})
        assert len(results) == 1
        assert "gene_1" in results

    def test_query_no_results(self):
        """Should return empty dict when no matches."""
        kg = KnowledgeGraph()
        kg.add_entity("gene_1", "Gene")
        results = kg.query(type="NonExistent")
        assert results == {}

    def test_query_all_entities(self):
        """Query with no filters should return all entities."""
        kg = KnowledgeGraph()
        kg.add_entity("gene_1", "Gene")
        kg.add_entity("disease_1", "Disease")
        results = kg.query()
        assert len(results) == 2


class TestKnowledgeGraphGetNeighbors:
    """Test getting neighboring entities."""

    def test_get_neighbors_basic(self):
        """Should return directly connected entities."""
        kg = KnowledgeGraph()
        kg.add_entity("gene_1", "Gene")
        kg.add_entity("disease_1", "Disease")
        kg.add_entity("drug_1", "Drug")
        kg.add_relation("gene_1", "associated_with", "disease_1")
        kg.add_relation("gene_1", "targeted_by", "drug_1")
        neighbors = kg.get_neighbors("gene_1")
        assert "disease_1" in neighbors
        assert "drug_1" in neighbors

    def test_get_neighbors_no_connections(self):
        """Should return empty set for isolated entity."""
        kg = KnowledgeGraph()
        kg.add_entity("gene_1", "Gene")
        neighbors = kg.get_neighbors("gene_1")
        assert neighbors == set()

    def test_get_neighbors_nonexistent_raises(self):
        """Should raise ValueError for non-existent entity."""
        kg = KnowledgeGraph()
        with pytest.raises(ValueError):
            kg.get_neighbors("nonexistent")


# =============================================================================
# Ontology Tests
# =============================================================================


class TestOntologyLoad:
    """Test loading ontology terms."""

    def test_load_ontology_basic(self):
        """Should load SO/GO/ChEBI terms."""
        ont = Ontology()
        ont.load_ontology("SO")
        assert len(ont.terms) > 0

    def test_load_ontology_go(self):
        """Should load GO terms."""
        ont = Ontology()
        ont.load_ontology("GO")
        assert len(ont.terms) > 0

    def test_load_ontology_chebi(self):
        """Should load ChEBI terms."""
        ont = Ontology()
        ont.load_ontology("ChEBI")
        assert len(ont.terms) > 0

    def test_load_ontology_invalid_source_raises(self):
        """Invalid ontology source should raise ValueError."""
        ont = Ontology()
        with pytest.raises(ValueError):
            ont.load_ontology("INVALID")


class TestOntologyGetTerm:
    """Test retrieving ontology terms."""

    def test_get_term_existing(self):
        """Should return term data for existing ID."""
        ont = Ontology()
        ont.load_ontology("SO")
        term = ont.get_term("SO:0000704")
        assert term is not None
        assert "name" in term

    def test_get_term_nonexistent(self):
        """Should return None for non-existent term."""
        ont = Ontology()
        ont.load_ontology("SO")
        term = ont.get_term("SO:9999999")
        assert term is None

    def test_get_term_before_load_raises(self):
        """Should raise RuntimeError if ontology not loaded."""
        ont = Ontology()
        with pytest.raises(RuntimeError):
            ont.get_term("SO:0000704")


class TestOntologyGetParents:
    """Test retrieving parent terms."""

    def test_get_parents_basic(self):
        """Should return parent term IDs."""
        ont = Ontology()
        ont.load_ontology("SO")
        parents = ont.get_parents("SO:0000704")
        assert isinstance(parents, list)

    def test_get_parents_root_term(self):
        """Root term should have no parents."""
        ont = Ontology()
        ont.load_ontology("SO")
        parents = ont.get_parents("SO:0000110")
        assert parents == []

    def test_get_parents_nonexistent_raises(self):
        """Should raise ValueError for non-existent term."""
        ont = Ontology()
        ont.load_ontology("SO")
        with pytest.raises(ValueError):
            ont.get_parents("SO:9999999")


# =============================================================================
# EventBus Tests
# =============================================================================


class TestEventBusPublish:
    """Test publishing events."""

    def test_publish_basic(self):
        """Should publish an event."""
        bus = EventBus()
        bus.publish("test_event", {"data": 42})
        events = bus.get_events()
        assert len(events) == 1
        assert events[0]["type"] == "test_event"

    def test_publish_with_data(self):
        """Should store event data."""
        bus = EventBus()
        bus.publish("gene_created", {"gene_id": "gene_1"})
        events = bus.get_events()
        assert events[0]["data"]["gene_id"] == "gene_1"

    def test_publish_multiple(self):
        """Should store multiple events."""
        bus = EventBus()
        bus.publish("event_1")
        bus.publish("event_2")
        bus.publish("event_3")
        assert len(bus.get_events()) == 3


class TestEventBusSubscribe:
    """Test subscribing to events."""

    def test_subscribe_basic(self):
        """Subscriber should receive published events."""
        bus = EventBus()
        received = []
        bus.subscribe("test_event", lambda e: received.append(e))
        bus.publish("test_event", {"msg": "hello"})
        assert len(received) == 1
        assert received[0]["data"]["msg"] == "hello"

    def test_subscribe_multiple_subscribers(self):
        """Multiple subscribers should all receive events."""
        bus = EventBus()
        received_1 = []
        received_2 = []
        bus.subscribe("test_event", lambda e: received_1.append(e))
        bus.subscribe("test_event", lambda e: received_2.append(e))
        bus.publish("test_event")
        assert len(received_1) == 1
        assert len(received_2) == 1

    def test_subscribe_wrong_type_no_receive(self):
        """Subscriber should not receive events of different type."""
        bus = EventBus()
        received = []
        bus.subscribe("type_a", lambda e: received.append(e))
        bus.publish("type_b")
        assert len(received) == 0


class TestEventBusGetEvents:
    """Test retrieving events."""

    def test_get_events_empty(self):
        """Should return empty list when no events."""
        bus = EventBus()
        assert bus.get_events() == []

    def test_get_events_filter_by_type(self):
        """Should filter events by type."""
        bus = EventBus()
        bus.publish("type_a", {"val": 1})
        bus.publish("type_b", {"val": 2})
        bus.publish("type_a", {"val": 3})
        events = bus.get_events(event_type="type_a")
        assert len(events) == 2

    def test_get_events_returns_copy(self):
        """Modifying returned events should not affect internal state."""
        bus = EventBus()
        bus.publish("test_event")
        events = bus.get_events()
        events.clear()
        assert len(bus.get_events()) == 1


# =============================================================================
# DigitalTwin Tests
# =============================================================================


class TestDigitalTwinUpdateState:
    """Test updating digital twin state."""

    def test_update_state_basic(self):
        """Should update twin state."""
        twin = DigitalTwin("cell_1")
        twin.update_state("temperature", 37.0)
        assert twin.get_state("temperature") == 37.0

    def test_update_state_multiple_keys(self):
        """Should update multiple state keys."""
        twin = DigitalTwin("cell_1")
        twin.update_state("temperature", 37.0)
        twin.update_state("ph", 7.4)
        state = twin.get_state()
        assert state["temperature"] == 37.0
        assert state["ph"] == 7.4

    def test_update_state_overwrite(self):
        """Should overwrite existing state value."""
        twin = DigitalTwin("cell_1")
        twin.update_state("temperature", 37.0)
        twin.update_state("temperature", 40.0)
        assert twin.get_state("temperature") == 40.0


class TestDigitalTwinGetState:
    """Test getting digital twin state."""

    def test_get_state_specific_key(self):
        """Should return value for specific key."""
        twin = DigitalTwin("cell_1")
        twin.update_state("temperature", 37.0)
        assert twin.get_state("temperature") == 37.0

    def test_get_state_all(self):
        """Should return all state when no key specified."""
        twin = DigitalTwin("cell_1")
        twin.update_state("temperature", 37.0)
        twin.update_state("ph", 7.4)
        state = twin.get_state()
        assert isinstance(state, dict)
        assert len(state) == 2

    def test_get_state_nonexistent_key(self):
        """Should return None for non-existent key."""
        twin = DigitalTwin("cell_1")
        assert twin.get_state("nonexistent") is None


class TestDigitalTwinSimulate:
    """Test digital twin simulation."""

    def test_simulate_basic(self):
        """Should run simulation and update state."""
        twin = DigitalTwin("cell_1")
        twin.update_state("cell_count", 100)
        twin.simulate(steps=1)
        assert twin.get_state("cell_count") != 100

    def test_simulate_multiple_steps(self):
        """Should run multiple simulation steps."""
        twin = DigitalTwin("cell_1")
        twin.update_state("cell_count", 100)
        twin.simulate(steps=5)
        state = twin.get_state()
        assert "cell_count" in state

    def test_simulate_zero_steps(self):
        """Zero steps should not change state."""
        twin = DigitalTwin("cell_1")
        twin.update_state("cell_count", 100)
        twin.simulate(steps=0)
        assert twin.get_state("cell_count") == 100

    def test_simulate_returns_state(self):
        """Should return current state after simulation."""
        twin = DigitalTwin("cell_1")
        twin.update_state("cell_count", 100)
        result = twin.simulate(steps=1)
        assert isinstance(result, dict)
        assert "cell_count" in result
