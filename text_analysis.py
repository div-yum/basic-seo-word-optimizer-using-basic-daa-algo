"""
text_analysis.py
Provides text processing and SEO content analysis functions.
Uses only the Python standard library.
"""

import re
from collections import Counter
from typing import Dict, List, Any

# Transparent, documented list of common English stop words
STOP_WORDS = frozenset({
    "a", "about", "above", "after", "again", "against", "all", "am", "an", "and",
    "any", "are", "aren't", "as", "at", "be", "because", "been", "before", "being",
    "below", "between", "both", "but", "by", "can", "cannot", "could", "did", "do",
    "does", "doing", "down", "during", "each", "few", "for", "from", "further",
    "had", "has", "have", "having", "he", "her", "here", "hers", "herself", "him",
    "himself", "his", "how", "i", "if", "in", "into", "is", "it", "its", "itself",
    "me", "more", "most", "my", "myself", "no", "nor", "not", "of", "off", "on",
    "once", "only", "or", "other", "ought", "our", "ours", "ourselves", "out", "over",
    "own", "same", "she", "should", "so", "some", "such", "than", "that", "the",
    "their", "theirs", "them", "themselves", "then", "there", "these", "they",
    "this", "those", "through", "to", "too", "under", "until", "up", "very", "was",
    "we", "were", "what", "when", "where", "which", "while", "who", "whom", "why",
    "with", "would", "you", "your", "yours", "yourself", "yourselves"
})


def tokenize(text: str) -> List[str]:
    """
    Extract words as lowercase alphanumeric tokens from text.
    Punctuation is stripped. Numbers attached to words are retained.
    """
    if not text or not isinstance(text, str):
        return []
    # Match contiguous word characters (letters and digits)
    return re.findall(r"\b[a-zA-Z0-9]+(?:'[a-zA-Z0-9]+)?\b", text.lower())


def count_phrase_occurrences(tokens: List[str], phrase: str) -> int:
    """
    Count occurrences of a keyword or multi-word phrase within a token list.
    Matching is exact on token sequence and case-insensitive.
    """
    phrase_tokens = tokenize(phrase)
    if not phrase_tokens or not tokens:
        return 0

    p_len = len(phrase_tokens)
    t_len = len(tokens)
    if p_len > t_len:
        return 0

    count = 0
    for i in range(t_len - p_len + 1):
        if tokens[i : i + p_len] == phrase_tokens:
            count += 1
    return count


def count_sentences(text: str) -> int:
    """
    Count sentences using period, exclamation mark, and question mark boundaries.
    """
    if not text or not text.strip():
        return 0
    # Split on terminal punctuation followed by whitespace or string end
    sentences = [s.strip() for s in re.split(r"[.!?]+(?:\s+|$)", text) if s.strip()]
    return len(sentences)


def count_paragraphs(text: str) -> int:
    """
    Count paragraphs by splitting on consecutive newlines (double return).
    """
    if not text or not text.strip():
        return 0
    paragraphs = [p.strip() for p in re.split(r"\n\s*\n", text) if p.strip()]
    return len(paragraphs)


def extract_filtered_frequencies(tokens: List[str], exclude_stop_words: bool = True) -> List[Dict[str, Any]]:
    """
    Count frequencies of tokens, optionally filtering out stop words.
    Returns list of dicts: [{"word": w, "count": c}, ...] sorted by frequency descending.
    """
    if not tokens:
        return []

    if exclude_stop_words:
        target_tokens = [w for w in tokens if w not in STOP_WORDS]
    else:
        target_tokens = tokens

    counts = Counter(target_tokens)
    # Sort primarily by count descending, then alphabetically for ties
    sorted_items = sorted(counts.items(), key=lambda item: (-item[1], item[0]))
    return [{"word": word, "count": count} for word, count in sorted_items]


