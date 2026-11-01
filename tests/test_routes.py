"""
tests/test_routes.py
Comprehensive integration tests for Flask API routes.
"""

import pytest
from app import app, MAX_TEXT_LENGTH


@pytest.fixture
def client():
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client


def test_health_check(client):
    response = client.get("/api/health")
    assert response.status_code == 200
    data = response.get_json()
    assert data["status"] == "healthy"
    assert data["service"] == "SEO Word Optimizer"


def test_index_route(client):
    response = client.get("/")
    assert response.status_code == 200
    assert b"SEO Word Optimizer" in response.data


def test_analyze_route_success(client):
    payload = {
        "title": "Best Cybersecurity Tools for Beginners",
        "target_keyword": "cybersecurity tools",
        "intro": "Cybersecurity tools help students learn network defense and security testing.",
        "headings": "Top cybersecurity tools\nHow to choose security tools",
        "body": "Cybersecurity tools help students understand network security. These tools can support monitoring."
    }
    response = client.post("/api/analyze", json=payload)
    assert response.status_code == 200
    data = response.get_json()
    assert data["status"] == "success"
    analysis = data["data"]
    assert analysis["metrics"]["word_count"] > 0
    assert analysis["metrics"]["target_keyword"] == "cybersecurity tools"
    assert analysis["presence"]["title_has_keyword"] is True
    assert analysis["presence"]["intro_has_keyword"] is True
    assert len(analysis["filtered_frequencies"]) > 0


def test_analyze_route_invalid_payload(client):
    # Not JSON
    res = client.post("/api/analyze", data="plain text")
    assert res.status_code == 400

    # Wrong type
    res2 = client.post("/api/analyze", json={"body": 12345})
    assert res2.status_code == 400
    assert "must be a string" in res2.get_json()["error"]


def test_analyze_route_exceeds_max_length(client):
    huge_text = "a" * (MAX_TEXT_LENGTH + 10)
    res = client.post("/api/analyze", json={"body": huge_text})
    assert res.status_code == 400
    assert "exceeds maximum allowed length" in res.get_json()["error"]


def test_search_keyword_route(client):
    keywords = [
        {"word": "algorithms", "count": 3},
        {"word": "data", "count": 2},
        {"word": "structure", "count": 1}
    ]
    # Found
    res = client.post("/api/search-keyword", json={"query": "data", "keywords": keywords})
    assert res.status_code == 200
    result = res.get_json()["data"]["search_result"]
    assert result["found"] is True
    assert result["word"] == "data"
    assert result["count"] == 2

    # Not found
    res2 = client.post("/api/search-keyword", json={"query": "network", "keywords": keywords})
    assert res2.status_code == 200
    result2 = res2.get_json()["data"]["search_result"]
    assert result2["found"] is False

    # Empty query validation
    res_err = client.post("/api/search-keyword", json={"query": "", "keywords": keywords})
    assert res_err.status_code == 400


def test_search_keyword_with_body_fallback(client):
    res = client.post("/api/search-keyword", json={
        "query": "learning",
        "body": "Cybersecurity tools help students with continuous learning."
    })
    assert res.status_code == 200
    result = res.get_json()["data"]["search_result"]
    assert result["found"] is True
    assert result["word"] == "learning"


def test_sort_comparison_route(client):
    frequencies = [
        {"word": "python", "count": 5},
        {"word": "flask", "count": 2},
        {"word": "algorithms", "count": 5},
        {"word": "analysis", "count": 1}
    ]
    res = client.post("/api/sort-comparison", json={"frequencies": frequencies, "repetitions": 25})
    assert res.status_code == 200
    data = res.get_json()["data"]
    assert data["outputs_match"] is True
    assert data["input_size"] == 4
    assert data["merge_sort"]["avg_time_ms"] >= 0.0
    assert data["quick_sort"]["avg_time_ms"] >= 0.0


def test_sort_comparison_with_body_fallback(client):
    res = client.post("/api/sort-comparison", json={
        "body": "Sorting algorithms analyze arrays and sorting algorithms organize data.",
        "repetitions": 10
    })
    assert res.status_code == 200
    data = res.get_json()["data"]
    assert data["outputs_match"] is True
    assert data["input_size"] > 0


def test_compare_drafts_route(client):
    payload = {
        "original_draft": "Students learn data structures and algorithms in Python.",
        "revised_draft": "Students actively learn fundamental data structures and algorithms in Python."
    }
    res = client.post("/api/compare-drafts", json=payload)
    assert res.status_code == 200
    data = res.get_json()["data"]
    assert data["lcs_length"] == 8
    assert "students" in data["lcs_words"]
    assert data["retained_ratio_original"] == 100.0


def test_compare_drafts_invalid(client):
    res = client.post("/api/compare-drafts", json={"original_draft": 123})
    assert res.status_code == 400


def test_compare_drafts_exceeds_max_length(client):
    huge_text = "a" * (MAX_TEXT_LENGTH + 10)
    res = client.post("/api/compare-drafts", json={"original_draft": huge_text, "revised_draft": "test"})
    assert res.status_code == 400
    assert "exceed maximum allowed length" in res.get_json()["error"]
