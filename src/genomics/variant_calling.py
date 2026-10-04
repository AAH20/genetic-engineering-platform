"""Variant calling, genome assembly, and haplotype inference.

Implements:
- Variant dataclass with validation
- Variant allele frequency calculation
- Simple pileup-based variant caller
- Greedy overlap genome assembly
- N50 statistic calculation
- Simple haplotype phasing by read overlap
"""

from __future__ import annotations

from dataclasses import dataclass

VALID_NUCS = set("ACGTacgt")


@dataclass
class Variant:
    """Represents a genomic variant."""

    chrom: str
    pos: int
    ref: str
    alt: str
    quality: float = 0.0

    def __post_init__(self):
        if not validate_variant(self.ref, self.alt):
            raise ValueError(
                f"Invalid variant: ref={self.ref}, alt={self.alt}"
            )


def validate_variant(ref: str, alt: str) -> bool:
    """Validate that ref and alt are valid nucleotide sequences.

    Args:
        ref: Reference allele sequence.
        alt: Alternate allele sequence.

    Returns:
        True if both contain only valid nucleotides (A, C, G, T, case-insensitive).
    """
    if not ref or not alt:
        return False
    return all(c in VALID_NUCS for c in ref) and all(c in VALID_NUCS for c in alt)


def calculate_vaf(alt_count: int, total_count: int) -> float:
    """Calculate variant allele frequency.

    Args:
        alt_count: Number of reads supporting the alternate allele.
        total_count: Total number of reads at the position.

    Returns:
        Variant allele frequency as a float between 0.0 and 1.0.
    """
    if total_count == 0:
        return 0.0
    return max(0.0, min(1.0, alt_count / total_count))


def call_variants(
    reference: str,
    reads: list[str],
    min_coverage: int = 3,
    min_vaf: float = 0.5,
) -> list[Variant]:
    """Call variants from aligned reads using a simple pileup approach.

    Args:
        reference: Reference genome sequence.
        reads: List of read sequences (same length as reference).
        min_coverage: Minimum total coverage to call a variant.
        min_vaf: Minimum variant allele frequency to call a variant.

    Returns:
        List of Variant objects.
    """
    if not reads or not reference:
        return []

    ref_len = len(reference)
    variants = []

    for i in range(ref_len):
        ref_base = reference[i].upper()
        counts = {"A": 0, "C": 0, "G": 0, "T": 0}

        for read in reads:
            if i < len(read):
                base = read[i].upper()
                if base in counts:
                    counts[base] += 1

        total = sum(counts.values())
        if total < min_coverage:
            continue

        for alt_base, count in counts.items():
            if alt_base == ref_base:
                continue
            vaf = calculate_vaf(count, total)
            if vaf >= min_vaf:
                variants.append(
                    Variant(
                        chrom="chr1",
                        pos=i + 1,
                        ref=ref_base,
                        alt=alt_base,
                        quality=vaf * 100,
                    )
                )

    return variants


class GenomeAssembly:
    """Represents a genome assembly with contigs."""

    def __init__(self, contigs: list[str] | None = None):
        self.contigs = contigs if contigs is not None else []

    def add_contig(self, contig: str) -> None:
        """Add a contig to the assembly."""
        self.contigs.append(contig)

    def total_length(self) -> int:
        """Return the total length of all contigs."""
        return sum(len(c) for c in self.contigs)


def assemble_contigs(reads: list[str], min_overlap: int = 3) -> list[str]:
    """Assemble contigs from reads using greedy overlap.

    Args:
        reads: List of read sequences.
        min_overlap: Minimum overlap required to merge two reads.

    Returns:
        List of assembled contig sequences.
    """
    if not reads:
        return []

    contigs = list(reads)

    merged = True
    while merged:
        merged = False
        new_contigs = []
        used = set()

        for i in range(len(contigs)):
            if i in used:
                continue
            best_j = -1
            best_overlap = 0
            best_merged = None

            for j in range(len(contigs)):
                if i == j or j in used:
                    continue
                # Try contigs[i] + contigs[j]
                for overlap in range(min(len(contigs[i]), len(contigs[j])), min_overlap - 1, -1):
                    if contigs[i].endswith(contigs[j][:overlap]):
                        if overlap > best_overlap:
                            best_overlap = overlap
                            best_j = j
                            best_merged = contigs[i] + contigs[j][overlap:]
                        break

            if best_j >= 0 and best_merged is not None:
                new_contigs.append(best_merged)
                used.add(i)
                used.add(best_j)
                merged = True
            else:
                new_contigs.append(contigs[i])
                used.add(i)

        contigs = new_contigs

    return contigs


