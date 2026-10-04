"""Test-driven development: KnowledgeGraph persistence tests."""
import json

from src.integration.knowledge_graph import KnowledgeGraph


def _build_sample_graph() -> KnowledgeGraph:
    """Build a small graph with entities and relations for testing."""
    kg = KnowledgeGraph()
    kg.add_entity("gene_1", "Gene", {"name": "BRCA1", "organism": "human"})
    kg.add_entity("gene_2", "Gene", {"name": "TP53", "organism": "human"})
    kg.add_entity("disease_1", "Disease", {"name": "breast cancer"})
    kg.add_relation("gene_1", "associated_with", "disease_1", weight=0.9)
    kg.add_relation("gene_2", "associated_with", "disease_1", weight=0.7)
    return kg


class TestToDict:
    """Test to_dict serialization."""

    def test_to_dict_returns_correct_structure(self):
        """to_dict should return dict with 'entities' and 'relations' keys."""
        kg = _build_sample_graph()
        data = kg.to_dict()
        assert isinstance(data, dict)
        assert "entities" in data
        assert "relations" in data

    def test_to_dict_entities_match_internal(self):
        """to_dict entities should match internal entities dict."""
        kg = _build_sample_graph()
        data = kg.to_dict()
        assert data["entities"] == kg.entities

    def test_to_dict_relations_match_internal(self):
        """to_dict relations should match internal relations list."""
        kg = _build_sample_graph()
        data = kg.to_dict()
        assert data["relations"] == kg.relations

    def test_to_dict_empty_graph(self):
        """to_dict on empty graph should return empty entities and relations."""
        kg = KnowledgeGraph()
        data = kg.to_dict()
        assert data["entities"] == {}
        assert data["relations"] == []


class TestFromDict:
    """Test from_dict deserialization."""

    def test_from_dict_reconstructs_graph_correctly(self):
        """from_dict should reconstruct a graph with correct entities and relations."""
        kg = _build_sample_graph()
        data = kg.to_dict()
        kg2 = KnowledgeGraph.from_dict(data)
        assert kg2.entities == kg.entities
        assert kg2.relations == kg.relations

    def test_from_dict_rebuilds_type_index(self):
        """from_dict should rebuild the type index correctly."""
        kg = _build_sample_graph()
        data = kg.to_dict()
        kg2 = KnowledgeGraph.from_dict(data)
        assert kg2._type_index["Gene"] == {"gene_1", "gene_2"}
        assert kg2._type_index["Disease"] == {"disease_1"}

    def test_from_dict_rebuilds_adj_index(self):
        """from_dict should rebuild the adjacency index correctly."""
        kg = _build_sample_graph()
        data = kg.to_dict()
        kg2 = KnowledgeGraph.from_dict(data)
        assert "disease_1" in kg2._adj_index["gene_1"]
        assert "disease_1" in kg2._adj_index["gene_2"]
        assert "gene_1" in kg2._adj_index["disease_1"]
        assert "gene_2" in kg2._adj_index["disease_1"]

    def test_from_dict_query_works(self):
        """Reconstructed graph should support query operations."""
        kg = _build_sample_graph()
        data = kg.to_dict()
        kg2 = KnowledgeGraph.from_dict(data)
        results = kg2.query(type="Gene")
        assert len(results) == 2
        assert "gene_1" in results
        assert "gene_2" in results

    def test_from_dict_get_neighbors_works(self):
        """Reconstructed graph should support get_neighbors."""
        kg = _build_sample_graph()
        data = kg.to_dict()
        kg2 = KnowledgeGraph.from_dict(data)
        neighbors = kg2.get_neighbors("gene_1")
        assert "disease_1" in neighbors


