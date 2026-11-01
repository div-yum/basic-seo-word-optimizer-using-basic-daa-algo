"""
tests/test_text_analysis.py
Unit tests for text processing, counts, keyword frequency, and density calculations.
"""

import pytest
from text_analysis import (
    tokenize,
    count_phrase_occurrences,
    count_sentences,
    count_paragraphs,
    extract_filtered_frequencies,
    extract_unique_sorted_keywords,
    analyze_article,
    STOP_WORDS
)


def test_tokenize_empty():
    assert tokenize("") == []
    assert tokenize(None) == []
    assert tokenize("   \n\t  ") == []


def test_tokenize_punctuation_and_case():
    text = "Hello, World! Testing 123... It's student's project."
    tokens = tokenize(text)
    assert tokens == ["hello", "world", "testing", "123", "it's", "student's", "project"]


def test_count_phrase_occurrences_single_word():
    tokens = ["seo", "optimization", "tools", "for", "seo", "beginners"]
    assert count_phrase_occurrences(tokens, "seo") == 2
    assert count_phrase_occurrences(tokens, "SEO") == 2
    assert count_phrase_occurrences(tokens, "python") == 0


def test_count_phrase_occurrences_multi_word():
    tokens = ["cybersecurity", "tools", "help", "students", "choose", "cybersecurity", "tools"]
    assert count_phrase_occurrences(tokens, "cybersecurity tools") == 2
    assert count_phrase_occurrences(tokens, "Cybersecurity Tools") == 2
    assert count_phrase_occurrences(tokens, "tools help") == 1
    assert count_phrase_occurrences(tokens, "tools students") == 0


def test_count_sentences():
    text = "This is sentence one. Is this sentence two? Yes! And here is four."
    assert count_sentences(text) == 4
    assert count_sentences("") == 0
    assert count_sentences("No end punctuation") == 1


def test_count_paragraphs():
    text = "Paragraph one.\n\nParagraph two with more details.\n\nParagraph three."
    assert count_paragraphs(text) == 3
    assert count_paragraphs("") == 0
    assert count_paragraphs("Just one line here.") == 1


def test_extract_filtered_frequencies():
    tokens = ["algorithm", "is", "an", "algorithm", "and", "data", "structure"]
    freqs = extract_filtered_frequencies(tokens, exclude_stop_words=True)
    # Stop words like "is", "an", "and" are filtered
    words = [item["word"] for item in freqs]
    assert "is" not in words
    assert "an" not in words
    assert "and" not in words
    assert freqs[0]["word"] == "algorithm"
    assert freqs[0]["count"] == 2
    assert freqs[1]["word"] == "data"
    assert freqs[1]["count"] == 1


def test_tie_breaking_alphabetical():
    tokens = ["banana", "apple", "cherry"]
    freqs = extract_filtered_frequencies(tokens, exclude_stop_words=False)
    # All count=1, should be ordered alphabetically: apple, banana, cherry
    assert [f["word"] for f in freqs] == ["apple", "banana", "cherry"]


def test_extract_unique_sorted_keywords():
    tokens = ["zebra", "apple", "banana", "apple"]
    unique_list = extract_unique_sorted_keywords(tokens)
    assert unique_list == [
        {"word": "apple", "count": 2},
        {"word": "banana", "count": 1},
        {"word": "zebra", "count": 1}
    ]


def test_sample_article_analysis():
    title = "Best Cybersecurity Tools for Beginners"
    target_keyword = "cybersecurity tools"
    intro = "Cybersecurity tools help students learn network defense and security testing."
    headings = "Top cybersecurity tools\nHow to choose security tools"
    body = (
        "Cybersecurity tools help students understand network security. "
        "These tools can support monitoring, learning, and authorized testing. "
        "Beginners should choose cybersecurity tools based on their learning goals."
    )

    result = analyze_article(
        title=title,
        target_keyword=target_keyword,
        intro=intro,
        headings=headings,
        body=body
    )

    metrics = result["metrics"]
    presence = result["presence"]

    # In body:
    # "Cybersecurity tools help students understand network security.
    #  These tools can support monitoring, learning, and authorized testing.
    #  Beginners should choose cybersecurity tools based on their learning goals."
    # Total tokens in body:
    # ["cybersecurity", "tools", "help", "students", "understand", "network", "security",
    #  "these", "tools", "can", "support", "monitoring", "learning", "and", "authorized", "testing",
    #  "beginners", "should", "choose", "cybersecurity", "tools", "based", "on", "their", "learning", "goals"]
    # Total = 26 tokens
    assert metrics["word_count"] == 26
    assert metrics["target_keyword"] == "cybersecurity tools"
    assert metrics["target_keyword_count"] == 2
    # Density: 2 / 26 * 100 = 7.69%
    expected_density = round(2 / 26 * 100, 2)
    assert metrics["target_keyword_density"] == expected_density

    # Title check
    assert presence["title_has_keyword"] is True
    # Intro check
    assert presence["intro_has_keyword"] is True
    # Headings check
    assert presence["heading_count"] == 2
    assert presence["headings_with_keyword"] == 1  # only first heading contains exact phrase "cybersecurity tools"

    # Recommendations
    assert len(result["recommendations"]) > 0


def test_analyze_empty_input():
    result = analyze_article("", "", "", "", "")
    assert result["metrics"]["word_count"] == 0
    assert result["metrics"]["target_keyword_count"] == 0
    assert result["metrics"]["target_keyword_density"] == 0.0
    assert result["presence"]["title_has_keyword"] is False
    assert result["filtered_frequencies"] == []
    assert result["unique_keywords_sorted"] == []