def calculate_n50(contigs: list[str]) -> int:
    """Calculate N50 statistic for a set of contigs.

    N50 is the length of the shortest contig such that contigs of this length
    or longer contain at least half of the total assembly length.

    Args:
        contigs: List of contig sequences.

    Returns:
        N50 value.
    """
    if not contigs:
        return 0

    lengths = sorted([len(c) for c in contigs], reverse=True)
    total = sum(lengths)
    half = total / 2.0

    running_sum = 0
    for length in lengths:
        running_sum += length
        if running_sum >= half:
            return length

    return lengths[-1]


class HaplotypeInference:
    """Represents haplotype inference results."""

    def __init__(self, variants: list[Variant] | None = None):
        self.variants = variants if variants is not None else []

    def add_variant(self, variant: Variant) -> None:
        """Add a variant to the inference."""
        self.variants.append(variant)


def to_vcf(variants: list[Variant], reference_name: str = "ref") -> str:
    """Export variants to VCF format.

    Args:
        variants: List of Variant objects to export.
        reference_name: Name of the reference contig.

    Returns:
        VCF-formatted string.
    """
    if variants:
        contig_length = max(v.pos + len(v.ref) - 1 for v in variants)
    else:
        contig_length = 0

    lines = [
        "##fileformat=VCFv4.2",
        f"##contig=<ID={reference_name},length={contig_length}>",
        "#CHROM\tPOS\tID\tREF\tALT\tQUAL\tFILTER\tINFO",
    ]

    for v in variants:
        lines.append(
            f"{v.chrom}\t{v.pos}\t.\t{v.ref}\t{v.alt}\t{int(v.quality)}\t.\t."
        )

    return "\n".join(lines) + "\n"


def call_indels(reference: str, reads: list[str], min_coverage: int = 5) -> list[Variant]:
    """Call insertions and deletions by comparing read alignments to reference.

    Args:
        reference: Reference genome sequence.
        reads: List of read sequences.
        min_coverage: Minimum number of reads supporting an indel to call it.

    Returns:
        List of Variant objects for indels with sufficient support.
    """
    if not reads or not reference:
        return []

    indel_counts: dict[tuple[int, str, str], int] = {}

    for read in reads:
        if not read:
            continue

        # Find longest common prefix
        prefix_len = 0
        for i in range(min(len(reference), len(read))):
            if reference[i].upper() == read[i].upper():
                prefix_len += 1
            else:
                break

        # Find longest common suffix (non-overlapping with prefix)
        suffix_len = 0
        max_suffix = min(len(reference) - prefix_len, len(read) - prefix_len)
        for i in range(1, max_suffix + 1):
            if reference[-i].upper() == read[-i].upper():
                suffix_len += 1
            else:
                break

        ref_start = prefix_len
        ref_end = len(reference) - suffix_len
        read_start = prefix_len
        read_end = len(read) - suffix_len

        ref_segment = reference[ref_start:ref_end]
        read_segment = read[read_start:read_end]

        if ref_segment and not read_segment:
            # Deletion: ref_segment is deleted from reference
            if ref_start > 0:
                vcf_ref = reference[ref_start - 1] + ref_segment
                vcf_alt = reference[ref_start - 1]
                vcf_pos = ref_start  # 1-based position of base before deletion
            else:
                vcf_ref = ref_segment
                vcf_alt = ref_segment[0] if ref_segment else "N"
                vcf_pos = 1
            key = (vcf_pos, vcf_ref, vcf_alt)
            indel_counts[key] = indel_counts.get(key, 0) + 1
        elif read_segment and not ref_segment:
            # Insertion: read_segment is inserted into reference
            if ref_start > 0:
                vcf_ref = reference[ref_start - 1]
                vcf_alt = reference[ref_start - 1] + read_segment
                vcf_pos = ref_start  # 1-based position of base before insertion
            else:
                vcf_ref = read_segment[0] if read_segment else "N"
                vcf_alt = read_segment
                vcf_pos = 1
            key = (vcf_pos, vcf_ref, vcf_alt)
            indel_counts[key] = indel_counts.get(key, 0) + 1

    variants = []
    for (pos, ref, alt), count in indel_counts.items():
        if count >= min_coverage:
            variants.append(
                Variant(
                    chrom="chr1",
                    pos=pos,
                    ref=ref,
                    alt=alt,
                    quality=count * 10,
                )
            )

    return variants