class TestDictRoundtrip:
    """Test to_dict/from_dict roundtrip preserves all data."""

    def test_roundtrip_preserves_entities(self):
        """Roundtrip should preserve all entity data."""
        kg = _build_sample_graph()
        data = kg.to_dict()
        kg2 = KnowledgeGraph.from_dict(data)
        assert kg2.entities == kg.entities

    def test_roundtrip_preserves_relations(self):
        """Roundtrip should preserve all relation data."""
        kg = _build_sample_graph()
        data = kg.to_dict()
        kg2 = KnowledgeGraph.from_dict(data)
        assert kg2.relations == kg.relations

    def test_roundtrip_preserves_query_results(self):
        """Query results should be identical after roundtrip."""
        kg = _build_sample_graph()
        data = kg.to_dict()
        kg2 = KnowledgeGraph.from_dict(data)
        assert kg2.query(type="Gene", properties={"organism": "human"}) == \
               kg.query(type="Gene", properties={"organism": "human"})

    def test_roundtrip_preserves_neighbors(self):
        """Neighbor sets should be identical after roundtrip."""
        kg = _build_sample_graph()
        data = kg.to_dict()
        kg2 = KnowledgeGraph.from_dict(data)
        assert kg2.get_neighbors("gene_1") == kg.get_neighbors("gene_1")
        assert kg2.get_neighbors("disease_1") == kg.get_neighbors("disease_1")


class TestToJson:
    """Test to_json serialization."""

    def test_to_json_returns_valid_json_string(self):
        """to_json should return a valid JSON string."""
        kg = _build_sample_graph()
        json_str = kg.to_json()
        assert isinstance(json_str, str)
        parsed = json.loads(json_str)
        assert isinstance(parsed, dict)

    def test_to_json_contains_entities(self):
        """JSON output should contain entities data."""
        kg = _build_sample_graph()
        json_str = kg.to_json()
        parsed = json.loads(json_str)
        assert "entities" in parsed
        assert "gene_1" in parsed["entities"]

    def test_to_json_contains_relations(self):
        """JSON output should contain relations data."""
        kg = _build_sample_graph()
        json_str = kg.to_json()
        parsed = json.loads(json_str)
        assert "relations" in parsed
        assert len(parsed["relations"]) == 2


class TestFromJson:
    """Test from_json deserialization."""

    def test_from_json_reconstructs_graph(self):
        """from_json should reconstruct a graph from JSON string."""
        kg = _build_sample_graph()
        json_str = kg.to_json()
        kg2 = KnowledgeGraph.from_json(json_str)
        assert kg2.entities == kg.entities
        assert kg2.relations == kg.relations

    def test_from_json_rebuilds_indexes(self):
        """from_json should rebuild internal indexes."""
        kg = _build_sample_graph()
        json_str = kg.to_json()
        kg2 = KnowledgeGraph.from_json(json_str)
        assert kg2._type_index["Gene"] == {"gene_1", "gene_2"}
        assert "disease_1" in kg2._adj_index["gene_1"]

    def test_from_json_query_works(self):
        """Reconstructed graph from JSON should support query."""
        kg = _build_sample_graph()
        json_str = kg.to_json()
        kg2 = KnowledgeGraph.from_json(json_str)
        results = kg2.query(type="Disease")
        assert len(results) == 1
        assert "disease_1" in results

    def test_from_json_get_neighbors_works(self):
        """Reconstructed graph from JSON should support get_neighbors."""
        kg = _build_sample_graph()
        json_str = kg.to_json()
        kg2 = KnowledgeGraph.from_json(json_str)
        neighbors = kg2.get_neighbors("gene_2")
        assert "disease_1" in neighbors


class TestJsonRoundtrip:
    """Test to_json/from_json roundtrip preserves all data."""

    def test_json_roundtrip_preserves_entities(self):
        """JSON roundtrip should preserve all entity data."""
        kg = _build_sample_graph()
        json_str = kg.to_json()
        kg2 = KnowledgeGraph.from_json(json_str)
        assert kg2.entities == kg.entities

    def test_json_roundtrip_preserves_relations(self):
        """JSON roundtrip should preserve all relation data."""
        kg = _build_sample_graph()
        json_str = kg.to_json()
        kg2 = KnowledgeGraph.from_json(json_str)
        assert kg2.relations == kg.relations

    def test_json_roundtrip_preserves_query_results(self):
        """Query results should be identical after JSON roundtrip."""
        kg = _build_sample_graph()
        json_str = kg.to_json()
        kg2 = KnowledgeGraph.from_json(json_str)
        assert kg2.query(type="Gene") == kg.query(type="Gene")

    def test_json_roundtrip_preserves_neighbors(self):
        """Neighbor sets should be identical after JSON roundtrip."""
        kg = _build_sample_graph()
        json_str = kg.to_json()
        kg2 = KnowledgeGraph.from_json(json_str)
        assert kg2.get_neighbors("gene_1") == kg.get_neighbors("gene_1")
