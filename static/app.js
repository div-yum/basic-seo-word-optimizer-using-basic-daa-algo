/**
 * app.js
 * Frontend controller for SEO Word Optimizer DAA Mini-Project.
 * Handles API calls, UI rendering, client-side exports, and interactive demonstrations.
 */

// Global in-memory state
const state = {
    analysis: null,
    sorting: null,
    lcs: null
};

// Sample data from academic requirements specification
const SAMPLE_ARTICLE = {
    title: "Best Cybersecurity Tools for Beginners",
    target_keyword: "cybersecurity tools",
    intro: "Cybersecurity tools help students learn network defense and security testing.",
    headings: "Top cybersecurity tools\nHow to choose security tools",
    body: "Cybersecurity tools help students understand network security. These tools can support monitoring, learning, and authorized testing. Beginners should choose cybersecurity tools based on their learning goals."
};

const SAMPLE_DRAFTS = {
    original: "Cybersecurity tools help students understand network defense. Beginners must test firewalls carefully.",
    revised: "Modern cybersecurity tools help students understand network defense. Beginners must practice testing firewalls carefully and ethically."
};

// DOM Elements
document.addEventListener("DOMContentLoaded", () => {
    initEventListeners();
});

function initEventListeners() {
    // Quick load samples
    document.getElementById("btn-load-sample").addEventListener("click", loadSampleArticle);
    document.getElementById("btn-load-drafts").addEventListener("click", loadSampleDrafts);

    // Section A: Content Analyzer
    document.getElementById("btn-analyze").addEventListener("click", handleAnalyze);
    document.getElementById("btn-clear-article").addEventListener("click", clearArticleForm);
    document.getElementById("btn-export-txt").addEventListener("click", exportTxtReport);
    document.getElementById("btn-export-csv").addEventListener("click", exportCsvReport);

    // Section B: Binary Search
    document.getElementById("btn-run-binary-search").addEventListener("click", handleBinarySearch);
    document.getElementById("input-binary-query").addEventListener("keydown", (e) => {
        if (e.key === "Enter") handleBinarySearch();
    });

    // Section C: Sorting Comparison
    document.getElementById("btn-run-sort-comparison").addEventListener("click", handleSortComparison);

    // Section D: Draft Comparison
    document.getElementById("btn-compare-drafts").addEventListener("click", handleDraftComparison);
    document.getElementById("btn-clear-drafts").addEventListener("click", clearDraftsForm);
}

// =====================================================================
// UTILITIES: Toast & Notifications
// =====================================================================
function showToast(message, type = "error") {
    const toast = document.getElementById("status-toast");
    toast.textContent = message;
    toast.className = `toast toast-${type}`;
    toast.classList.remove("hidden");
    setTimeout(() => {
        toast.classList.add("hidden");
    }, 4500);
}

// =====================================================================
// SAMPLE DATA LOADERS
// =====================================================================
function loadSampleArticle() {
    document.getElementById("input-title").value = SAMPLE_ARTICLE.title;
    document.getElementById("input-keyword").value = SAMPLE_ARTICLE.target_keyword;
    document.getElementById("input-intro").value = SAMPLE_ARTICLE.intro;
    document.getElementById("input-headings").value = SAMPLE_ARTICLE.headings;
    document.getElementById("input-body").value = SAMPLE_ARTICLE.body;
    document.getElementById("input-binary-query").value = "tools";
    showToast("Sample cybersecurity article loaded. Click 'Analyze Content' to process.", "success");
}

function loadSampleDrafts() {
    document.getElementById("input-draft-orig").value = SAMPLE_DRAFTS.original;
    document.getElementById("input-draft-rev").value = SAMPLE_DRAFTS.revised;
    showToast("Sample draft comparison text loaded. Click 'Compare Drafts' to run LCS.", "success");
}

function clearArticleForm() {
    document.getElementById("input-title").value = "";
    document.getElementById("input-keyword").value = "";
    document.getElementById("input-intro").value = "";
    document.getElementById("input-headings").value = "";
    document.getElementById("input-body").value = "";
    document.getElementById("analyzer-results").classList.add("hidden");
    state.analysis = null;
}

function clearDraftsForm() {
    document.getElementById("input-draft-orig").value = "";
    document.getElementById("input-draft-rev").value = "";
    document.getElementById("lcs-results").classList.add("hidden");
    state.lcs = null;
}

