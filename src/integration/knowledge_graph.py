"""Knowledge Graph, Ontology, EventBus, and Digital Twin implementation."""

from __future__ import annotations

import copy
import json
import random
from typing import Any, Callable

# =============================================================================
# KnowledgeGraph
# =============================================================================


class KnowledgeGraph:
    """Simple knowledge graph for entities and relations."""

    def __init__(self, event_bus: EventBus | None = None) -> None:
        self.entities: dict[str, dict[str, Any]] = {}
        self.relations: list[tuple[str, str, str, float]] = []
        self._type_index: dict[str, set[str]] = {}
        self._adj_index: dict[str, set[str]] = {}
        self._event_bus = event_bus

    def add_entity(
        self, entity_id: str, entity_type: str, properties: dict[str, Any] | None = None
    ) -> None:
        """Add an entity with a type and optional properties."""
        if not entity_id:
            raise ValueError("Entity ID cannot be empty")
        self.entities[entity_id] = {
            "type": entity_type,
            "properties": properties or {},
        }
        self._type_index.setdefault(entity_type, set()).add(entity_id)
        self._adj_index.setdefault(entity_id, set())
        if self._event_bus is not None:
            self._event_bus.publish("entity_added", {
                "entity_id": entity_id,
                "entity_type": entity_type,
                "properties": properties or {},
            })

    def add_relation(
        self, source: str, relation: str, target: str, weight: float = 1.0
    ) -> None:
        """Add a relation between two entities."""
        if source not in self.entities:
            raise ValueError(f"Source entity '{source}' does not exist")
        if target not in self.entities:
            raise ValueError(f"Target entity '{target}' does not exist")
        self.relations.append((source, relation, target, weight))
        self._adj_index.setdefault(source, set()).add(target)
        self._adj_index.setdefault(target, set()).add(source)
        if self._event_bus is not None:
            self._event_bus.publish("relation_added", {
                "source": source,
                "relation": relation,
                "target": target,
                "weight": weight,
            })

    def query(
        self,
        type: str | None = None,
        properties: dict[str, Any] | None = None,
    ) -> dict[str, dict[str, Any]]:
        """Query entities by type and/or properties."""
        results: dict[str, dict[str, Any]] = {}
        if type is not None:
            candidates = self._type_index.get(type, set())
        else:
            candidates = set(self.entities.keys())
        for entity_id in candidates:
            entity_data = self.entities[entity_id]
            if properties is not None:
                match = all(
                    entity_data["properties"].get(k) == v
                    for k, v in properties.items()
                )
                if not match:
                    continue
            results[entity_id] = copy.deepcopy(entity_data)
        return results

    def get_neighbors(self, entity_id: str) -> set[str]:
        """Get all entities directly connected to the given entity."""
        if entity_id not in self.entities:
            raise ValueError(f"Entity '{entity_id}' does not exist")
        return set(self._adj_index.get(entity_id, set()))

    def to_dict(self) -> dict[str, Any]:
        """Serialize the graph to a dictionary."""
        return {
            "entities": self.entities,
            "relations": self.relations,
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> KnowledgeGraph:
        """Reconstruct a KnowledgeGraph from a dictionary."""
        kg = cls()
        kg.entities = data["entities"]
        kg.relations = [tuple(r) for r in data["relations"]]
        # Rebuild indexes
        for entity_id, entity_data in kg.entities.items():
            entity_type = entity_data["type"]
            kg._type_index.setdefault(entity_type, set()).add(entity_id)
            kg._adj_index.setdefault(entity_id, set())
        for source, _rel, target, _w in kg.relations:
            kg._adj_index.setdefault(source, set()).add(target)
            kg._adj_index.setdefault(target, set()).add(source)
        return kg

    def to_json(self) -> str:
        """Serialize the graph to a JSON string."""
        return json.dumps(self.to_dict())

    @classmethod
    def from_json(cls, json_str: str) -> KnowledgeGraph:
        """Reconstruct a KnowledgeGraph from a JSON string."""
        return cls.from_dict(json.loads(json_str))


# =============================================================================
# Ontology
# =============================================================================


_ONTOLOGY_DATA: dict[str, dict[str, dict[str, Any]]] = {
    "SO": {
        "SO:0000110": {"name": "sequence_feature", "parents": []},
        "SO:0000704": {"name": "gene", "parents": ["SO:0000110"]},
        "SO:0000234": {"name": "transcript", "parents": ["SO:0000110"]},
        "SO:0000147": {"name": "exon", "parents": ["SO:0000110"]},
    },
    "GO": {
        "GO:0008150": {"name": "biological_process", "parents": []},
        "GO:0005575": {"name": "cellular_component", "parents": []},
        "GO:0003674": {"name": "molecular_function", "parents": []},
        "GO:0007049": {"name": "cell cycle", "parents": ["GO:0008150"]},
        "GO:0006281": {"name": "DNA repair", "parents": ["GO:0008150"]},
    },
    "ChEBI": {
        "CHEBI:15377": {"name": "water", "parents": []},
        "CHEBI:17794": {"name": "carbohydrate", "parents": []},
        "CHEBI:18059": {"name": "lipid", "parents": []},
        "CHEBI:33695": {"name": "protein", "parents": []},
    },
}


class Ontology:
    """Ontology for SO/GO/ChEBI terms."""

    def __init__(self) -> None:
        self.terms: dict[str, dict[str, Any]] = {}
        self._loaded: bool = False

    def load_ontology(self, source: str) -> None:
        """Load ontology terms from a source (SO, GO, ChEBI)."""
        if source not in _ONTOLOGY_DATA:
            raise ValueError(f"Unknown ontology source: {source}")
        self.terms = copy.deepcopy(_ONTOLOGY_DATA[source])
        self._loaded = True

    def get_term(self, term_id: str) -> dict[str, Any] | None:
        """Get term by ID. Returns None if not found."""
        if not self._loaded:
            raise RuntimeError("Ontology not loaded. Call load_ontology() first.")
        term = self.terms.get(term_id)
        return copy.deepcopy(term) if term is not None else None

    def get_parents(self, term_id: str) -> list[str]:
        """Get parent term IDs for a given term."""
        if not self._loaded:
            raise RuntimeError("Ontology not loaded. Call load_ontology() first.")
        if term_id not in self.terms:
            raise ValueError(f"Term '{term_id}' not found in ontology")
        return list(self.terms[term_id].get("parents", []))


# =============================================================================
# EventBus
# =============================================================================


class EventBus:
    """Simple event bus for publish/subscribe pattern."""

    def __init__(self, max_events: int = 10000) -> None:
        self._events: list[dict[str, Any]] = []
        self._subscribers: dict[str, list[Callable[[dict[str, Any]], None]]] = {}
        self._max_events = max_events

    def publish(self, event_type: str, data: dict[str, Any] | None = None) -> None:
        """Publish an event to all subscribers."""
        event = {
            "type": event_type,
            "data": data or {},
        }
        self._events.append(event)
        if len(self._events) > self._max_events:
            self._events = self._events[-self._max_events:]
        for callback in self._subscribers.get(event_type, []):
            callback(copy.deepcopy(event))

    def subscribe(
        self, event_type: str, callback: Callable[[dict[str, Any]], None]
    ) -> None:
        """Subscribe a callback to an event type."""
        if event_type not in self._subscribers:
            self._subscribers[event_type] = []
        self._subscribers[event_type].append(callback)

    def get_events(self, event_type: str | None = None) -> list[dict[str, Any]]:
        """Retrieve events, optionally filtered by type."""
        if event_type is None:
            return copy.deepcopy(self._events)
        return copy.deepcopy([e for e in self._events if e["type"] == event_type])


# =============================================================================
# DigitalTwin
# =============================================================================


class DigitalTwin:
    """Digital twin for simulating biological entities."""

    def __init__(self, twin_id: str, event_bus: EventBus | None = None) -> None:
        self.twin_id = twin_id
        self._state: dict[str, Any] = {}
        self._event_bus = event_bus

    def update_state(self, key: str, value: Any) -> None:
        """Update a state variable."""
        self._state[key] = value
        if self._event_bus is not None:
            self._event_bus.publish("state_updated", {
                "twin_id": self.twin_id,
                "key": key,
                "value": value,
            })

    def get_state(self, key: str | None = None) -> Any:
        """Get state for a specific key, or all state if no key given."""
        if key is not None:
            return self._state.get(key)
        return copy.deepcopy(self._state)

    def simulate(self, steps: int = 1) -> dict[str, Any]:
        """Run simulation for a number of steps."""
        if steps <= 0:
            return copy.deepcopy(self._state)
        for _ in range(steps):
            if "cell_count" in self._state:
                old = self._state["cell_count"]
                new = old * (1 + random.uniform(-0.1, 0.1))
                # Guarantee minimum change of 1 to avoid rounding collapse
                if new > old:
                    self._state["cell_count"] = max(old + 1, round(new))
                else:
                    self._state["cell_count"] = max(1, min(old - 1, round(new)))
            if "temperature" in self._state:
                self._state["temperature"] += random.uniform(-0.5, 0.5)
            if "ph" in self._state:
                self._state["ph"] += random.uniform(-0.1, 0.1)
        if self._event_bus is not None:
            self._event_bus.publish("simulation_step", {
                "twin_id": self.twin_id,
                "steps": steps,
            })
        return copy.deepcopy(self._state)
