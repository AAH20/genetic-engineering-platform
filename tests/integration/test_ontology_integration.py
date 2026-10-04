"""TDD tests for ontology annotation integration with KnowledgeGraph."""
from src.integration.knowledge_graph import KnowledgeGraph, Ontology


class TestAnnotateWithOntology:
    """KnowledgeGraph.annotate_with_ontology adds ontology terms to entities."""

    def test_annotate_adds_term_to_entity_properties(self):
        """annotate_with_ontology adds 'ontology_term' to entity properties."""
        kg = KnowledgeGraph()
        kg.add_entity("gene_1", "Gene", {"name": "BRCA1"})
        ontology = Ontology()
        ontology.load_ontology("SO")

        kg.annotate_with_ontology("gene_1", ontology, "SO:0000704")

        assert "ontology_term" in kg.entities["gene_1"]["properties"]
        assert "SO:0000704" in kg.entities["gene_1"]["properties"]["ontology_term"]

    def test_annotate_with_invalid_entity_raises_value_error(self):
        """annotate_with_ontology with non-existent entity raises ValueError."""
        kg = KnowledgeGraph()
        ontology = Ontology()
        ontology.load_ontology("SO")

        try:
            kg.annotate_with_ontology("nonexistent", ontology, "SO:0000704")
            assert False, "Expected ValueError"
        except ValueError:
            pass


class TestGetOntologyAnnotations:
    """KnowledgeGraph.get_ontology_annotations returns term IDs for an entity."""

    def test_get_annotations_returns_list_of_terms(self):
        """get_ontology_annotations returns all ontology term IDs for an entity."""
        kg = KnowledgeGraph()
        kg.add_entity("gene_1", "Gene", {"name": "BRCA1"})
        ontology = Ontology()
        ontology.load_ontology("SO")

        kg.annotate_with_ontology("gene_1", ontology, "SO:0000704")
        kg.annotate_with_ontology("gene_1", ontology, "SO:0000110")

        annotations = kg.get_ontology_annotations("gene_1")
        assert isinstance(annotations, list)
        assert "SO:0000704" in annotations
        assert "SO:0000110" in annotations

    def test_get_annotations_with_no_annotations_returns_empty_list(self):
        """get_ontology_annotations returns [] when entity has no annotations."""
        kg = KnowledgeGraph()
        kg.add_entity("gene_1", "Gene", {"name": "BRCA1"})

        annotations = kg.get_ontology_annotations("gene_1")
        assert annotations == []


class TestQueryByOntology:
    """KnowledgeGraph.query_by_ontology returns entities matching a term."""

    def test_query_by_ontology_returns_matching_entities(self):
        """query_by_ontology returns all entities annotated with a given term."""
        kg = KnowledgeGraph()
        kg.add_entity("gene_1", "Gene", {"name": "BRCA1"})
        kg.add_entity("gene_2", "Gene", {"name": "TP53"})
        kg.add_entity("gene_3", "Gene", {"name": "EGFR"})
        ontology = Ontology()
        ontology.load_ontology("SO")

        kg.annotate_with_ontology("gene_1", ontology, "SO:0000704")
        kg.annotate_with_ontology("gene_2", ontology, "SO:0000704")
        kg.annotate_with_ontology("gene_3", ontology, "SO:0000234")

        results = kg.query_by_ontology("SO:0000704")

        assert isinstance(results, dict)
        assert "gene_1" in results
        assert "gene_2" in results
        assert "gene_3" not in results

    def test_query_by_ontology_with_no_matches_returns_empty_dict(self):
        """query_by_ontology returns {} when no entities match the term."""
        kg = KnowledgeGraph()
        kg.add_entity("gene_1", "Gene", {"name": "BRCA1"})
        ontology = Ontology()
        ontology.load_ontology("SO")

        kg.annotate_with_ontology("gene_1", ontology, "SO:0000704")

        results = kg.query_by_ontology("GO:0008150")
        assert results == {}
