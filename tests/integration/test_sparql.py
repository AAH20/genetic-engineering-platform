"""TDD tests for SPARQL query interface and graph visualization export."""
from src.integration.knowledge_graph import KnowledgeGraph


class TestSparqlQuery:
    """KnowledgeGraph.query_sparql supports basic SELECT WHERE patterns."""

    def test_simple_select_returns_all_entities(self):
        """SELECT ?s WHERE { ?s type Gene } returns all Gene entities."""
        kg = KnowledgeGraph()
        kg.add_entity("gene_1", "Gene", {"name": "BRCA1"})
        kg.add_entity("gene_2", "Gene", {"name": "TP53"})
        kg.add_entity("disease_1", "Disease", {"name": "Cancer"})

        results = kg.query_sparql("SELECT ?s WHERE { ?s type Gene }")

        assert len(results) == 2
        assert all("s" in r for r in results)
        entity_ids = {r["s"] for r in results}
        assert entity_ids == {"gene_1", "gene_2"}

    def test_type_filter_returns_filtered_results(self):
        """SELECT with type filter returns only matching type."""
        kg = KnowledgeGraph()
        kg.add_entity("gene_1", "Gene", {"name": "BRCA1"})
        kg.add_entity("prot_1", "Protein", {"name": "p53"})
        kg.add_entity("gene_2", "Gene", {"name": "EGFR"})

        results = kg.query_sparql("SELECT ?s WHERE { ?s type Protein }")

        assert len(results) == 1
        assert results[0]["s"] == "prot_1"

    def test_no_matches_returns_empty_list(self):
        """Query with no matching entities returns empty list."""
        kg = KnowledgeGraph()
        kg.add_entity("gene_1", "Gene", {"name": "BRCA1"})

        results = kg.query_sparql("SELECT ?s WHERE { ?s type NonExistent }")

        assert results == []

    def test_select_with_relation_pattern(self):
        """SELECT ?s ?o WHERE { ?s associated_with ?o } returns relation bindings."""
        kg = KnowledgeGraph()
        kg.add_entity("gene_1", "Gene")
        kg.add_entity("disease_1", "Disease")
        kg.add_entity("disease_2", "Disease")
        kg.add_relation("gene_1", "associated_with", "disease_1")
        kg.add_relation("gene_1", "associated_with", "disease_2")

        results = kg.query_sparql("SELECT ?s ?o WHERE { ?s associated_with ?o }")

        assert len(results) == 2
        pairs = {(r["s"], r["o"]) for r in results}
        assert pairs == {("gene_1", "disease_1"), ("gene_1", "disease_2")}

    def test_select_with_fixed_subject(self):
        """SELECT ?o WHERE { gene_1 associated_with ?o } returns targets for fixed subject."""
        kg = KnowledgeGraph()
        kg.add_entity("gene_1", "Gene")
        kg.add_entity("disease_1", "Disease")
        kg.add_entity("disease_2", "Disease")
        kg.add_relation("gene_1", "associated_with", "disease_1")
        kg.add_relation("gene_1", "associated_with", "disease_2")

        results = kg.query_sparql("SELECT ?o WHERE { gene_1 associated_with ?o }")

        assert len(results) == 2
        targets = {r["o"] for r in results}
        assert targets == {"disease_1", "disease_2"}


class TestGraphMlExport:
    """KnowledgeGraph.to_graphml returns valid GraphML XML."""

    def test_to_graphml_returns_valid_xml_string(self):
        """to_graphml returns a string containing valid GraphML XML."""
        kg = KnowledgeGraph()
        kg.add_entity("gene_1", "Gene", {"name": "BRCA1"})
        kg.add_entity("disease_1", "Disease", {"name": "Cancer"})
        kg.add_relation("gene_1", "associated_with", "disease_1")

        result = kg.to_graphml()

        assert isinstance(result, str)
        assert "<?xml" in result
        assert "<graphml" in result
        assert "<graph" in result
        assert "<node" in result
        assert "<edge" in result
        assert "gene_1" in result
        assert "disease_1" in result

    def test_to_graphml_contains_entity_types(self):
        """GraphML output includes entity type information."""
        kg = KnowledgeGraph()
        kg.add_entity("gene_1", "Gene", {"name": "BRCA1"})

        result = kg.to_graphml()

        assert "Gene" in result
        assert "BRCA1" in result


class TestCytoscapeJsonExport:
    """KnowledgeGraph.to_cytoscape_json returns Cytoscape-compatible dict."""

    def test_to_cytoscape_json_returns_dict_with_nodes_and_edges(self):
        """to_cytoscape_json returns dict with 'nodes' and 'edges' keys."""
        kg = KnowledgeGraph()
        kg.add_entity("gene_1", "Gene")
        kg.add_entity("disease_1", "Disease")
        kg.add_relation("gene_1", "associated_with", "disease_1")

        result = kg.to_cytoscape_json()

        assert isinstance(result, dict)
        assert "nodes" in result
        assert "edges" in result
        assert isinstance(result["nodes"], list)
        assert isinstance(result["edges"], list)

    def test_to_cytoscape_json_nodes_have_correct_structure(self):
        """Each node has 'data' with 'id' and 'label'."""
        kg = KnowledgeGraph()
        kg.add_entity("gene_1", "Gene", {"name": "BRCA1"})
        kg.add_entity("disease_1", "Disease", {"name": "Cancer"})

        result = kg.to_cytoscape_json()

        assert len(result["nodes"]) == 2
        for node in result["nodes"]:
            assert "data" in node
            assert "id" in node["data"]
            assert "label" in node["data"]

        labels = {n["data"]["label"] for n in result["nodes"]}
        assert "BRCA1" in labels
        assert "Cancer" in labels

    def test_to_cytoscape_json_edges_have_correct_structure(self):
        """Each edge has 'data' with 'source' and 'target'."""
        kg = KnowledgeGraph()
        kg.add_entity("gene_1", "Gene")
        kg.add_entity("disease_1", "Disease")
        kg.add_relation("gene_1", "associated_with", "disease_1")

        result = kg.to_cytoscape_json()

        assert len(result["edges"]) == 1
        edge = result["edges"][0]
        assert "data" in edge
        assert edge["data"]["source"] == "gene_1"
        assert edge["data"]["target"] == "disease_1"
