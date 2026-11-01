"""
tests/test_algorithms.py
Unit tests for Binary Search, Merge Sort, Quick Sort, and LCS.
"""

import pytest
from algorithms import (
    binary_search_keyword,
    merge_sort,
    quick_sort,
    compare_sorting_algorithms,
    compute_lcs
)


# =====================================================================
# BINARY SEARCH TESTS
# =====================================================================

def test_binary_search_empty():
    res = binary_search_keyword([], "cybersecurity")
    assert res["found"] is False
    assert res["index"] == -1
    assert res["comparisons"] == 0

    res2 = binary_search_keyword([{"word": "test", "count": 1}], "")
    assert res2["found"] is False
    assert res2["index"] == -1


def test_binary_search_single_item():
    items = [{"word": "python", "count": 5}]
    res_found = binary_search_keyword(items, "python")
    assert res_found["found"] is True
    assert res_found["index"] == 0
    assert res_found["count"] == 5

    res_missing = binary_search_keyword(items, "java")
    assert res_missing["found"] is False
    assert res_missing["index"] == -1


def test_binary_search_normal_and_case():
    items = [
        {"word": "algorithm", "count": 3},
        {"word": "binary", "count": 1},
        {"word": "dynamic", "count": 4},
        {"word": "graph", "count": 2},
        {"word": "search", "count": 5},
        {"word": "tree", "count": 2}
    ]
    # Beginning
    res1 = binary_search_keyword(items, "algorithm")
    assert res1["found"] is True
    assert res1["index"] == 0

    # Middle
    res2 = binary_search_keyword(items, "DYNAMIC")
    assert res2["found"] is True
    assert res2["index"] == 2
    assert res2["count"] == 4

    # End
    res3 = binary_search_keyword(items, "Tree")
    assert res3["found"] is True
    assert res3["index"] == 5

    # Not found
    res4 = binary_search_keyword(items, "sorting")
    assert res4["found"] is False
    assert res4["index"] == -1
    assert len(res4["steps"]) > 0


# =====================================================================
# MERGE SORT & QUICK SORT TESTS
# =====================================================================

def test_sorting_empty_and_single():
    assert merge_sort([]) == []
    assert quick_sort([]) == []

    single = [{"word": "code", "count": 1}]
    assert merge_sort(single) == single
    assert quick_sort(single) == single


def test_sorting_tie_breaking_alphabetical():
    # When frequencies are equal, alphabetical order applies
    items = [
        {"word": "delta", "count": 2},
        {"word": "alpha", "count": 2},
        {"word": "beta", "count": 5},
        {"word": "gamma", "count": 2}
    ]
    # Expected: beta (count 5), then alpha, delta, gamma (count 2 each, alphabetical)
    expected = [
        {"word": "beta", "count": 5},
        {"word": "alpha", "count": 2},
        {"word": "delta", "count": 2},
        {"word": "gamma", "count": 2}
    ]

    res_merge = merge_sort(items)
    res_quick = quick_sort(items)

    assert res_merge == expected
    assert res_quick == expected
    assert res_merge == res_quick


def test_merge_and_quick_sort_produce_identical_output():
    import random
    words = ["seo", "optimization", "ranking", "search", "engine", "google", "meta", "title", "content", "speed"]
    items = [{"word": w, "count": random.randint(1, 10)} for w in words]

    merge_out = merge_sort(items)
    quick_out = quick_sort(items)

    assert merge_out == quick_out
    # Check descending order
    for i in range(len(merge_out) - 1):
        assert (merge_out[i]["count"] > merge_out[i + 1]["count"]) or (
            merge_out[i]["count"] == merge_out[i + 1]["count"] and merge_out[i]["word"] <= merge_out[i + 1]["word"]
        )


def test_compare_sorting_benchmark():
    items = [
        {"word": f"word{i}", "count": (i * 7) % 13}
        for i in range(30)
    ]
    bench = compare_sorting_algorithms(items, repetitions=20)
    assert bench["input_size"] == 30
    assert bench["repetitions"] == 20
    assert bench["outputs_match"] is True
    assert bench["merge_sort"]["avg_time_ms"] >= 0.0
    assert bench["quick_sort"]["avg_time_ms"] >= 0.0
    assert len(bench["merge_sort"]["sorted_data"]) == 30


# =====================================================================
# LCS TESTS
# =====================================================================

def test_lcs_empty():
    res = compute_lcs([], [])
    assert res["lcs_length"] == 0
    assert res["lcs_words"] == []

    res2 = compute_lcs(["word"], [])
    assert res2["lcs_length"] == 0


def test_lcs_identical():
    tokens = ["the", "quick", "brown", "fox"]
    res = compute_lcs(tokens, tokens)
    assert res["lcs_length"] == 4
    assert res["lcs_words"] == tokens
    assert res["retained_ratio_original"] == 100.0


def test_lcs_completely_different():
    t1 = ["apple", "banana"]
    t2 = ["orange", "grape"]
    res = compute_lcs(t1, t2)
    assert res["lcs_length"] == 0
    assert res["lcs_words"] == []


def test_lcs_order_validation():
    # Draft 1: "seo tools help students improve content"
    # Draft 2: "good seo tools help all students create better content"
    t1 = ["seo", "tools", "help", "students", "improve", "content"]
    t2 = ["good", "seo", "tools", "help", "all", "students", "create", "better", "content"]

    res = compute_lcs(t1, t2)
    assert res["lcs_words"] == ["seo", "tools", "help", "students", "content"]
    assert res["lcs_length"] == 5

    # Verify that lcs_words appears in order in both t1 and t2
    def is_subsequence(sub, full):
        it = iter(full)
        return all(item in it for item in sub)

    assert is_subsequence(res["lcs_words"], t1)
    assert is_subsequence(res["lcs_words"], t2)
