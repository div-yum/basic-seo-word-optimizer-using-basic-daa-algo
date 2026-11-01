"""
algorithms.py
Manual implementations of selected DAA algorithms for the SEO Word Optimizer:
1. Binary Search (Keyword lookup in sorted array)
2. Merge Sort and Quick Sort (Keyword frequency ranking & benchmark comparison)
3. Longest Common Subsequence (LCS via Dynamic Programming for draft comparison)
"""

import time
from typing import List, Dict, Any, Tuple


# =====================================================================
# 1. BINARY SEARCH
# =====================================================================

def binary_search_keyword(sorted_keywords: List[Dict[str, Any]], target: str) -> Dict[str, Any]:
    """
    Search for a target word in an alphabetically sorted list of unique keywords.
    Each item in sorted_keywords is a dict: {"word": str, "count": int}.
    
    Time Complexity:
      - Best Case: O(1) [target is at the middle]
      - Average Case: O(log n)
      - Worst Case: O(log n)
    Space Complexity: O(1) auxiliary space (iterative).
    """
    if not target or not isinstance(target, str):
        return {
            "found": False,
            "query": target or "",
            "count": 0,
            "index": -1,
            "comparisons": 0,
            "steps": [],
            "message": "Target search query is empty."
        }

    query = target.strip().lower()
    low = 0
    high = len(sorted_keywords) - 1
    comparisons = 0
    steps = []

    while low <= high:
        comparisons += 1
        mid = (low + high) // 2
        mid_item = sorted_keywords[mid]
        mid_word = mid_item.get("word", "")

        steps.append({
            "step": comparisons,
            "low": low,
            "high": high,
            "mid": mid,
            "mid_word": mid_word
        })

        if mid_word == query:
            return {
                "found": True,
                "query": query,
                "word": mid_word,
                "count": mid_item.get("count", 0),
                "index": mid,
                "comparisons": comparisons,
                "steps": steps,
                "message": f"Keyword '{query}' found at index {mid} with frequency {mid_item.get('count', 0)}."
            }
        elif mid_word < query:
            low = mid + 1
        else:
            high = mid - 1

    return {
        "found": False,
        "query": query,
        "word": None,
        "count": 0,
        "index": -1,
        "comparisons": comparisons,
        "steps": steps,
        "message": f"Keyword '{query}' not found in the extracted unique keywords."
    }


# =====================================================================
# 2. MERGE SORT & QUICK SORT
# =====================================================================

def _compare_keyword_items(a: Dict[str, Any], b: Dict[str, Any]) -> int:
    """
    Compare two keyword items for ranking:
    1. Higher count comes first (descending).
    2. Alphabetical order for ties (ascending).
    
    Returns:
      -1 if a should appear before b (a has higher priority)
       1 if b should appear before a
       0 if identical
    """
    count_a = a.get("count", 0)
    count_b = b.get("count", 0)

    if count_a > count_b:
        return -1
    if count_a < count_b:
        return 1

    # Counts are equal: compare words alphabetically
    word_a = a.get("word", "")
    word_b = b.get("word", "")

    if word_a < word_b:
        return -1
    elif word_a > word_b:
        return 1
    return 0


