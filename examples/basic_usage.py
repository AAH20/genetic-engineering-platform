"""Examples for Genetic Engineering Platform."""

from src.crispr.grna_design import design_grna, GuideRNA
from src.biosecurity.screening import BiosecurityGate
from src.integration.knowledge_graph import KnowledgeGraph


def example_crispr():
    """Example 1: CRISPR Guide RNA Design."""
    target = "GAGTCCGAGCAGAAGAAGAAGGG"
    result = design_grna(target, pam="NGG")
    if result:
        grna = GuideRNA(
            sequence=result["sequence"],
            efficiency=result["efficiency"],
            off_targets=result["off_targets"],
        )
        print("gRNA:", grna.sequence)
        print("Efficiency:", grna.efficiency)
        print("GC Content:", grna.gc_content)


def example_biosecurity():
    """Example 2: Biosecurity Screening."""
    gate = BiosecurityGate()
    seq = "GAGTCCGAGCAGAAGAAGAA"
    if gate.evaluate(seq):
        print("Sequence passed biosecurity screening")


def example_knowledge_graph():
    """Example 3: Knowledge Graph Query."""
    kg = KnowledgeGraph()
    kg.add_entity("gene1", "Gene", {"name": "BRCA1"})
    kg.add_entity("disease1", "Disease", {"name": "Breast Cancer"})
    kg.add_relation("gene1", "associated_with", "disease1")
    neighbors = kg.get_neighbors("gene1")
    for n in neighbors:
        print("  ", n["id"], n["type"], n["properties"])


def example_full_pipeline():
    """Example 4: Full Pipeline."""
    target = "GAGTCCGAGCAGAAGAAGAAGGG"
    design = design_grna(target, pam="NGG")
    gate = BiosecurityGate()
    if design and gate.evaluate(design["sequence"]):
        kg = KnowledgeGraph()
        kg.add_entity("grna1", "GuideRNA", {
            "sequence": design["sequence"],
            "efficiency": design["efficiency"],
            "target": target,
        })
        print("Design complete:", design["sequence"])
        print("Efficiency:", design["efficiency"])
    else:
        print("Design failed biosecurity screening")


if __name__ == "__main__":
    print("=== CRISPR Design ===")
    example_crispr()
    print("\n=== Biosecurity Screening ===")
    example_biosecurity()
    print("\n=== Knowledge Graph ===")
    example_knowledge_graph()
    print("\n=== Full Pipeline ===")
    example_full_pipeline()
