"""Test-driven development: Graph algorithm tests for KnowledgeGraph."""
import pytest

from src.integration.knowledge_graph import KnowledgeGraph

# =============================================================================
# shortest_path Tests
# =============================================================================


class TestShortestPath:
    """Test BFS shortest path between entities."""

    def test_shortest_path_no_path_returns_empty(self):
        """Should return [] when no path exists between source and target."""
        kg = KnowledgeGraph()
        kg.add_entity("a", "Gene")
        kg.add_entity("b", "Gene")
        result = kg.shortest_path("a", "b")
        assert result == []

    def test_shortest_path_direct_connection(self):
        """Should return [source, target] for directly connected entities."""
        kg = KnowledgeGraph()
        kg.add_entity("a", "Gene")
        kg.add_entity("b", "Disease")
        kg.add_relation("a", "associated_with", "b")
        result = kg.shortest_path("a", "b")
        assert result == ["a", "b"]

    def test_shortest_path_multi_hop(self):
        """Should return correct path for multi-hop connections."""
        kg = KnowledgeGraph()
        kg.add_entity("a", "Gene")
        kg.add_entity("b", "Protein")
        kg.add_entity("c", "Pathway")
        kg.add_entity("d", "Disease")
        kg.add_relation("a", "encodes", "b")
        kg.add_relation("b", "part_of", "c")
        kg.add_relation("c", "associated_with", "d")
        result = kg.shortest_path("a", "d")
        assert result == ["a", "b", "c", "d"]

    def test_shortest_path_same_source_target(self):
        """Should return [source] when source equals target."""
        kg = KnowledgeGraph()
        kg.add_entity("a", "Gene")
        result = kg.shortest_path("a", "a")
        assert result == ["a"]

    def test_shortest_path_nonexistent_source_raises(self):
        """Should raise ValueError for non-existent source."""
        kg = KnowledgeGraph()
        kg.add_entity("a", "Gene")
        with pytest.raises(ValueError):
            kg.shortest_path("nonexistent", "a")

    def test_shortest_path_nonexistent_target_raises(self):
        """Should raise ValueError for non-existent target."""
        kg = KnowledgeGraph()
        kg.add_entity("a", "Gene")
        with pytest.raises(ValueError):
            kg.shortest_path("a", "nonexistent")


# =============================================================================
# get_connected_components Tests
# =============================================================================


class TestGetConnectedComponents:
    """Test finding connected components in the graph."""

    def test_empty_graph_returns_empty_list(self):
        """Should return [] for an empty graph."""
        kg = KnowledgeGraph()
        result = kg.get_connected_components()
        assert result == []

    def test_single_entity_returns_single_component(self):
        """Should return one component with one entity."""
        kg = KnowledgeGraph()
        kg.add_entity("a", "Gene")
        result = kg.get_connected_components()
        assert len(result) == 1
        assert result[0] == {"a"}

    def test_connected_graph_returns_single_component(self):
        """Should return one component for a fully connected graph."""
        kg = KnowledgeGraph()
        kg.add_entity("a", "Gene")
        kg.add_entity("b", "Protein")
        kg.add_entity("c", "Pathway")
        kg.add_relation("a", "encodes", "b")
        kg.add_relation("b", "part_of", "c")
        result = kg.get_connected_components()
        assert len(result) == 1
        assert result[0] == {"a", "b", "c"}

    def test_disconnected_graph_returns_multiple_components(self):
        """Should return separate components for disconnected subgraphs."""
        kg = KnowledgeGraph()
        kg.add_entity("a", "Gene")
        kg.add_entity("b", "Protein")
        kg.add_entity("c", "Pathway")
        kg.add_entity("d", "Disease")
        kg.add_relation("a", "encodes", "b")
        kg.add_relation("c", "associated_with", "d")
        result = kg.get_connected_components()
        assert len(result) == 2
        component_sets = [set(c) for c in result]
        assert {"a", "b"} in component_sets
        assert {"c", "d"} in component_sets

    def test_isolated_entities_each_own_component(self):
        """Each isolated entity should be its own component."""
        kg = KnowledgeGraph()
        kg.add_entity("a", "Gene")
        kg.add_entity("b", "Protein")
        kg.add_entity("c", "Pathway")
        result = kg.get_connected_components()
        assert len(result) == 3
        component_sets = [set(c) for c in result]
        assert {"a"} in component_sets
        assert {"b"} in component_sets
        assert {"c"} in component_sets


# =============================================================================
# get_degree_centrality Tests
# =============================================================================


class TestGetDegreeCentrality:
    """Test degree centrality calculation."""

    def test_empty_graph_returns_empty_dict(self):
        """Should return {} for an empty graph."""
        kg = KnowledgeGraph()
        result = kg.get_degree_centrality()
        assert result == {}

    def test_returns_dict_with_all_entities(self):
        """Should return a dict containing every entity."""
        kg = KnowledgeGraph()
        kg.add_entity("a", "Gene")
        kg.add_entity("b", "Protein")
        kg.add_entity("c", "Pathway")
        result = kg.get_degree_centrality()
        assert isinstance(result, dict)
        assert set(result.keys()) == {"a", "b", "c"}

    def test_isolated_entity_has_zero_centrality(self):
        """Isolated entity should have centrality of 0.0."""
        kg = KnowledgeGraph()
        kg.add_entity("a", "Gene")
        result = kg.get_degree_centrality()
        assert result["a"] == 0.0

    def test_connected_entity_centrality(self):
        """Entity with connections should have positive centrality."""
        kg = KnowledgeGraph()
        kg.add_entity("a", "Gene")
        kg.add_entity("b", "Protein")
        kg.add_entity("c", "Pathway")
        kg.add_relation("a", "encodes", "b")
        kg.add_relation("a", "part_of", "c")
        result = kg.get_degree_centrality()
        assert result["a"] > 0.0
        assert result["b"] > 0.0
        assert result["c"] > 0.0

    def test_centrality_values_are_normalized(self):
        """Centrality values should be between 0 and 1."""
        kg = KnowledgeGraph()
        kg.add_entity("a", "Gene")
        kg.add_entity("b", "Protein")
        kg.add_entity("c", "Pathway")
        kg.add_relation("a", "encodes", "b")
        kg.add_relation("a", "part_of", "c")
        result = kg.get_degree_centrality()
        for value in result.values():
            assert 0.0 <= value <= 1.0