def extract_unique_sorted_keywords(tokens: List[str], exclude_stop_words: bool = False) -> List[Dict[str, Any]]:
    """
    Extract unique keywords sorted alphabetically with their occurrence count.
    Used for Binary Search demonstration.
    """
    if not tokens:
        return []

    if exclude_stop_words:
        filtered = [t for t in tokens if t not in STOP_WORDS]
    else:
        filtered = tokens

    counts = Counter(filtered)
    # Sort alphabetically
    sorted_words = sorted(counts.keys())
    return [{"word": w, "count": counts[w]} for w in sorted_words]


def generate_recommendations(
    title: str,
    target_keyword: str,
    intro: str,
    headings: List[str],
    body_tokens: List[str],
    keyword_count: int,
    keyword_density: float,
    title_has_kw: bool,
    intro_has_kw: bool,
    headings_with_kw: int
) -> List[Dict[str, str]]:
    """
    Generate practical, educational recommendations based on content structure
    and descriptive SEO checks. Does NOT claim to predict search rankings.
    """
    recs = []

    # Title checks
    if not title.strip():
        recs.append({
            "category": "Title",
            "type": "warning",
            "message": "Article title is missing. Add a concise, descriptive title outlining the topic."
        })
    elif target_keyword.strip() and not title_has_kw:
        recs.append({
            "category": "Title",
            "type": "info",
            "message": f"Target keyword '{target_keyword}' was not found in the title. Consider including it for clearer topic focus."
        })
    elif target_keyword.strip() and title_has_kw:
        recs.append({
            "category": "Title",
            "type": "success",
            "message": f"Target keyword '{target_keyword}' is present in the title."
        })

    # Introduction checks
    if not intro.strip():
        recs.append({
            "category": "Introduction",
            "type": "warning",
            "message": "Introduction is missing. A strong introductory paragraph sets context for readers."
        })
    elif target_keyword.strip() and not intro_has_kw:
        recs.append({
            "category": "Introduction",
            "type": "info",
            "message": f"Target keyword '{target_keyword}' was not found in the introduction. Including it early helps establish context."
        })
    elif target_keyword.strip() and intro_has_kw:
        recs.append({
            "category": "Introduction",
            "type": "success",
            "message": f"Target keyword '{target_keyword}' is present in the introduction."
        })

    # Headings checks
    valid_headings = [h.strip() for h in headings if h.strip()]
    if not valid_headings:
        recs.append({
            "category": "Headings",
            "type": "warning",
            "message": "No section headings provided. Meaningful headings improve text readability and structure."
        })
    elif target_keyword.strip():
        if headings_with_kw == 0:
            recs.append({
                "category": "Headings",
                "type": "info",
                "message": f"Target keyword was not found in any heading ({len(valid_headings)} total). Consider using it naturally in relevant headings."
            })
        else:
            recs.append({
                "category": "Headings",
                "type": "success",
                "message": f"Target keyword appears in {headings_with_kw} of {len(valid_headings)} heading(s)."
            })

    # Body length checks
    word_count = len(body_tokens)
    if word_count == 0:
        recs.append({
            "category": "Body Length",
            "type": "warning",
            "message": "Article body is empty. Enter or paste text to perform content analysis."
        })
    elif word_count < 100:
        recs.append({
            "category": "Body Length",
            "type": "info",
            "message": f"Article body is relatively short ({word_count} words). Consider expanding explanations or adding examples."
        })
    else:
        recs.append({
            "category": "Body Length",
            "type": "success",
            "message": f"Article body length is substantial ({word_count} words)."
        })

    # Keyword density checks (Descriptive metric only)
    if target_keyword.strip() and word_count > 0:
        if keyword_count == 0:
            recs.append({
                "category": "Keyword Density",
                "type": "warning",
                "message": f"Target keyword '{target_keyword}' does not appear in the body text (0.00% density)."
            })
        elif keyword_density > 3.5:
            recs.append({
                "category": "Keyword Density",
                "type": "warning",
                "message": f"Keyword density is unusually high ({keyword_density:.2f}%). Review repeated terms to ensure the article reads naturally and avoids stuffing."
            })
        elif 1.0 <= keyword_density <= 3.5:
            recs.append({
                "category": "Keyword Density",
                "type": "success",
                "message": f"Keyword density is {keyword_density:.2f}%, within a balanced descriptive range. Ensure wording sounds natural."
            })
        else:
            recs.append({
                "category": "Keyword Density",
                "type": "info",
                "message": f"Keyword density is {keyword_density:.2f}% ({keyword_count} occurrence(s)). Consider using it slightly more if appropriate for clarity."
            })

    return recs