// =====================================================================
// SECTION A: CONTENT ANALYZER
// =====================================================================
async function handleAnalyze() {
    const title = document.getElementById("input-title").value;
    const target_keyword = document.getElementById("input-keyword").value;
    const intro = document.getElementById("input-intro").value;
    const headings = document.getElementById("input-headings").value;
    const body = document.getElementById("input-body").value;

    if (!body.trim()) {
        showToast("Please provide article body text to analyze.", "error");
        return;
    }

    const btn = document.getElementById("btn-analyze");
    btn.disabled = true;
    btn.textContent = "Analyzing...";

    try {
        const response = await fetch("/api/analyze", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ title, target_keyword, intro, headings, body })
        });

        const resData = await response.json();
        if (!response.ok) {
            throw new Error(resData.error || "Analysis failed.");
        }

        state.analysis = resData.data;
        renderAnalysisResults(resData.data);
        showToast("Analysis complete!", "success");

        // Automatically prefill binary search query if keyword provided
        if (target_keyword.trim() && !document.getElementById("input-binary-query").value) {
            const firstWord = target_keyword.trim().split(/\s+/)[0];
            document.getElementById("input-binary-query").value = firstWord;
        }
    } catch (err) {
        showToast(err.message, "error");
    } finally {
        btn.disabled = false;
        btn.innerHTML = "&#x25B6; Analyze Content";
    }
}

function renderAnalysisResults(data) {
    const metrics = data.metrics;
    const presence = data.presence;

    document.getElementById("val-word-count").textContent = metrics.word_count;
    document.getElementById("val-char-count").textContent = metrics.character_count;
    document.getElementById("val-char-no-space").textContent = `${metrics.character_count_no_spaces} without spaces`;
    document.getElementById("val-sentence-count").textContent = metrics.sentence_count;
    document.getElementById("val-paragraph-count").textContent = metrics.paragraph_count;
    document.getElementById("val-kw-count").textContent = metrics.target_keyword_count;
    document.getElementById("val-kw-query").textContent = metrics.target_keyword || "Not specified";
    document.getElementById("val-kw-density").textContent = `${metrics.target_keyword_density}%`;

    // Presence checks
    updatePresenceBadge("badge-title", "Title", presence.title_has_keyword, metrics.target_keyword);
    updatePresenceBadge("badge-intro", "Introduction", presence.intro_has_keyword, metrics.target_keyword);
    updateHeadingsBadge("badge-headings", presence.headings_with_keyword, presence.heading_count, metrics.target_keyword);

    // Frequencies Table
    const tbody = document.getElementById("tbody-frequencies");
    tbody.innerHTML = "";
    const topFreqs = (data.filtered_frequencies || []).slice(0, 15);
    if (topFreqs.length === 0) {
        tbody.innerHTML = `<tr><td colspan="3" style="text-align:center; color:#94a3b8;">No significant terms found.</td></tr>`;
    } else {
        topFreqs.forEach((item, index) => {
            const tr = document.createElement("tr");
            tr.innerHTML = `
                <td><strong>#${index + 1}</strong></td>
                <td><code>${escapeHtml(item.word)}</code></td>
                <td><span class="pill-dot"></span> ${item.count}</td>
            `;
            tbody.appendChild(tr);
        });
    }

    // Recommendations
    const recContainer = document.getElementById("recommendations-container");
    recContainer.innerHTML = "";
    (data.recommendations || []).forEach(rec => {
        const item = document.createElement("div");
        item.className = `rec-item rec-${rec.type || 'info'}`;
        item.innerHTML = `
            <span>&bull;</span>
            <div><strong>${escapeHtml(rec.category)}:</strong> ${escapeHtml(rec.message)}</div>
        `;
        recContainer.appendChild(item);
    });

    document.getElementById("analyzer-results").classList.remove("hidden");
}

function updatePresenceBadge(elementId, label, hasKeyword, keyword) {
    const el = document.getElementById(elementId);
    if (!keyword) {
        el.className = "badge-item";
        el.innerHTML = `<span class="badge-icon">&#x25CB;</span> <span>${label}: No target keyword set</span>`;
        return;
    }
    if (hasKeyword) {
        el.className = "badge-item badge-found";
        el.innerHTML = `<span class="badge-icon">&#x2713;</span> <span>${label}: Present</span>`;
    } else {
        el.className = "badge-item badge-missing";
        el.innerHTML = `<span class="badge-icon">&#x2715;</span> <span>${label}: Not detected</span>`;
    }
}

