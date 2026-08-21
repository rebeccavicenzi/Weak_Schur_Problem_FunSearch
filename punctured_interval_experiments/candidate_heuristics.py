"""
Hand-written, deterministic candidate priority functions inspired by
Rafilipojaona (2017)'s punctured-interval structures. No LLM involvement.

All three share the same signature as the repository's existing priority
functions -- priority(i, k, partition) -> float -- so they run unmodified
through harness.solve() (reused from EXP-001) exactly like any evolved
candidate would.

Shared vocabulary (see paper_analysis.md / mapping_to_priority.md):
  - m = min(partition[i]) if non-empty: the color's own anchor value. The
    paper ties block size to exactly this value (Definition 5, 12).
  - "gap" = an integer strictly between a bin's min and its current max
    that is NOT in that bin (Definition 4: at most 2 per structural block).
    Under our sequential solver, gaps are permanent once created (see
    mapping_to_priority.md) -- they can never be "filled" later by the
    same bin, only budgeted for when deciding whether to jump ahead now.

The exact reward magnitudes below (10, 5, 1, -1000, ...) are OUR calibration
choices, not derived from the paper -- flagged explicitly, not claimed as
literature-backed.
"""

MAX_GAPS = 2  # Definition 4: |G| <= 2, hard cap, this part IS paper-derived


def _current_window(sorted_vals, max_gaps):
    """
    Given a bin's sorted elements, find the longest suffix window [r, last]
    (last = sorted_vals[-1]) whose count of missing integers is <= max_gaps.
    This is the bin's "current structural block" in the paper's sense.

    Returns (r, last, gaps_in_window, present_count).
    """
    last = sorted_vals[-1]
    s = set(sorted_vals)
    r = last
    gaps = 0
    while r - 1 >= sorted_vals[0]:
        candidate = r - 1
        if candidate not in s:
            if gaps + 1 > max_gaps:
                break
            gaps += 1
        r = candidate
    present_count = (last - r + 1) - gaps
    return r, last, gaps, present_count


def _prospective_new_gaps(last, k):
    """How many NEW permanent gaps would appear if bin takes k next, given
    its current max is `last`. k > last always holds under our sequential
    solver (see mapping_to_priority.md)."""
    return k - last - 1


def priority_h0_rigid_m_blocking(i: int, k: int, partition: list) -> float:
    """
    H0 -- "Rigid m-blocking."
    Hypothesis under test: does rewarding contiguous growth up to a target
    block length of m (the color's own minimum, per Def. 5/12/Prop. 7),
    WITH ZERO GAP TOLERANCE, produce a useful/structured priority function?
    """
    bin_i = partition[i]
    if not bin_i:
        return -k  # prioritize empty/virgin bins for new colors

    sorted_vals = sorted(bin_i)
    m = sorted_vals[0]
    last = sorted_vals[-1]

    # contiguous run length ending at `last`, ZERO gaps tolerated
    run_len = 1
    idx = len(sorted_vals) - 1
    while idx > 0 and sorted_vals[idx] - sorted_vals[idx - 1] == 1:
        run_len += 1
        idx -= 1

    if k != last + 1:
        # Cannot contiguously extend at all under a zero-gap rule.
        return -(k - last)

    if run_len < m:
        return float(m)  # strongly prefer completing the current block
    return 1.0  # block already reached target size m; mild preference only


def priority_h1_full_mimicry(i: int, k: int, partition: list) -> float:
    """
    H1 -- "Full punctured-interval mimicry."
    Hypothesis under test: does COMBINING block-size-approx-m targeting
    (as in H0) WITH tolerance for up to 2 permanent gaps (Def. 4's exact
    cap) outperform either idea alone (H0, H2)?
    """
    bin_i = partition[i]
    if not bin_i:
        return -k

    sorted_vals = sorted(bin_i)
    m = sorted_vals[0]
    r, last, gaps_in_window, present_count = _current_window(sorted_vals, MAX_GAPS)

    new_gaps = _prospective_new_gaps(last, k)
    total_gaps_if_taken = gaps_in_window + new_gaps

    if total_gaps_if_taken > MAX_GAPS:
        # Would blow the paper's hard |G| <= 2 cap for this block.
        return -1000.0 - new_gaps

    prospective_present = present_count + 1
    size_bonus = float(m) if prospective_present < m else 1.0

    # Reward is reduced the more gap-budget this choice spends now.
    return size_bonus - 2.0 * new_gaps


def priority_h2_gap_tolerance_only(i: int, k: int, partition: list) -> float:
    """
    H2 -- "Gap tolerance only, no explicit m-sized target."
    Hypothesis under test: is the raw <=2-gap-cap mechanic alone (isolated
    from any block-size targeting) already enough to matter, i.e. is the
    m-targeting in H1 doing real work or is the gap tolerance carrying it?
    """
    bin_i = partition[i]
    if not bin_i:
        return -k

    sorted_vals = sorted(bin_i)
    r, last, gaps_in_window, present_count = _current_window(sorted_vals, MAX_GAPS)

    new_gaps = _prospective_new_gaps(last, k)
    total_gaps_if_taken = gaps_in_window + new_gaps

    if total_gaps_if_taken > MAX_GAPS:
        return -1000.0 - new_gaps

    # No comparison to m anywhere -- flat preference for smaller jumps only.
    return 10.0 - new_gaps


CANDIDATES = {
    "H0_rigid_m_blocking": priority_h0_rigid_m_blocking,
    "H1_full_mimicry": priority_h1_full_mimicry,
    "H2_gap_tolerance_only": priority_h2_gap_tolerance_only,
}