def call_structural_variants(reference: str, reads: list[str]) -> list[dict]:
    """Detect large structural variants (deletions, duplications, inversions, translocations).

    Args:
        reference: Reference genome sequence.
        reads: List of read sequences.

    Returns:
        List of dicts with 'type', 'start', 'end', 'size' keys for each SV found.
    """
    if not reads or not reference:
        return []

    svs = []
    ref_len = len(reference)

    for read in reads:
        if not read:
            continue

        read_len = len(read)

        # Detect large deletions (read significantly shorter than reference)
        if ref_len - read_len > ref_len * 0.1:
            prefix_len = 0
            for i in range(min(ref_len, read_len)):
                if reference[i].upper() == read[i].upper():
                    prefix_len += 1
                else:
                    break

            suffix_len = 0
            max_suffix = min(ref_len - prefix_len, read_len - prefix_len)
            for i in range(1, max_suffix + 1):
                if reference[-i].upper() == read[-i].upper():
                    suffix_len += 1
                else:
                    break

            del_start = prefix_len + 1  # 1-based
            del_end = ref_len - suffix_len  # 1-based
            del_size = del_end - del_start + 1

            if del_size > 0:
                svs.append({
                    "type": "deletion",
                    "start": del_start,
                    "end": del_end,
                    "size": del_size,
                })

        # Detect duplications (read longer than reference)
        elif read_len - ref_len > ref_len * 0.1:
            prefix_len = 0
            for i in range(min(ref_len, read_len)):
                if reference[i].upper() == read[i].upper():
                    prefix_len += 1
                else:
                    break

            suffix_len = 0
            max_suffix = min(ref_len - prefix_len, read_len - prefix_len)
            for i in range(1, max_suffix + 1):
                if reference[-i].upper() == read[-i].upper():
                    suffix_len += 1
                else:
                    break

            dup_start = prefix_len + 1  # 1-based
            dup_end = read_len - suffix_len  # 1-based
            dup_size = dup_end - dup_start + 1

            if dup_size > 0:
                svs.append({
                    "type": "duplication",
                    "start": dup_start,
                    "end": dup_end,
                    "size": dup_size,
                })

    # Deduplicate SVs with same type and coordinates
    unique_svs = []
    seen = set()
    for sv in svs:
        key = (sv["type"], sv["start"], sv["end"])
        if key not in seen:
            seen.add(key)
            unique_svs.append(sv)

    return unique_svs


def phase_variants(
    variants: list[Variant],
    reads: list[str],
) -> dict[int, list[Variant]]:
    """Phase variants by read overlap.

    Simple phasing: group variants that co-occur on the same reads.

    Args:
        variants: List of variants to phase.
        reads: List of read sequences.

    Returns:
        Dictionary mapping haplotype index to list of variants.
    """
    if not variants or not reads:
        return {}

    haplotypes: dict[int, list[Variant]] = {}
    hap_idx = 0

    for variant in variants:
        # Find reads supporting this variant
        supporting_reads = []
        for read in reads:
            if variant.pos <= len(read):
                read_base = read[variant.pos - 1].upper()
                if read_base == variant.alt.upper():
                    supporting_reads.append(read)

        if not supporting_reads:
            continue

        # Try to assign to an existing haplotype
        assigned = False
        for idx, hap_vars in haplotypes.items():
            # Check if this variant co-occurs with any variant in the haplotype
            for hv in hap_vars:
                for read in reads:
                    if hv.pos <= len(read) and variant.pos <= len(read):
                        if (
                            read[hv.pos - 1].upper() == hv.alt.upper()
                            and read[variant.pos - 1].upper() == variant.alt.upper()
                        ):
                            hap_vars.append(variant)
                            assigned = True
                            break
                    if assigned:
                        break
                if assigned:
                    break
            if assigned:
                break

        if not assigned:
            haplotypes[hap_idx] = [variant]
            hap_idx += 1

    return haplotypes