def analyze_article(
    title: str = "",
    target_keyword: str = "",
    intro: str = "",
    headings: str = "",
    body: str = ""
) -> Dict[str, Any]:
    """
    Perform full content analysis on user-supplied fields.
    Returns metrics, keyword frequencies, presence checks, and suggestions.
    """
    title = title or ""
    target_keyword = (target_keyword or "").strip()
    intro = intro or ""
    body = body or ""

    # Parse headings line by line
    heading_lines = [line.strip() for line in (headings or "").splitlines() if line.strip()]

    # Tokenize article body
    body_tokens = tokenize(body)
    word_count = len(body_tokens)
    char_count = len(body)
    char_count_no_spaces = len(body.replace(" ", "").replace("\t", "").replace("\n", "").replace("\r", ""))
    sentence_count = count_sentences(body)
    paragraph_count = count_paragraphs(body)

    # Keyword occurrence & density
    keyword_count = count_phrase_occurrences(body_tokens, target_keyword) if target_keyword else 0
    keyword_density = round((keyword_count / word_count * 100), 2) if word_count > 0 else 0.0

    # Presence checks
    title_tokens = tokenize(title)
    intro_tokens = tokenize(intro)
    title_has_kw = count_phrase_occurrences(title_tokens, target_keyword) > 0 if target_keyword else False
    intro_has_kw = count_phrase_occurrences(intro_tokens, target_keyword) > 0 if target_keyword else False

    headings_with_kw = 0
    heading_details = []
    for h in heading_lines:
        h_tokens = tokenize(h)
        has_kw = count_phrase_occurrences(h_tokens, target_keyword) > 0 if target_keyword else False
        if has_kw:
            headings_with_kw += 1
        heading_details.append({"text": h, "has_keyword": has_kw})

    # Frequencies
    filtered_frequencies = extract_filtered_frequencies(body_tokens, exclude_stop_words=True)
    all_frequencies = extract_filtered_frequencies(body_tokens, exclude_stop_words=False)
    unique_sorted = extract_unique_sorted_keywords(body_tokens, exclude_stop_words=False)

    # Recommendations
    recs = generate_recommendations(
        title=title,
        target_keyword=target_keyword,
        intro=intro,
        headings=heading_lines,
        body_tokens=body_tokens,
        keyword_count=keyword_count,
        keyword_density=keyword_density,
        title_has_kw=title_has_kw,
        intro_has_kw=intro_has_kw,
        headings_with_kw=headings_with_kw
    )

    return {
        "metrics": {
            "word_count": word_count,
            "character_count": char_count,
            "character_count_no_spaces": char_count_no_spaces,
            "sentence_count": sentence_count,
            "paragraph_count": paragraph_count,
            "target_keyword": target_keyword,
            "target_keyword_count": keyword_count,
            "target_keyword_density": keyword_density
        },
        "presence": {
            "title_has_keyword": title_has_kw,
            "intro_has_keyword": intro_has_kw,
            "heading_count": len(heading_lines),
            "headings_with_keyword": headings_with_kw,
            "heading_details": heading_details
        },
        "filtered_frequencies": filtered_frequencies,
        "all_frequencies": all_frequencies,
        "unique_keywords_sorted": unique_sorted,
        "recommendations": recs
    }
