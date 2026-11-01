"""
app.py
Flask Application for the SEO Word Optimizer DAA Mini-Project.
Provides REST API endpoints for:
- Content Analysis (/api/analyze)
- Keyword Lookup via Binary Search (/api/search-keyword)
- Merge Sort vs Quick Sort Comparison (/api/sort-comparison)
- Draft Comparison via Longest Common Subsequence (/api/compare-drafts)
"""

from flask import Flask, render_template, jsonify, request
from text_analysis import analyze_article, tokenize, extract_unique_sorted_keywords
from algorithms import binary_search_keyword, compare_sorting_algorithms, compute_lcs

app = Flask(__name__)

# Maximum allowed payload string length for safety
MAX_TEXT_LENGTH = 100_000


@app.route("/")
def index():
    """Render the dashboard interface."""
    return render_template("index.html")


@app.route("/api/health", methods=["GET"])
def health():
    """Service health status check."""
    return jsonify({
        "status": "healthy",
        "service": "SEO Word Optimizer",
        "version": "1.0.0"
    }), 200


@app.route("/api/analyze", methods=["POST"])
def analyze():
    """
    Analyze article fields and return counts, keyword occurrences, density,
    presence checks, frequencies, and actionable educational suggestions.
    """
    if not request.is_json:
        return jsonify({"error": "Request body must be valid JSON."}), 400

    data = request.get_json(silent=True)
    if not isinstance(data, dict):
        return jsonify({"error": "Invalid JSON format. Expected an object."}), 400

    title = data.get("title", "")
    target_keyword = data.get("target_keyword", "")
    intro = data.get("intro", "")
    headings = data.get("headings", "")
    body = data.get("body", "")

    # Type checks
    for field_name, val in [("title", title), ("target_keyword", target_keyword),
                            ("intro", intro), ("headings", headings), ("body", body)]:
        if not isinstance(val, str):
            return jsonify({"error": f"Field '{field_name}' must be a string."}), 400
        if len(val) > MAX_TEXT_LENGTH:
            return jsonify({"error": f"Field '{field_name}' exceeds maximum allowed length of {MAX_TEXT_LENGTH} characters."}), 400

    # Perform analysis
    result = analyze_article(
        title=title,
        target_keyword=target_keyword,
        intro=intro,
        headings=headings,
        body=body
    )

    return jsonify({
        "status": "success",
        "data": result
    }), 200


@app.route("/api/search-keyword", methods=["POST"])
def search_keyword():
    """
    Run Binary Search on an alphabetically sorted list of unique extracted keywords.
    Accepts either an existing sorted keyword list or raw article body text.
    """
    if not request.is_json:
        return jsonify({"error": "Request body must be valid JSON."}), 400

    data = request.get_json(silent=True)
    if not isinstance(data, dict):
        return jsonify({"error": "Invalid JSON format. Expected an object."}), 400

    query = data.get("query", "")
    if not isinstance(query, str) or not query.strip():
        return jsonify({"error": "Search query keyword is required and cannot be empty."}), 400

    keywords = data.get("keywords")
    if keywords is None:
        # Fallback to analyzing body if provided
        body = data.get("body", "")
        if not isinstance(body, str):
            return jsonify({"error": "Field 'body' must be a string."}), 400
        tokens = tokenize(body)
        keywords = extract_unique_sorted_keywords(tokens)
    else:
        if not isinstance(keywords, list):
            return jsonify({"error": "Field 'keywords' must be an array of objects."}), 400
        # Validate elements and guarantee sorting
        sanitized = []
        for item in keywords:
            if isinstance(item, dict) and "word" in item:
                w = str(item["word"]).strip().lower()
                c = int(item.get("count", 0))
                sanitized.append({"word": w, "count": c})
        # Sort alphabetically to guarantee binary search prerequisite
        keywords = sorted(sanitized, key=lambda x: x["word"])

    search_result = binary_search_keyword(keywords, query)

    return jsonify({
        "status": "success",
        "data": {
            "search_result": search_result,
            "total_unique_keywords": len(keywords)
        }
    }), 200


@app.route("/api/sort-comparison", methods=["POST"])
def sort_comparison():
    """
    Execute Merge Sort and Quick Sort on identical copies of keyword frequencies.
    Measures and compares actual high-resolution runtimes.
    """
    if not request.is_json:
        return jsonify({"error": "Request body must be valid JSON."}), 400

    data = request.get_json(silent=True)
    if not isinstance(data, dict):
        return jsonify({"error": "Invalid JSON format. Expected an object."}), 400

    frequencies = data.get("frequencies")
    if frequencies is None:
        # Fallback: extract frequencies from body
        body = data.get("body", "")
        if not isinstance(body, str):
            return jsonify({"error": "Provide either 'frequencies' array or 'body' text."}), 400
        tokens = tokenize(body)
        from text_analysis import extract_filtered_frequencies
        frequencies = extract_filtered_frequencies(tokens, exclude_stop_words=True)

    if not isinstance(frequencies, list):
        return jsonify({"error": "Field 'frequencies' must be an array of objects."}), 400

    sanitized = []
    for item in frequencies:
        if isinstance(item, dict) and "word" in item and "count" in item:
            sanitized.append({"word": str(item["word"]), "count": int(item["count"])})

    repetitions = data.get("repetitions", 100)
    if not isinstance(repetitions, int) or repetitions <= 0:
        repetitions = 100

    comparison_result = compare_sorting_algorithms(sanitized, repetitions=repetitions)

    return jsonify({
        "status": "success",
        "data": comparison_result
    }), 200


@app.route("/api/compare-drafts", methods=["POST"])
def compare_drafts():
    """
    Compare original and revised article drafts using LCS Dynamic Programming.
    Returns retained words, retention percentages, and changed token metrics.
    """
    if not request.is_json:
        return jsonify({"error": "Request body must be valid JSON."}), 400

    data = request.get_json(silent=True)
    if not isinstance(data, dict):
        return jsonify({"error": "Invalid JSON format. Expected an object."}), 400

    draft1 = data.get("original_draft", "")
    draft2 = data.get("revised_draft", "")

    if not isinstance(draft1, str) or not isinstance(draft2, str):
        return jsonify({"error": "Both 'original_draft' and 'revised_draft' must be strings."}), 400

    if len(draft1) > MAX_TEXT_LENGTH or len(draft2) > MAX_TEXT_LENGTH:
        return jsonify({"error": f"Drafts exceed maximum allowed length of {MAX_TEXT_LENGTH} characters."}), 400

    tokens1 = tokenize(draft1)
    tokens2 = tokenize(draft2)

    lcs_result = compute_lcs(tokens1, tokens2)

    return jsonify({
        "status": "success",
        "data": lcs_result
    }), 200


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=True)
