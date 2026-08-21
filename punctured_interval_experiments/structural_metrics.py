"""
Post-hoc structural analysis: does a FINISHED partition's color classes
actually resemble Rafilipojaona's punctured-interval structure?

This is deliberately independent of candidate_heuristics.py -- it only looks
at the final partition, not at how it was built, so it can be applied
identically to the baseline, to any of H0/H1/H2, or (per rowley_207_followup.md)
to a future externally supplied partition.

Method: greedily decompose each color class into the fewest possible maximal
windows with at most MAX_GAPS internal gaps each (Definition 4's cap). This
mirrors, as an analysis tool, the same window notion used constructively in
candidate_heuristics.py's H1/H2.
"""

MAX_GAPS = 2


def decompose_into_punctured_intervals(elements, max_gaps=MAX_GAPS):
    """
    Greedily segments a bin's elements into maximal <=max_gaps-gap windows.
    Returns a list of dicts: start, end, size (elements present), gaps, span.
    """
    sorted_e = sorted(elements)
    n = len(sorted_e)
    segments = []
    i = 0
    while i < n:
        start = sorted_e[i]
        j = i
        gaps_used = 0
        while j + 1 < n:
            step = sorted_e[j + 1] - sorted_e[j] - 1  # missing integers between
            if gaps_used + step <= max_gaps:
                gaps_used += step
                j += 1
            else:
                break
        end = sorted_e[j]
        segments.append(
            {
                "start": start,
                "end": end,
                "size": j - i + 1,
                "gaps": gaps_used,
                "span": end - start + 1,
            }
        )
        i = j + 1
    return segments


def analyze_bin(elements):
    """Structural summary for one color class."""
    if not elements:
        return {
            "count": 0,
            "min": None,
            "max": None,
            "num_segments": 0,
            "segments": [],
            "mean_segment_size": None,
            "mean_gaps_per_segment": None,
            "mean_size_to_m_ratio": None,
        }

    sorted_e = sorted(elements)
    m = sorted_e[0]
    segments = decompose_into_punctured_intervals(sorted_e)
    sizes = [s["size"] for s in segments]
    gaps = [s["gaps"] for s in segments]
    size_to_m_ratios = [s["size"] / m for s in segments] if m > 0 else []

    return {
        "count": len(elements),
        "min": sorted_e[0],
        "max": sorted_e[-1],
        "num_segments": len(segments),
        "segments": segments,
        "mean_segment_size": sum(sizes) / len(sizes),
        "mean_gaps_per_segment": sum(gaps) / len(gaps),
        "mean_size_to_m_ratio": (
            sum(size_to_m_ratios) / len(size_to_m_ratios) if size_to_m_ratios else None
        ),
    }


def analyze_partition(partition):
    """
    Structural summary for a whole partition. Lower num_segments (fewer,
    larger blocks) and mean_size_to_m_ratio close to 1.0 both indicate closer
    resemblance to the paper's special-set structure (Definition 12).
    """
    bins = [analyze_bin(b) for b in partition]
    total_elements = sum(b["count"] for b in bins)
    total_segments = sum(b["num_segments"] for b in bins)
    ratios = [b["mean_size_to_m_ratio"] for b in bins if b["mean_size_to_m_ratio"] is not None]

    return {
        "bins": bins,
        "total_elements": total_elements,
        "total_segments": total_segments,
        "elements_per_segment_overall": (
            total_elements / total_segments if total_segments else None
        ),
        "mean_size_to_m_ratio_overall": (sum(ratios) / len(ratios) if ratios else None),
    }