function updateHeadingsBadge(elementId, withKw, totalHeadings, keyword) {
    const el = document.getElementById(elementId);
    if (totalHeadings === 0) {
        el.className = "badge-item badge-missing";
        el.innerHTML = `<span class="badge-icon">&#x2715;</span> <span>Headings: None entered</span>`;
        return;
    }
    if (!keyword) {
        el.className = "badge-item";
        el.innerHTML = `<span class="badge-icon">&#x25CB;</span> <span>Headings: ${totalHeadings} entered</span>`;
        return;
    }
    if (withKw > 0) {
        el.className = "badge-item badge-found";
        el.innerHTML = `<span class="badge-icon">&#x2713;</span> <span>Headings: Found in ${withKw} of ${totalHeadings}</span>`;
    } else {
        el.className = "badge-item badge-missing";
        el.innerHTML = `<span class="badge-icon">&#x2715;</span> <span>Headings: Not found (${totalHeadings} checked)</span>`;
    }
}

// =====================================================================
// SECTION B: BINARY SEARCH
// =====================================================================
async function handleBinarySearch() {
    const query = document.getElementById("input-binary-query").value.trim();
    if (!query) {
        showToast("Please enter a keyword to search.", "error");
        return;
    }

    // Determine keywords source: use analyzed unique keywords if available, else article body
    let keywords = null;
    let body = null;
    if (state.analysis && state.analysis.unique_keywords_sorted) {
        keywords = state.analysis.unique_keywords_sorted;
    } else {
        body = document.getElementById("input-body").value;
        if (!body.trim()) {
            showToast("Please analyze content first or paste text in the article body.", "error");
            return;
        }
    }

    const btn = document.getElementById("btn-run-binary-search");
    btn.disabled = true;
    btn.textContent = "Searching...";

    try {
        const response = await fetch("/api/search-keyword", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ query, keywords, body })
        });

        const resData = await response.json();
        if (!response.ok) {
            throw new Error(resData.error || "Binary search failed.");
        }

        renderBinarySearchResults(resData.data);
    } catch (err) {
        showToast(err.message, "error");
    } finally {
        btn.disabled = false;
        btn.textContent = "Binary Search";
    }
}

function renderBinarySearchResults(data) {
    const sr = data.search_result;
    const totalN = data.total_unique_keywords;
    const maxComp = totalN > 0 ? Math.ceil(Math.log2(totalN + 1)) : 0;

    const card = document.getElementById("binary-status-card");
    const heading = document.getElementById("binary-status-heading");
    const msg = document.getElementById("binary-status-message");

    if (sr.found) {
        card.className = "result-status-card status-found";
        heading.textContent = `Found: "${sr.word}"`;
        msg.textContent = `Target keyword exists in the dictionary with occurrence frequency of ${sr.count}. Found at index ${sr.index}.`;
    } else {
        card.className = "result-status-card status-not-found";
        heading.textContent = `Not Found: "${sr.query}"`;
        msg.textContent = `Keyword does not exist in the extracted unique keywords of this article.`;
    }

    document.getElementById("val-binary-n").textContent = totalN;
    document.getElementById("val-binary-comparisons").textContent = sr.comparisons;
    document.getElementById("val-binary-max-comp").textContent = maxComp;
    document.getElementById("val-binary-index").textContent = sr.index >= 0 ? sr.index : "N/A";

    // Trace steps
    const traceContainer = document.getElementById("binary-trace-steps");
    traceContainer.innerHTML = "";
    if (sr.steps && sr.steps.length > 0) {
        sr.steps.forEach(step => {
            const item = document.createElement("div");
            item.className = "trace-step-item";
            item.innerHTML = `
                <span><strong>Step ${step.step}:</strong> range [${step.low}..${step.high}]</span>
                <span>mid=${step.mid} &rarr; <code>"${escapeHtml(step.mid_word)}"</code></span>
            `;
            traceContainer.appendChild(item);
        });
    } else {
        traceContainer.innerHTML = `<div style="font-size:12px; color:#94a3b8;">No search steps recorded.</div>`;
    }

    document.getElementById("binary-search-results").classList.remove("hidden");
}

// =====================================================================
// SECTION C: SORTING COMPARISON
// =====================================================================
async function handleSortComparison() {
    let frequencies = null;
    let body = null;

    if (state.analysis && state.analysis.filtered_frequencies) {
        frequencies = state.analysis.filtered_frequencies;
    } else {
        body = document.getElementById("input-body").value;
        if (!body.trim()) {
            showToast("Please analyze content first or paste text in the article body.", "error");
            return;
        }
    }

    const repetitions = parseInt(document.getElementById("select-repetitions").value, 10) || 100;
    const btn = document.getElementById("btn-run-sort-comparison");
    btn.disabled = true;
    btn.innerHTML = "Benchmarking...";

    try {
        const response = await fetch("/api/sort-comparison", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ frequencies, body, repetitions })
        });

        const resData = await response.json();
        if (!response.ok) {
            throw new Error(resData.error || "Sorting benchmark failed.");
        }

        state.sorting = resData.data;
        renderSortingResults(resData.data);
        showToast("Sorting benchmark complete!", "success");
    } catch (err) {
        showToast(err.message, "error");
    } finally {
        btn.disabled = false;
        btn.innerHTML = "&#x26A1; Compare Sorting Algorithms";
    }
}