def merge_sort(items: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """
    Manually implemented Merge Sort for keyword ranking.
    Divides list into two halves, recursively sorts, and merges.
    
    Time Complexity:
      - Best, Average, Worst: O(n log n)
    Space Complexity: O(n) auxiliary memory for merged sublists.
    Stability: Stable.
    """
    if len(items) <= 1:
        return list(items)

    mid = len(items) // 2
    left = merge_sort(items[:mid])
    right = merge_sort(items[mid:])

    # Merge step
    merged = []
    i = 0
    j = 0
    while i < len(left) and j < len(right):
        if _compare_keyword_items(left[i], right[j]) <= 0:
            merged.append(left[i])
            i += 1
        else:
            merged.append(right[j])
            j += 1

    merged.extend(left[i:])
    merged.extend(right[j:])
    return merged


def quick_sort(items: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """
    Manually implemented Quick Sort for keyword ranking using middle pivot.
    Partitions elements into higher priority, equal, and lower priority sublists.
    
    Time Complexity:
      - Best & Average Case: O(n log n)
      - Worst Case: O(n^2) (e.g. extremely unbalanced partitions)
    Space Complexity: O(log n) to O(n) call stack / partition memory.
    """
    if len(items) <= 1:
        return list(items)

    pivot = items[len(items) // 2]
    greater_priority = []
    equal_priority = []
    less_priority = []

    for item in items:
        cmp = _compare_keyword_items(item, pivot)
        if cmp < 0:
            greater_priority.append(item)
        elif cmp == 0:
            equal_priority.append(item)
        else:
            less_priority.append(item)

    return quick_sort(greater_priority) + equal_priority + quick_sort(less_priority)


def compare_sorting_algorithms(
    keyword_freqs: List[Dict[str, Any]],
    repetitions: int = 100
) -> Dict[str, Any]:
    """
    Run Merge Sort and Quick Sort on identical copies of keyword_freqs.
    Measures high-resolution execution time averaged over repeated runs.
    
    Validates that both sorting algorithms produce the identical ordered result.
    """
    if not keyword_freqs:
        return {
            "input_size": 0,
            "repetitions": repetitions,
            "merge_sort": {"avg_time_ms": 0.0, "sorted_data": []},
            "quick_sort": {"avg_time_ms": 0.0, "sorted_data": []},
            "outputs_match": True,
            "message": "Empty keyword list provided."
        }

    n = len(keyword_freqs)
    # Clamp repetitions between 10 and 500 for responsiveness and accuracy
    actual_reps = max(10, min(repetitions, 500))

    # Benchmark Merge Sort
    start_ms = time.perf_counter()
    merge_result = []
    for _ in range(actual_reps):
        copy_data = [dict(item) for item in keyword_freqs]
        merge_result = merge_sort(copy_data)
    total_merge_sec = time.perf_counter() - start_ms
    avg_merge_ms = (total_merge_sec / actual_reps) * 1000.0

    # Benchmark Quick Sort
    start_qs = time.perf_counter()
    quick_result = []
    for _ in range(actual_reps):
        copy_data = [dict(item) for item in keyword_freqs]
        quick_result = quick_sort(copy_data)
    total_qs_sec = time.perf_counter() - start_qs
    avg_qs_ms = (total_qs_sec / actual_reps) * 1000.0

    # Verify both produce identical outputs
    outputs_match = (merge_result == quick_result)

    return {
        "input_size": n,
        "repetitions": actual_reps,
        "merge_sort": {
            "avg_time_ms": round(avg_merge_ms, 5),
            "sorted_data": merge_result
        },
        "quick_sort": {
            "avg_time_ms": round(avg_qs_ms, 5),
            "sorted_data": quick_result
        },
        "outputs_match": outputs_match,
        "explanation": (
            f"Evaluated across {actual_reps} runs on identical copies of {n} keyword items. "
            f"Merge Sort took avg {avg_merge_ms:.5f} ms (O(n log n) worst-case guaranteed). "
            f"Quick Sort took avg {avg_qs_ms:.5f} ms (average O(n log n)). "
            f"Results match strictly: {outputs_match}."
        )
    }


# =====================================================================
# 3. LONGEST COMMON SUBSEQUENCE (LCS) VIA DYNAMIC PROGRAMMING
# =====================================================================

def compute_lcs(tokens1: List[str], tokens2: List[str], max_tokens: int = 1500) -> Dict[str, Any]:
    """
    Compute the Longest Common Subsequence between two word token sequences
    using 2D Dynamic Programming, and reconstruct the retained word sequence.
    
    Time Complexity: O(m * n)
    Space Complexity: O(m * n) for the DP memoization matrix.
    
    Args:
      tokens1: Words in original draft.
      tokens2: Words in revised draft.
      max_tokens: Limit to prevent memory/performance exhaustion on overly large inputs.
    """
    m_orig = len(tokens1)
    n_orig = len(tokens2)

    # Check bounds
    truncated = False
    t1 = tokens1
    t2 = tokens2
    if m_orig > max_tokens or n_orig > max_tokens:
        t1 = tokens1[:max_tokens]
        t2 = tokens2[:max_tokens]
        truncated = True

    m = len(t1)
    n = len(t2)

    if m == 0 or n == 0:
        return {
            "original_word_count": m_orig,
            "revised_word_count": n_orig,
            "lcs_length": 0,
            "lcs_words": [],
            "retained_ratio_original": 0.0,
            "retained_ratio_revised": 0.0,
            "words_removed_approx": m_orig,
            "words_added_approx": n_orig,
            "truncated": truncated,
            "explanation": "One or both drafts contain no words."
        }

    # Initialize (m+1) x (n+1) DP table
    dp = [[0] * (n + 1) for _ in range(m + 1)]

    # Fill DP table
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if t1[i - 1] == t2[j - 1]:
                dp[i][j] = dp[i - 1][j - 1] + 1
            else:
                dp[i][j] = max(dp[i - 1][j], dp[i][j - 1])

    lcs_length = dp[m][n]

    # Reconstruct LCS by backtracking from dp[m][n]
    lcs_words = []
    i, j = m, n
    while i > 0 and j > 0:
        if t1[i - 1] == t2[j - 1]:
            lcs_words.append(t1[i - 1])
            i -= 1
            j -= 1
        elif dp[i - 1][j] >= dp[i][j - 1]:
            i -= 1
        else:
            j -= 1

    lcs_words.reverse()

    # Calculate statistics
    retained_orig = round((lcs_length / m_orig * 100), 2) if m_orig > 0 else 0.0
    retained_rev = round((lcs_length / n_orig * 100), 2) if n_orig > 0 else 0.0
    removed_approx = max(0, m_orig - lcs_length)
    added_approx = max(0, n_orig - lcs_length)

    explanation = (
        f"LCS identified {lcs_length} words retained in identical relative order between the two drafts. "
        f"This accounts for {retained_orig}% of Draft 1 and {retained_rev}% of Draft 2. "
        f"Note: LCS measures sequential token retention, not semantic meaning."
    )

    return {
        "original_word_count": m_orig,
        "revised_word_count": n_orig,
        "lcs_length": lcs_length,
        "lcs_words": lcs_words,
        "retained_ratio_original": retained_orig,
        "retained_ratio_revised": retained_rev,
        "words_removed_approx": removed_approx,
        "words_added_approx": added_approx,
        "truncated": truncated,
        "explanation": explanation
    }
