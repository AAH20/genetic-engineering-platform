"""Biosecurity screening: sequence screening, dual-use detection, compliance, and gating."""
from __future__ import annotations

from typing import Any

# Known threat sequence patterns (simplified motifs for screening)
THREAT_PATTERNS: dict[str, str] = {
    "botulinum_neurotoxin_light_chain": "GAGCTGCTGGACTTCGCT",
    "ricin_chain_A": "ATCGAGCTGCTGGACTTCGCT",
    "tetrodotoxin_binding": "TTCGCTGCTGCTGCTGCTGC",
    "anthrax_lethal_factor": "GCTATCGAGCTGCTGGACTTC",
    "cholera_toxin_A": "GCTGCTGGACTTCGCTATCGAG",
    "diphtheria_toxin": "CTGCTGGACTTCGCTATCGAGCTG",
    "shiga_toxin": "GAGCTGCTGGACTTCGCTATCGAGCT",
    "pertussis_toxin": "ATCGAGCTGCTGGACTTCGCTATCGAG",
}

# Dual-use concern patterns
DUAL_USE_PATTERNS: dict[str, str] = {
    "virulence_factor": "GCTATCGAGCTGCTGGACTTC",
    "toxin_related": "TTCGCTGCTGCTGCTGCTGC",
    "antibiotic_resistance_marker": "GAGCTGCTGGACTTCGCT",
    "immune_evasion": "ATCGAGCTGCTGGACTTCGCT",
    "host_cell_entry": "CTGCTGGACTTCGCTATCGAGCTG",
}

# Regulatory frameworks
REGULATORY_FRAMEWORKS: dict[str, dict[str, Any]] = {
    "NIH": {
        "name": "NIH Guidelines for Recombinant/Synthetic Nucleic Acid Research",
        "risk_threshold": 0.6,
        "requires_review_above": 0.3,
    },
    "WHO": {
        "name": "WHO Laboratory Biosafety Manual",
        "risk_threshold": 0.5,
        "requires_review_above": 0.25,
    },
    "CDC": {
        "name": "CDC Biosafety in Microbiological and Biomedical Laboratories",
        "risk_threshold": 0.7,
        "requires_review_above": 0.35,
    },
}


class SequenceScreener:
    """Screen DNA sequences against known threat patterns."""

    def __init__(self) -> None:
        self.threat_patterns = THREAT_PATTERNS

    def screen_sequence(self, sequence: str) -> dict[str, Any]:
        """Check sequence against known threat patterns.

        Returns dict with:
            is_clean: bool - True if no threat patterns found
            matches: list[str] - names of matched threat patterns
        """
        if not sequence:
            return {"is_clean": True, "matches": []}

        seq_upper = sequence.upper()
        matches: list[str] = []

        for name, pattern in self.threat_patterns.items():
            if pattern in seq_upper:
                matches.append(name)

        return {
            "is_clean": len(matches) == 0,
            "matches": matches,
        }

    def calculate_risk_score(self, sequence: str) -> float:
        """Calculate a 0-1 risk score for a sequence.

        Score is based on:
            - Number of threat pattern matches
            - GC content deviation from normal (50%)
            - Sequence length (very short or very long sequences score higher)
        """
        if not sequence:
            return 0.0

        seq_upper = sequence.upper()
        score = 0.0

        # Threat pattern contribution (up to 0.6)
        threat_count = 0
        for pattern in self.threat_patterns.values():
            if pattern in seq_upper:
                threat_count += 1
        score += min(threat_count * 0.2, 0.6)

        # GC content deviation (up to 0.2)
        gc_count = seq_upper.count("G") + seq_upper.count("C")
        gc_content = gc_count / len(seq_upper) if seq_upper else 0.0
        gc_deviation = abs(gc_content - 0.5)
        score += min(gc_deviation * 0.4, 0.2)

        # Length anomaly (up to 0.2)
        seq_len = len(sequence)
        if seq_len < 20:
            score += 0.1
        elif seq_len > 10000:
            score += 0.1

        return min(score, 1.0)

    def check_homology(self, sequence: str, reference: str) -> dict[str, Any]:
        """Check homology between a sequence and a reference.

        Uses a simple k-mer based approach:
            - Extract k-mers (k=8) from both sequences
            - Calculate Jaccard similarity

        Returns dict with:
            homology: float - 0.0 to 1.0 similarity score
            is_homologous: bool - True if homology >= 0.7
        """
        if not sequence or not reference:
            return {"homology": 0.0, "is_homologous": False}

        k = 8
        seq_upper = sequence.upper()
        ref_upper = reference.upper()

        if len(seq_upper) < k or len(ref_upper) < k:
            return {"homology": 0.0, "is_homologous": False}

        # Extract k-mers
        seq_kmers = {seq_upper[i:i+k] for i in range(len(seq_upper) - k + 1)}
        ref_kmers = {ref_upper[i:i+k] for i in range(len(ref_upper) - k + 1)}

        # Jaccard similarity
        intersection = seq_kmers & ref_kmers
        union = seq_kmers | ref_kmers

        homology = len(intersection) / len(union) if union else 0.0

        return {
            "homology": round(homology, 4),
            "is_homologous": homology >= 0.7,
        }