function renderSortingResults(data) {
    const banner = document.getElementById("sort-match-banner");
    const bannerText = document.getElementById("sort-match-text");

    if (data.outputs_match) {
        banner.style.display = "flex";
        bannerText.textContent = `Outputs Match: 100% Identical Ordering Across All ${data.input_size} Items`;
    } else {
        banner.style.display = "none";
    }

    document.getElementById("val-merge-time").textContent = `${data.merge_sort.avg_time_ms.toFixed(5)} ms`;
    document.getElementById("val-quick-time").textContent = `${data.quick_sort.avg_time_ms.toFixed(5)} ms`;
    document.getElementById("sort-benchmark-explanation").textContent = data.explanation;

    document.getElementById("sorting-results").classList.remove("hidden");
}

// =====================================================================
// SECTION D: DRAFT COMPARISON (LCS)
// =====================================================================
async function handleDraftComparison() {
    const draft1 = document.getElementById("input-draft-orig").value;
    const draft2 = document.getElementById("input-draft-rev").value;

    if (!draft1.trim() && !draft2.trim()) {
        showToast("Please provide at least one draft to compare.", "error");
        return;
    }

    const btn = document.getElementById("btn-compare-drafts");
    btn.disabled = true;
    btn.textContent = "Computing LCS...";

    try {
        const response = await fetch("/api/compare-drafts", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ original_draft: draft1, revised_draft: draft2 })
        });

        const resData = await response.json();
        if (!response.ok) {
            throw new Error(resData.error || "Draft comparison failed.");
        }

        state.lcs = resData.data;
        renderLcsResults(resData.data);
        showToast("Draft comparison complete!", "success");
    } catch (err) {
        showToast(err.message, "error");
    } finally {
        btn.disabled = false;
        btn.innerHTML = "&#x21C4; Compare Drafts";
    }
}

function renderLcsResults(data) {
    document.getElementById("val-lcs-m").textContent = data.original_word_count;
    document.getElementById("val-lcs-n").textContent = data.revised_word_count;
    document.getElementById("val-lcs-len").textContent = data.lcs_length;
    document.getElementById("val-lcs-ret-orig").textContent = `${data.retained_ratio_original}%`;
    document.getElementById("val-lcs-ret-rev").textContent = `${data.retained_ratio_revised}%`;
    document.getElementById("val-lcs-diff").textContent = `~${data.words_removed_approx + data.words_added_approx} words`;

    const container = document.getElementById("lcs-words-container");
    container.innerHTML = "";

    if (data.lcs_words && data.lcs_words.length > 0) {
        data.lcs_words.forEach(word => {
            const pill = document.createElement("span");
            pill.className = "lcs-token-pill";
            pill.textContent = word;
            container.appendChild(pill);
        });
    } else {
        container.innerHTML = `<span style="font-size:13px; color:#94a3b8;">No common word sequence identified between drafts.</span>`;
    }

    document.getElementById("lcs-results").classList.remove("hidden");
}

