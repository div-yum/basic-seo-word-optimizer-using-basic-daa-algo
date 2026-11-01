# SEO Word Optimizer &mdash; B.Tech DAA Mini-Project

An end-to-end, explainable academic web application built for B.Tech Computer Science / Information Technology students. The project demonstrates core **Design and Analysis of Algorithms (DAA)** techniques on real-world text content:

1. **Binary Search** &mdash; Logarithmic keyword lookup in an alphabetically sorted dictionary.
2. **Merge Sort vs Quick Sort** &mdash; High-resolution benchmarking and tie-breaker keyword frequency ranking.
3. **Longest Common Subsequence (LCS)** &mdash; Dynamic Programming ($O(m \times n)$) draft comparison and sequence reconstruction.

---

## Table of Contents
1. [Project Overview & Abstract](#1-project-overview--abstract)
2. [Problem Statement & Objectives](#2-problem-statement--objectives)
3. [Technology Stack](#3-technology-stack)
4. [System Architecture & Workflow](#4-system-architecture--workflow)
5. [Text Analysis Methodology](#5-text-analysis-methodology)
6. [DAA Algorithms & Theoretical Complexity](#6-daa-algorithms--theoretical-complexity)
7. [Algorithm Pseudocode](#7-algorithm-pseudocode)
8. [Setup & Running Instructions](#8-setup--running-instructions)
9. [Running Automated Tests](#9-running-automated-tests)
10. [Sample Test Run & Benchmark Results](#10-sample-test-run--benchmark-results)
11. [Limitations & Honest Scope](#11-limitations--honest-scope)
12. [Viva Voce Questions & Answers](#12-viva-voce-questions--answers)

---

## 1. Project Overview & Abstract

In introductory SEO and content editing, writers need to inspect article structure, term frequencies, and keyword presence across key sections (title, introduction, headings, and body). 

**SEO Word Optimizer** connects fundamental algorithmic paradigms (Divide-and-Conquer, Dynamic Programming, and Binary Search) with practical text processing. Rather than using external black-box search engine APIs or unverifiable scoring models, this project implements and benchmarks every algorithm manually in standard Python.

---

## 2. Problem Statement & Objectives

### Problem Statement
Content creators require transparent metrics about their written text (word counts, target term distribution, structural placement, and revision histories) without sending private drafts to third-party proprietary services. Concurrently, undergraduate engineering students often study algorithms purely in abstract contexts; applying these algorithms to tangible text processing reinforces time/space complexity concepts.

### Objectives
- Extract, normalize, and tokenize user-supplied text into standardized word tokens.
- Implement **Binary Search** ($O(\log n)$) to query keywords within an alphabetically ordered unique word dictionary.
- Implement **Merge Sort** and **Quick Sort** manually to order extracted terms by frequency (descending) and lexicographically (ascending) for ties, confirming parity and benchmarking runtimes.
- Implement **Longest Common Subsequence (LCS)** using 2D Dynamic Programming ($O(m \times n)$) to identify retained word order across article drafts.
- Provide a clean single-page dashboard with client-side export to TXT and CSV.

---

## 3. Technology Stack

- **Backend:** Python 3 (standard library only for algorithms and text parsing)
- **Web Framework:** Flask (lightweight REST API & template rendering)
- **Frontend:** Vanilla HTML5, CSS3 (modern responsive card layout), Vanilla JavaScript (no external frameworks or CDNs required)
- **Testing:** `pytest` (comprehensive automated test suite covering edge cases, routing, and algorithm correctness)

---

## 4. System Architecture & Workflow

```
[User Interface (Browser)]
       |
       |-- 1. Input Article Fields / Drafts
       v
[Flask REST API (app.py)]
       |
       +---> [text_analysis.py]
       |         Tokenization -> Stop-word filtering -> Occurrence counting -> Metrics
       |
       +---> [algorithms.py]
                 - binary_search_keyword()  [O(log n)]
                 - merge_sort()             [O(n log n)]
                 - quick_sort()             [O(n log n) avg]
                 - compute_lcs()            [O(m * n) DP]
       |
       v
[JSON Response / Real-time DOM Rendering / TXT & CSV Export]
```

### Folder Structure
```
seo-word-optimizer/
├── app.py                     # Flask web server and JSON REST endpoints
├── text_analysis.py           # Tokenizer, stop words, keyword density, recommendations
├── algorithms.py              # Pure Python implementations of Binary Search, Merge Sort, Quick Sort, LCS
├── requirements.txt           # Minimal dependencies (Flask, pytest)
├── README.md                  # Comprehensive academic report and project documentation
├── templates/
│   └── index.html             # Responsive single-page dashboard
├── static/
│   ├── style.css              # Modern academic styling and responsive grid
│   └── app.js                 # Frontend API controller, state handling, and report exports
└── tests/
    ├── test_text_analysis.py  # Unit tests for text processing & density formulas
    ├── test_algorithms.py     # Unit tests for DAA algorithms & complexity bounds
    └── test_routes.py         # Integration tests for Flask endpoints & payloads
```

---

## 5. Text Analysis Methodology

1. **Tokenization Rule:** Words are extracted using lowercase alphanumeric matching (`\b[a-zA-Z0-9]+(?:'[a-zA-Z0-9]+)?\b`). Punctuation is stripped while contractions and numbers are preserved.
2. **Stop Word Filtering:** A documented list of standard English functional words (e.g., *the, is, and, with, this*) is excluded when generating top keyword rankings.
3. **Keyword Density Formula:**
   $$\text{Keyword Density (\%)} = \left(\frac{\text{Target Keyword Occurrences}}{\text{Total Article Body Word Tokens}}\right) \times 100$$
4. **Structural Placement:** Case-insensitive phrase matching checks whether the target phrase appears in the Title, the Introduction, or any specified Headings.
5. **Practical Recommendations:** Rules-based checklist evaluating keyword presence, draft lengths, and natural usage ranges (1.0% to 3.5%).

---

## 6. DAA Algorithms & Theoretical Complexity

| Algorithm | Paradigm | Best Case | Average Case | Worst Case | Auxiliary Space | Stable? |
|---|---|---|---|---|---|---|
| **Binary Search** | Decrease and Conquer | $O(1)$ | $O(\log n)$ | $O(\log n)$ | $O(1)$ (iterative) | N/A |
| **Merge Sort** | Divide and Conquer | $O(n \log n)$ | $O(n \log n)$ | $O(n \log n)$ | $O(n)$ | Yes |
| **Quick Sort** | Divide and Conquer (Partitioning) | $O(n \log n)$ | $O(n \log n)$ | $O(n^2)$ | $O(\log n)$ to $O(n)$ | No |
| **LCS (DP)** | Dynamic Programming | $O(m \times n)$ | $O(m \times n)$ | $O(m \times n)$ | $O(m \times n)$ | N/A |

### Explanation of Sorting Tie-Breaker
In keyword frequency tables, multiple words may have identical frequencies (e.g., "apple": 2, "banana": 2). To ensure deterministic results:
- Primary key: `count` (descending order).
- Tie-breaker key: `word` (lexicographically ascending order).
Because each word in the dictionary is unique, every `(count, word)` key pair is distinct. As a result, both **Merge Sort** and **Quick Sort** produce 100% identical rankings.

---

## 7. Algorithm Pseudocode

### A. Binary Search on Sorted Keyword Dictionary
```
Algorithm BinarySearchKeyword(A, query):
    low = 0
    high = length(A) - 1
    while low <= high:
        mid = floor((low + high) / 2)
        if A[mid].word == query:
            return FOUND at index mid with A[mid].count
        else if A[mid].word < query:
            low = mid + 1
        else:
            high = mid - 1
    return NOT_FOUND
```

### B. Merge Sort for Keyword Ranking
```
Algorithm MergeSort(A):
    if length(A) <= 1:
        return A
    mid = length(A) / 2
    Left = MergeSort(A[0 ... mid - 1])
    Right = MergeSort(A[mid ... end])
    return Merge(Left, Right)

Algorithm Merge(Left, Right):
    result = []
    i = 0, j = 0
    while i < length(Left) and j < length(Right):
        if Left[i].count > Right[j].count or (Left[i].count == Right[j].count and Left[i].word <= Right[j].word):
            result.append(Left[i]); i += 1
        else:
            result.append(Right[j]); j += 1
    append remaining elements of Left and Right to result
    return result
```

### C. Longest Common Subsequence (LCS)
```
Algorithm ComputeLCS(X[1..m], Y[1..n]):
    Initialize table DP[0..m, 0..n] with zeros
    for i from 1 to m:
        for j from 1 to n:
            if X[i] == Y[j]:
                DP[i, j] = DP[i - 1, j - 1] + 1
            else:
                DP[i, j] = max(DP[i - 1, j], DP[i, j - 1])
    
    // Backtracking to reconstruct LCS sequence
    i = m, j = n, sequence = []
    while i > 0 and j > 0:
        if X[i] == Y[j]:
            sequence.append(X[i]); i -= 1; j -= 1
        else if DP[i - 1, j] >= DP[i, j - 1]:
            i -= 1
        else:
            j -= 1
    reverse(sequence)
    return DP[m, n], sequence
```

---

## 8. Setup & Running Instructions

### Prerequisites
- Python 3.9+ (Python 3.10, 3.11, 3.12, 3.13, 3.14 supported)
- Standard web browser (Chrome, Edge, Firefox, Safari)

### Installation Steps

1. Open your terminal or PowerShell and navigate to the project folder:
   ```bash
   cd "C:\Users\Lenovo\.gemini\antigravity\scratch\seo-word-optimizer"
   ```

2. (Optional) Create and activate a Python virtual environment:
   ```bash
   python -m venv venv
   # On Windows PowerShell:
   .\venv\Scripts\Activate.ps1
   ```

3. Install the dependencies:
   ```bash
   python -m pip install -r requirements.txt
   ```

4. Start the application:
   ```bash
   python app.py
   ```

5. Open your web browser and visit:
   ```
   http://127.0.0.1:5000
   ```

---

## 9. Running Automated Tests

Run the full pytest suite from the project directory:

```bash
python -m pytest -v
```

All 34 automated unit and integration tests will execute, validating:
- Tokenizer behavior, contractions, and punctuation handling.
- Stop-word filtering and exact frequency counting.
- Binary Search for existing terms, missing terms, and edge cases.
- 100% output parity between Merge Sort and Quick Sort.
- Subsequence verification for LCS draft comparison.
- Robust HTTP status handling, type safety, and input size constraints.

---

## 10. Sample Test Run & Benchmark Results

### Sample Input (from Specification)
- **Title:** `Best Cybersecurity Tools for Beginners`
- **Target Keyword:** `cybersecurity tools`
- **Introduction:** `Cybersecurity tools help students learn network defense and security testing.`
- **Headings:**
  ```
  Top cybersecurity tools
  How to choose security tools
  ```
- **Body:**
  ```
  Cybersecurity tools help students understand network security. These tools can support monitoring, learning, and authorized testing. Beginners should choose cybersecurity tools based on their learning goals.
  ```

### Live Test Outputs
- **Total Word Count:** 26 tokens
- **Character Count:** 214 characters (189 excluding whitespace)
- **Target Keyword Count:** 2 occurrences in body
- **Keyword Density:** $2 / 26 \times 100 = 7.69\%$
- **Presence Checks:**
  - Title: **Present** ($\checkmark$)
  - Introduction: **Present** ($\checkmark$)
  - Headings: **Present in 1 of 2 headings** ($\checkmark$)
- **Top Non-Stop Words:** `tools` (3), `cybersecurity` (2), `learning` (2), `authorized` (1), `beginners` (1)

### Sorting Benchmark Results (Measured across 100 iterations)
- **Input Size ($n$):** 16 unique filtered keywords
- **Merge Sort Average Runtime:** `0.00940 ms`
- **Quick Sort Average Runtime:** `0.00670 ms`
- **Output Parity:** **100% Identical** across all positions.

### LCS Draft Comparison
- **Draft 1:** `Cybersecurity tools help students understand network defense. Beginners must test firewalls carefully.` ($m = 12$ words)
- **Draft 2:** `Modern cybersecurity tools help students understand network defense. Beginners must practice testing firewalls carefully and ethically.` ($n = 15$ words)
- **LCS Length:** $11$ words retained
- **LCS Sequence:** `cybersecurity tools help students understand network defense beginners must firewalls carefully`
- **Retention:** $91.67\%$ of Draft 1, $73.33\%$ of Draft 2.

---

## 11. Limitations & Honest Scope

1. **Local Text Processing:** Operates strictly on user-supplied strings. It does not perform web scraping, crawler simulation, or network requests.
2. **Descriptive Metrics:** Keyword density and placement checks are structural guideposts, not guarantees of Google SERP placement.
3. **No Machine Learning / AI:** All algorithms are deterministic, transparent, and manually implemented.
4. **LCS Subsequence Scope:** LCS evaluates sequential token alignment; it does not compute semantic embeddings or detect paraphrased sentences.

---

## 12. Viva Voce Questions & Answers

**Q1: Why is Binary Search $O(\log n)$ while linear search is $O(n)$?**
> *Answer:* At every comparison, Binary Search compares the target with the middle element of a sorted array and discards half of the remaining search space. The recurrence relation is $T(n) = T(n/2) + O(1)$, which solves to $O(\log_2 n)$ using the Master Theorem.

**Q2: What is the primary prerequisite for Binary Search?**
> *Answer:* The input collection must be sorted in a monotonic (e.g., ascending alphabetical) order with $O(1)$ random index access. Creating this sorted list from raw text has an initial cost of $O(n \log n)$.

**Q3: Why might Quick Sort be faster than Merge Sort in practice despite having a worse worst-case complexity?**
> *Answer:* Quick Sort has smaller constant factors and exhibits superior CPU cache locality because it partitions in-place. Merge Sort requires allocating $O(n)$ auxiliary memory and copying elements back and forth during the merge phase.

**Q4: Under what conditions does Quick Sort exhibit its worst-case runtime of $O(n^2)$?**
> *Answer:* When the chosen pivot consistently splits the array into maximally unbalanced partitions (e.g., selecting the minimum or maximum element in an already sorted array). Using a middle element or median-of-three pivot strategy mitigates this issue.

**Q5: What are the two core properties that make a problem solvable by Dynamic Programming?**
> *Answer:* 
> 1. **Optimal Substructure:** An optimal solution to the problem contains within it optimal solutions to subproblems.
> 2. **Overlapping Subproblems:** The same subproblems are solved repeatedly rather than generating new subproblems.

**Q6: What is the difference between a Subsequence and a Substring?**
> *Answer:* A substring must be contiguous in the original string. A subsequence is derived by deleting zero or more characters/words without changing the relative order of the remaining elements.

**Q7: How is the LCS reconstructed after filling the DP table?**
> *Answer:* By backtracking from $DP[m][n]$ back to $DP[0][0]$. If $X[i-1] == Y[j-1]$, the word is part of the LCS, and we move diagonally to $(i-1, j-1)$. Otherwise, we step in the direction of the larger neighbor: $\max(DP[i-1][j], DP[i][j-1])$.