class DualUseDetector:
    """Detect potential dual-use DNA sequences."""

    def __init__(self) -> None:
        self.dual_use_patterns = DUAL_USE_PATTERNS

    def detect_dual_use(self, sequence: str) -> dict[str, Any]:
        """Flag potential dual-use sequences.

        Returns dict with:
            is_dual_use: bool - True if any dual-use patterns found
            flags: list[str] - names of matched dual-use patterns
        """
        if not sequence:
            return {"is_dual_use": False, "flags": []}

        seq_upper = sequence.upper()
        flags: list[str] = []

        for name, pattern in self.dual_use_patterns.items():
            if pattern in seq_upper:
                flags.append(name)

        return {
            "is_dual_use": len(flags) > 0,
            "flags": flags,
        }

    def classify_risk_level(self, risk_score: float) -> str:
        """Classify risk level from a 0-1 risk score.

        Levels:
            Low: 0.0 - 0.3
            Medium: 0.3 - 0.6
            High: 0.6 - 0.85
            Extreme: 0.85 - 1.0
        """
        if risk_score < 0.0:
            risk_score = 0.0
        if risk_score > 1.0:
            risk_score = 1.0

        if risk_score < 0.3:
            return "Low"
        elif risk_score < 0.6:
            return "Medium"
        elif risk_score < 0.85:
            return "High"
        else:
            return "Extreme"


class ComplianceChecker:
    """Verify sequences against regulatory frameworks."""

    def __init__(self) -> None:
        self.frameworks = REGULATORY_FRAMEWORKS
        self.screener = SequenceScreener()
        self.dual_use_detector = DualUseDetector()

    def check_compliance(self, sequence: str, framework: str = "NIH") -> dict[str, Any]:
        """Verify sequence against a regulatory framework.

        Returns dict with:
            compliant: bool - True if sequence passes compliance
            violations: list[str] - descriptions of violations
            framework: str - the framework checked against
        """
        if not sequence:
            return {"compliant": True, "violations": [], "framework": framework}

        if framework not in self.frameworks:
            return {
                "compliant": False,
                "violations": [f"Unknown regulatory framework: {framework}"],
                "framework": framework,
            }

        violations: list[str] = []
        config = self.frameworks[framework]

        # Check threat patterns
        screening = self.screener.screen_sequence(sequence)
        if not screening["is_clean"]:
            for match in screening["matches"]:
                violations.append(f"Threat pattern detected: {match}")

        # Check dual-use
        dual_use = self.dual_use_detector.detect_dual_use(sequence)
        if dual_use["is_dual_use"]:
            for flag in dual_use["flags"]:
                violations.append(f"Dual-use concern: {flag}")

        # Check risk score against framework threshold
        risk_score = self.screener.calculate_risk_score(sequence)
        if risk_score > config["risk_threshold"]:
            violations.append(
                f"Risk score {risk_score:.2f} exceeds {framework} threshold "
                f"({config['risk_threshold']})"
            )

        return {
            "compliant": len(violations) == 0,
            "violations": violations,
            "framework": framework,
        }

    def generate_report(self, sequence: str, framework: str = "NIH") -> dict[str, Any]:
        """Generate a compliance report for a sequence.

        Returns dict with:
            sequence_length: int
            framework: str
            compliant: bool
            violations: list[str]
            risk_score: float
            risk_level: str
            screening_result: dict
            dual_use_result: dict
        """
        compliance = self.check_compliance(sequence, framework=framework)
        risk_score = self.screener.calculate_risk_score(sequence)
        risk_level = self.dual_use_detector.classify_risk_level(risk_score)
        screening = self.screener.screen_sequence(sequence)
        dual_use = self.dual_use_detector.detect_dual_use(sequence)

        return {
            "sequence_length": len(sequence),
            "framework": framework,
            "compliant": compliance["compliant"],
            "violations": compliance["violations"],
            "risk_score": round(risk_score, 4),
            "risk_level": risk_level,
            "screening_result": screening,
            "dual_use_result": dual_use,
        }


class BiosecurityGate:
    """Gate that evaluates sequences for biosecurity compliance."""

    def __init__(self) -> None:
        self.screener = SequenceScreener()
        self.dual_use_detector = DualUseDetector()
        self.compliance_checker = ComplianceChecker()

    def evaluate(self, sequence: str, framework: str = "NIH") -> dict[str, Any]:
        """Evaluate a sequence through the biosecurity gate.

        Returns dict with:
            passed: bool - True if sequence passes all checks
            risk_level: str - Low/Medium/High/Extreme
            risk_score: float - 0-1 risk score
            screening_result: dict
            dual_use_result: dict
            compliance_result: dict
        """
        if not sequence:
            return {
                "passed": True,
                "risk_level": "Low",
                "risk_score": 0.0,
                "screening_result": {"is_clean": True, "matches": []},
                "dual_use_result": {"is_dual_use": False, "flags": []},
                "compliance_result": {"compliant": True, "violations": []},
            }

        screening = self.screener.screen_sequence(sequence)
        dual_use = self.dual_use_detector.detect_dual_use(sequence)
        compliance = self.compliance_checker.check_compliance(sequence, framework=framework)
        risk_score = self.screener.calculate_risk_score(sequence)
        risk_level = self.dual_use_detector.classify_risk_level(risk_score)

        # Gate passes if: no threat matches, no dual-use flags, and compliant
        passed = (
            screening["is_clean"]
            and not dual_use["is_dual_use"]
            and compliance["compliant"]
        )

        return {
            "passed": passed,
            "risk_level": risk_level,
            "risk_score": round(risk_score, 4),
            "screening_result": screening,
            "dual_use_result": dual_use,
            "compliance_result": compliance,
        }