// =====================================================================
// SECTION E: REPORT EXPORT (TXT & CSV)
// =====================================================================
function exportTxtReport() {
    if (!state.analysis) {
        showToast("Run Content Analysis first before exporting a report.", "error");
        return;
    }

    const a = state.analysis;
    const m = a.metrics;
    const p = a.presence;
    const timestamp = new Date().toISOString().replace("T", " ").substring(0, 19);

    let content = `========================================================================\n`;
    content += `SEO WORD OPTIMIZER - ACADEMIC ANALYSIS REPORT\n`;
    content += `B.Tech Design & Analysis of Algorithms (DAA) Mini-Project\n`;
    content += `Generated at: ${timestamp}\n`;
    content += `========================================================================\n\n`;

    content += `1. ARTICLE DETAILS\n`;
    content += `------------------------------------------------------------------------\n`;
    content += `Title: ${document.getElementById("input-title").value || "N/A"}\n`;
    content += `Target Keyword: ${m.target_keyword || "None"}\n`;
    content += `Word Count: ${m.word_count}\n`;
    content += `Character Count: ${m.character_count} (${m.character_count_no_spaces} without spaces)\n`;
    content += `Sentence Count: ${m.sentence_count}\n`;
    content += `Paragraph Count: ${m.paragraph_count}\n`;
    content += `Keyword Count: ${m.target_keyword_count}\n`;
    content += `Keyword Density: ${m.target_keyword_density}%\n\n`;

    content += `2. STRUCTURAL PLACEMENT CHECKS\n`;
    content += `------------------------------------------------------------------------\n`;
    content += `Keyword in Title: ${p.title_has_keyword ? "YES" : "NO"}\n`;
    content += `Keyword in Introduction: ${p.intro_has_keyword ? "YES" : "NO"}\n`;
    content += `Headings with Keyword: ${p.headings_with_keyword} of ${p.heading_count}\n\n`;

    content += `3. TOP KEYWORDS (STOP WORDS FILTERED)\n`;
    content += `------------------------------------------------------------------------\n`;
    content += `Rank | Keyword                       | Occurrences\n`;
    content += `-----+-------------------------------+------------\n`;
    (a.filtered_frequencies || []).slice(0, 20).forEach((item, idx) => {
        const rankStr = String(idx + 1).padEnd(4);
        const wordStr = item.word.padEnd(29);
        const countStr = String(item.count).padStart(11);
        content += `${rankStr} | ${wordStr} | ${countStr}\n`;
    });
    content += `\n`;

    if (state.sorting) {
        content += `4. DAA SORTING BENCHMARK (MERGE SORT vs QUICK SORT)\n`;
        content += `------------------------------------------------------------------------\n`;
        content += `Input Size: ${state.sorting.input_size} items\n`;
        content += `Repetitions: ${state.sorting.repetitions} runs\n`;
        content += `Merge Sort Avg Time: ${state.sorting.merge_sort.avg_time_ms.toFixed(5)} ms\n`;
        content += `Quick Sort Avg Time: ${state.sorting.quick_sort.avg_time_ms.toFixed(5)} ms\n`;
        content += `Outputs Match: ${state.sorting.outputs_match ? "100% IDENTICAL" : "MISMATCH"}\n\n`;
    }

    if (state.lcs) {
        content += `5. DAA DRAFT COMPARISON (LONGEST COMMON SUBSEQUENCE)\n`;
        content += `------------------------------------------------------------------------\n`;
        content += `Original Words (m): ${state.lcs.original_word_count}\n`;
        content += `Revised Words (n): ${state.lcs.revised_word_count}\n`;
        content += `LCS Length: ${state.lcs.lcs_length} words\n`;
        content += `Retention Ratio (Original): ${state.lcs.retained_ratio_original}%\n`;
        content += `Retention Ratio (Revised): ${state.lcs.retained_ratio_revised}%\n`;
        content += `Retained Sequence: ${state.lcs.lcs_words.join(" ")}\n\n`;
    }

    content += `6. EDUCATIONAL RECOMMENDATIONS\n`;
    content += `------------------------------------------------------------------------\n`;
    (a.recommendations || []).forEach(rec => {
        content += `[${rec.category}] (${rec.type.toUpperCase()}): ${rec.message}\n`;
    });
    content += `\n`;

    content += `========================================================================\n`;
    content += `LIMITATIONS & DISCLAIMER:\n`;
    content += `This report is computed locally using deterministic text analysis algorithms.\n`;
    content += `It does not predict Google search rankings or guarantee indexing.\n`;
    content += `========================================================================\n`;

    downloadFile(content, "seo_analysis_report.txt", "text/plain");
}

function exportCsvReport() {
    if (!state.analysis || !state.analysis.filtered_frequencies) {
        showToast("Run Content Analysis first before exporting CSV.", "error");
        return;
    }

    const freqs = state.analysis.filtered_frequencies;
    let csv = `Rank,Keyword,Occurrences\n`;
    freqs.forEach((item, idx) => {
        csv += `${idx + 1},"${item.word.replace(/"/g, '""')}",${item.count}\n`;
    });

    downloadFile(csv, "seo_keyword_frequencies.csv", "text/csv");
}

function downloadFile(content, filename, mimeType) {
    const blob = new Blob([content], { type: mimeType });
    const url = URL.createObjectURL(blob);
    const a = document.createElement("a");
    a.href = url;
    a.download = filename;
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    URL.revokeObjectURL(url);
    showToast(`Downloaded ${filename}`, "success");
}

function escapeHtml(str) {
    if (!str) return "";
    return String(str)
        .replace(/&/g, "&amp;")
        .replace(/</g, "&lt;")
        .replace(/>/g, "&gt;")
        .replace(/"/g, "&quot;")
        .replace(/'/g, "&#039;");
}
