"""TDD tests for EventBus integration with KnowledgeGraph and DigitalTwin."""
from src.integration.knowledge_graph import DigitalTwin, EventBus, KnowledgeGraph


class TestKnowledgeGraphEventIntegration:
    """KnowledgeGraph publishes events when event_bus is provided."""

    def test_add_entity_publishes_event(self):
        """add_entity should publish 'entity_added' to the event bus."""
        bus = EventBus()
        kg = KnowledgeGraph(event_bus=bus)
        kg.add_entity("gene_1", "Gene", {"name": "BRCA1"})
        events = bus.get_events("entity_added")
        assert len(events) == 1
        assert events[0]["data"]["entity_id"] == "gene_1"
        assert events[0]["data"]["entity_type"] == "Gene"

    def test_add_relation_publishes_event(self):
        """add_relation should publish 'relation_added' to the event bus."""
        bus = EventBus()
        kg = KnowledgeGraph(event_bus=bus)
        kg.add_entity("gene_1", "Gene")
        kg.add_entity("disease_1", "Disease")
        kg.add_relation("gene_1", "associated_with", "disease_1", weight=0.9)
        events = bus.get_events("relation_added")
        assert len(events) == 1
        assert events[0]["data"]["source"] == "gene_1"
        assert events[0]["data"]["relation"] == "associated_with"
        assert events[0]["data"]["target"] == "disease_1"

    def test_without_event_bus_works_normally(self):
        """KnowledgeGraph without event_bus should work without publishing."""
        kg = KnowledgeGraph()
        kg.add_entity("gene_1", "Gene")
        kg.add_entity("disease_1", "Disease")
        kg.add_relation("gene_1", "associated_with", "disease_1")
        assert "gene_1" in kg.entities
        assert len(kg.relations) == 1


class TestDigitalTwinEventIntegration:
    """DigitalTwin publishes events when event_bus is provided."""

    def test_update_state_publishes_event(self):
        """update_state should publish 'state_updated' to the event bus."""
        bus = EventBus()
        twin = DigitalTwin("cell_1", event_bus=bus)
        twin.update_state("temperature", 37.0)
        events = bus.get_events("state_updated")
        assert len(events) == 1
        assert events[0]["data"]["twin_id"] == "cell_1"
        assert events[0]["data"]["key"] == "temperature"
        assert events[0]["data"]["value"] == 37.0

    def test_simulate_publishes_event(self):
        """simulate should publish 'simulation_step' to the event bus."""
        bus = EventBus()
        twin = DigitalTwin("cell_1", event_bus=bus)
        twin.update_state("cell_count", 100)
        twin.simulate(steps=1)
        events = bus.get_events("simulation_step")
        assert len(events) == 1
        assert events[0]["data"]["twin_id"] == "cell_1"

    def test_without_event_bus_works_normally(self):
        """DigitalTwin without event_bus should work without publishing."""
        twin = DigitalTwin("cell_1")
        twin.update_state("temperature", 37.0)
        twin.update_state("cell_count", 100)
        assert twin.get_state("temperature") == 37.0
        twin.simulate(steps=1)
        assert "cell_count" in twin.get_state()
