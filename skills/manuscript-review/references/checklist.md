# Pre-Publication Manuscript Review Checklist

**Note:** This checklist is optimized for arXiv/preprint submissions. Items marked
with ★ are high priority for technical quality and reproducibility. Items marked
with ◆ are recommendations that may be relaxed for arXiv. Venue-specific formatting
and compliance requirements (§18) are generally N/A for arXiv.

## 1. Macro-Coherence & Argumentative Architecture

- [ ] ★ **Thesis-thread continuity**: Trace the central claim from abstract → introduction → each section → discussion → conclusion. Major gaps reduce clarity.
- [ ] ★ **Narrative arc integrity**: Does the paper follow a coherent logical flow, or does it fork into unresolved threads?
- [ ] ◆ **Section-level necessity test**: For each section, consider whether it serves the central argument. Extraneous sections dilute focus.
- [ ] ◆ **Scope boundary enforcement**: Content should align with stated contributions. Scope creep reduces impact.
- [ ] ★ **Logical dependency ordering**: If Section N depends on concepts from Section M, then M < N. Forward dependencies confuse readers.
- [ ] ◆ **Transition sufficiency**: Section connections help readability. Abrupt transitions increase cognitive load.
- [ ] ★ **Argument-evidence coupling**: Claims should be near their supporting evidence (citation, data, derivation). Orphaned claims damage credibility.

## 2. Abstract as Standalone Document

- [ ] ★ **Functional completeness**: Context → Gap → Approach → Results → Implication. Clear structure helps readers quickly assess relevance.
- [ ] ★ **Quantitative specificity**: Include concrete metrics. "14.3% reduction" beats "significant improvement." Builds credibility.
- [ ] ◆ **No undefined acronyms**: Expand abbreviations in abstract. Good practice but flexible for arXiv.
- [ ] ◆ **No citations in abstract**: Generally avoid, but arXiv is flexible.
- [ ] ★ **Promise-delivery alignment**: Abstract should match paper content. Overclaiming damages trust.
- [ ] ◆ **Keyword-abstract coherence**: Keywords in abstract text improve discoverability.

## 3. Title Calibration

- [ ] **Precision-scope match**: Title specifies exactly the domain, method class, and contribution type. Overly broad titles signal unfocused work.
- [ ] **No question titles** unless the paper genuinely explores rather than asserts (rare in empirical work).
- [ ] **No colon-separated titles** unless the subtitle genuinely disambiguates (most colon titles are lazy two-part constructions where one part suffices).
- [ ] **Indexability**: Title contains the 2–3 terms a researcher in your subfield would actually search for.

## 4. Introduction Architecture

- [ ] ★ **Funnel structure**: Broad context → specific gap → contribution → organization. Clear structure aids comprehension.
- [ ] ★ **Gap statement explicitness**: State the specific gap or problem, not vague "more work is needed." Establishes motivation.
- [ ] ★ **Contribution enumeration**: List specific contributions explicitly. Helps readers assess relevance and novelty.
- [ ] ◆ **No results in introduction**: High-level summary acceptable, but detailed results belong in results section.
- [ ] ◆ **Related work positioning**: If in introduction, should motivate the gap rather than comprehensive survey.

## 5. Related Work / Literature Review

- [ ] **Taxonomic organization**: Grouped by methodological approach, conceptual framework, or chronological evolution — not random listing.
- [ ] **Critical synthesis, not annotation**: Each cited work must be evaluated relative to your contribution. "X did Y" is annotation. "X did Y, but their approach assumes Z, which fails under condition W that our method addresses" is synthesis.
- [ ] **Recency coverage**: At minimum, all relevant work from the last 24 months in the target venue and top-3 adjacent venues.
- [ ] **Self-citation calibration**: Present where genuinely relevant; absent where it's padding. Reviewers notice both excesses.
- [ ] **Competitor fairness**: Characterize competing approaches accurately. Straw-manning rival methods is detectable and damages credibility.
- [ ] **Explicit differentiation statement**: A single paragraph or table delineating exactly how your work differs from the closest 3–5 prior contributions.

## 6. Methodology / Technical Exposition

- [ ] ★ **Reproducibility sufficiency**: A competent practitioner should be able to understand and replicate the approach from the paper's description alone. Underspecified methods reduce trust and impact. _(Document-level check. For code-level verification → manuscript-provenance §1, §7.)_
- [ ] ★ **Assumption explicitness**: Key modeling assumptions should be stated and justified. Hidden assumptions damage credibility.
- [ ] ★ **Notation consistency**: Symbols should be defined at first use and used consistently. Symbol conflicts confuse readers.
- [ ] ◆ **Equation-text integration**: Equations work best when introduced in prose with variables defined nearby. Improves readability.
- [ ] ◆ **Algorithm pseudocode**: Non-trivial procedures benefit from pseudocode alongside prose description. Aids understanding.
- [ ] ◆ **Complexity analysis**: Time/space complexity for algorithms helps readers assess scalability.
- [ ] ★ **Hyperparameter specification**: List key hyperparameters and selection rationale in the paper. Essential for reproducibility. _(Checks paper lists them. For verifying values match code/config → manuscript-provenance §1, §8.)_

## 7. Experimental Design & Results

- [ ] ★ **Baseline adequacy**: Include meaningful baselines—ablations, relevant comparisons, simple baselines for scale. Missing baselines weaken claims.
- [ ] ★ **Dataset characterization**: Describe size, splits, preprocessing. Under-characterized data hinders reproducibility.
- [ ] ★ **Statistical rigor**: Report variance (confidence intervals, std dev) for stochastic methods. Single runs lack credibility.
- [ ] ◆ **Effect size, not just p-values**: Statistical significance should accompany practical significance. Effect sizes add context.
- [ ] ◆ **Evaluation metric justification**: Explain metric choices, especially if non-standard. Helps readers assess relevance.
- [ ] ◆ **Table/figure self-containment**: Captions should enable interpretation without body text. Improves accessibility.
- [ ] ★ **Result-claim alignment**: Claims should trace to specific evidence (tables, figures, tests). Unsupported claims damage trust.
- [ ] ◆ **Negative results reporting**: Reporting null/negative results improves transparency and prevents publication bias.
- [ ] ◆ **Computational cost reporting**: Hardware specs and runtime reported in paper. Especially important for expensive methods. _(Checks paper reports them. For verifying values trace to benchmarking scripts → manuscript-provenance §1.)_

## 8. Discussion & Interpretation

- [ ] **No new results**: Discussion interprets existing results; it does not introduce unreported findings.
- [ ] **Alternative explanations**: For every key finding, at least one plausible alternative explanation considered and addressed.
- [ ] **Generalizability boundary**: Explicit statement of conditions under which results are expected to hold and conditions under which they may not.
- [ ] **Connection to prior work**: Results contextualized against related work findings. Agreement and disagreement with prior results both acknowledged and explained.
- [ ] **Implications scoped to evidence**: Implications must be proportional to the evidence presented. Do not extrapolate from a single-dataset evaluation to field-wide conclusions.

## 9. Limitations

- [ ] ★ **Genuine, not performative**: Identify actual weaknesses, not vague "future work could use more data." Builds trust.
- [ ] ◆ **Preemptive acknowledgment**: Addressing likely objections strengthens credibility. Especially valuable for peer review.
- [ ] ◆ **Threat-to-validity taxonomy**: Consider internal (confounds), external (generalizability), and construct (metric alignment) validity.
- [ ] ◆ **Mitigation or acknowledgment**: Note whether limitations were mitigated or accepted. Shows thoughtfulness.

## 10. Conclusion

- [ ] **No new information**: Summary only. Any new claim here is a structural defect.
- [ ] **Contribution restatement**: Map back to the enumerated contributions from the introduction. 1:1 correspondence.
- [ ] **Future work specificity**: "Future work will explore X" is weak. "Future work will extend the approach to domain Y by modifying component Z, pending resolution of limitation W" is actionable.

## 11. Citation & Reference Hygiene

- [ ] ★ **Citation-reference bijection**: Every citation should have a reference entry; every reference should be cited. Orphans suggest carelessness.
- [ ] ◆ **Style conformance**: Consistent citation style improves professionalism. ArXiv is flexible but consistency matters.
- [ ] ◆ **Primary source preference**: Cite original papers when possible. Builds stronger foundation.
- [ ] ◆ **Preprint/publication status**: Update arXiv citations to published versions when available. Shows thoroughness.
- [ ] ◆ **Self-consistency**: Mixed citation styles (some with DOIs, some without) reduce polish.
- [ ] ★ **Citation placement**: Citations near their claims improve credibility and verifiability.
- [ ] ◆ **Retraction check**: Verify cited works haven't been retracted. Rare but important.

## 12. Figures & Tables

- [ ] **Sequential callout ordering**: First mention of Figure 1 precedes first mention of Figure 2 in body text. No out-of-order callouts.
- [ ] **Resolution and legibility**: All text within figures readable at print scale (minimum ~8pt equivalent). Vector formats (PDF/SVG) for plots; raster (PNG ≥300 DPI) only for photographs or screenshots. _(Document quality check. For verifying figures are script-generated in correct format → manuscript-provenance §3.)_
- [ ] **Colorblind accessibility**: No red-green only differentiation. Use colorblind-safe palettes (viridis, cividis) or redundant encoding (shape + color).
- [ ] **Axis labels with units**: Every axis labeled with quantity and unit. No unitless axes unless the quantity is genuinely dimensionless.
- [ ] **Consistent visual language**: Same color/marker/line-style mapping across all figures for the same method/condition. _(Document consistency. For verifying visual config is code-defined → manuscript-provenance §3.)_
- [ ] **No chartjunk**: No 3D effects, unnecessary gridlines, or decorative elements. Maximize data-ink ratio.
- [ ] **Table alignment**: Decimal-aligned numeric columns. Left-aligned text columns. No center-aligned numbers.
- [ ] **Significant figure consistency**: Same number of decimal places for the same metric across all tables. _(Internal document consistency. For verifying precision matches script output → manuscript-provenance §2.)_

## 13. Language & Prose Mechanics (Recommendations for arXiv)

- [ ] ◆ **Tense consistency**: Generally: methods = past, established facts = present, results = past. Consistency matters more than strict adherence.
- [ ] ◆ **Hedging calibration**: Avoid overclaiming ("proves") and under-hedging ("might possibly"). Aim for precise claims.
- [ ] ◆ **Active voice preference**: Active voice improves clarity. Passive is fine for methodology ("The model was trained"). Mixed usage is acceptable.
- [ ] ◆ **Nominalization reduction**: "We analyzed" beats "We performed an analysis of". Reduces word count, improves clarity.
- [ ] ◆ **Sentence length variance**: Mix sentence lengths for readability. Not a strict requirement.
- [ ] ◆ **Paragraph unity**: One idea per paragraph generally works well. Flexible guideline.
- [ ] ◆ **Weasel word check**: "Clearly", "obviously", "it is well known" add little. Consider removing, but not mandatory.
- [ ] ◆ **Marketing language**: "Novel", "state-of-the-art" are acceptable with supporting evidence. ArXiv allows more informal tone than journals.

## 14. Abbreviations & Nomenclature

- [ ] **First-use expansion**: Every abbreviation expanded at first occurrence in body text. Separately expanded in abstract if used there.
- [ ] **Abbreviation necessity test**: If the term appears fewer than ~5 times total, don't abbreviate. The cognitive load of tracking the abbreviation exceeds the space savings.
- [ ] **No ambiguous abbreviations**: If the same abbreviation maps to multiple expansions within the field, disambiguate or avoid.
- [ ] **Abbreviation list**: If venue requires or permits a nomenclature/abbreviation table, include it. If not, verify internal consistency suffices.
- [ ] **Consistent use post-definition**: After defining an abbreviation, use it exclusively. Do not alternate between the abbreviation and the full form.

## 15. Mathematical Typesetting & Notation

- [ ] **Scalar/vector/matrix convention**: Consistent typographic distinction (e.g., italic lowercase for scalars, bold lowercase for vectors, bold uppercase for matrices). Stated explicitly if non-standard.
- [ ] **Operator formatting**: Standard operators (log, sin, exp, argmax) in upright/roman, not italic. Custom operators defined before use.
- [ ] **Equation numbering**: Number only referenced equations. Unreferenced equations numbered = visual noise.
- [ ] **Punctuation in equations**: Equations are part of sentences. They take commas, periods, and conjunctions as grammatically appropriate.
- [ ] **Consistent subscript/superscript semantics**: Subscripts for indices, superscripts for exponents or labels — or whatever convention you adopt, applied uniformly.
- [ ] **Definition before use**: No symbol appears in an equation before its textual definition. Zero tolerance.

## 16. Supplementary Material & Appendices

- [ ] **Necessity audit**: Supplementary material contains details that support but are not essential to the core argument. If removing it weakens the paper, it belongs in the main text.
- [ ] **Cross-reference integrity**: All references to supplementary material from the main text resolve correctly (Appendix A, Supplementary Figure S1, etc.).
- [ ] **Standalone readability**: Supplementary material should be interpretable with minimal back-reference to the main text.

## 17. Ethical, Legal & Administrative Compliance (Recommended for arXiv)

- [ ] ◆ **Ethics statement**: If human subjects involved, consider including IRB approval statement. Not required for arXiv.
- [ ] ◆ **Data availability statement**: Stating dataset access in the paper improves reproducibility and impact. Recommended. _(Checks statement exists. For verifying data is versioned/tracked → manuscript-provenance §10.)_
- [ ] ◆ **Code availability statement**: Repository links in the paper strongly recommended. Increases citations and reproducibility. _(Checks statement exists. For verifying repo URL validity and README accuracy → manuscript-provenance §11.)_
- [ ] ◆ **Conflict of interest**: Optional for arXiv. Standard for journals.
- [ ] ◆ **Funding acknowledgment**: Optional but common practice. Include if applicable.
- [ ] ◆ **Author contributions**: Optional for arXiv. Required by some journals.
- [ ] ◆ **License compatibility**: If using third-party code/data/models, verify licenses permit your use. Good practice.

## 18. Submission-Specific Formatting (N/A for arXiv by default)

- [ ] N/A **Page/word limits**: ArXiv has no page limits. Ignore unless targeting a specific conference/journal.
- [ ] N/A **Template conformance**: ArXiv accepts standard LaTeX. No strict template requirements.
- [ ] N/A **Anonymization**: ArXiv is not anonymous. Author names appear in submissions.
- [ ] ◆ **File size limits**: ArXiv has reasonable limits (~1GB). Rarely an issue.
- [ ] N/A **Supplementary format requirements**: ArXiv accepts common file types. Very flexible.

## 20. Claims-Evidence Calibration

- [ ] ★ **Claim-evidence strength match**: Every assertion graded by claim strength (strong/definitive, moderate/qualified, hedged/tentative) and evidence strength (direct experimental, indirect/correlational, citation-only, analogical, none). Mismatches flagged — strong claim on weak evidence = overclaim; hedged claim on strong evidence = underclaim.
- [ ] ★ **Causal language audit**: "causes", "leads to", "results in", "produces", "drives" only with causal evidence (controlled experiment, intervention study). Correlational evidence permits "is associated with", "co-occurs with", "predicts". Mixing causal language with correlational evidence is overclaiming.
- [ ] ★ **Quantifier precision**: "significant" means statistically significant with reported test. "Large", "substantial", "considerable" have reference scale. "Most", "many", "few" have approximate counts or proportions. Naked quantifiers without anchoring are weasel words masquerading as precision.
- [ ] ★ **Generalization scope match**: Claims about "X in general" supported by evidence spanning conditions sufficient for generalization. Claims from single-dataset results scoped to that dataset. Claims from one domain do not generalize to "any domain" without transfer evidence.
- [ ] ★ **Comparative claim grounding**: "better than", "outperforms", "superior to", "improves upon" backed by head-to-head comparison on shared evaluation. No comparative claims against methods not actually evaluated in the paper.
- [ ] ★ **Negation claim rigor**: "X does not affect Y" requires evidence of absence (null result with adequate power/sensitivity analysis), not absence of evidence (didn't test it). "We found no effect" is different from "there is no effect."
- [ ] ★ **Attribution specificity**: Claims about what "the model does" or "the method achieves" backed by analysis isolating the contribution (ablation, controlled comparison). Without isolation, the claim is about the full pipeline, not the specific component.
- [ ] ★ **Hedging-evidence inversion detection**: Paragraphs where strong experimental results are described with "may suggest", "could indicate", "appears to show" — the evidence is doing the work, the language is hiding it. Sharpen to match the evidence.
- [ ] ★ **Implicit claim detection**: Sentences that imply superiority, novelty, or generality without stating it explicitly. "Unlike prior work, our approach handles X" implies prior work cannot handle X — verify this is supported. Implicit claims dodge scrutiny but still register with readers.
- [ ] ◆ **Result cherry-picking check**: All reported metrics consistent across tables/figures. No selective reporting of metrics where the method performs well while omitting metrics where it doesn't. Negative or mixed results acknowledged.

## 21. Narrative Flow & Coherence

- [ ] ★ **Sentence-to-sentence coherence**: Each sentence connects logically to the previous one. No unexplained topic shifts between adjacent sentences. A reader should never ask "why is this sentence here?" within a paragraph.
- [ ] ★ **Given-new information contract**: Sentences open with known/established information (given) and close with new information (new). Violating this forces the reader to hold unanchored new concepts while searching for the connection. Systematic violation makes prose feel disjointed even when individual sentences are clear.
- [ ] ★ **Paragraph topic discipline**: First sentence of each paragraph states or clearly implies the paragraph's main point. No buried leads — key information in paragraph openers, not midway through or at the end. Readers scan topic sentences to navigate; buried leads defeat this.
- [ ] ★ **Cross-sentence reference ordering**: If sentence 3 discusses content from sentence 1, and sentence 4 discusses content from sentence 2, the reader zigzags between referents. Reorder so references flow forward sequentially: 1→3→2→4 becomes 1→3, 2→4 or interleave cleanly.
- [ ] ★ **Logic gap detection**: Conclusions that skip premises. "A is true. Therefore C." — missing the B that connects them. The author knows B implicitly; the reader does not. Each inferential step must be stated or explicitly cited.
- [ ] ★ **Paragraph-to-paragraph transition**: Last sentence of paragraph N connects thematically to first sentence of paragraph N+1. No hard cuts where the reader must infer the relationship between consecutive paragraphs.
- [ ] ◆ **No premature forward references**: Do not mention a concept, method, or result that hasn't been introduced yet without explicit forward-reference signaling ("as we describe in Section X"). Unnamed forward references ("this approach, described later") force the reader to hold unresolved references.
- [ ] ◆ **No orphaned setups**: If a paragraph introduces a concept, question, or promise ("We address this in three ways"), the same section delivers on it completely. Setup without payoff in the same section is a structural defect.
- [ ] ◆ **Argument momentum**: The text moves forward. No paragraph that could be deleted without breaking the logical chain. No paragraph that restates a previous paragraph's conclusion as its own contribution. Each paragraph advances the argument by at least one step.
- [ ] ◆ **Section-internal arc**: Each section has a discernible beginning (what this section does), middle (the content), and end (what was established). Sections that just stop without landing the point leave the reader unanchored.

## 22. Prose Microstructure

- [ ] ★ **Referential clarity**: "this", "it", "they", "these results", "the approach", "the method" must have unambiguous antecedents within 1-2 sentences. If two plausible referents exist, the pronoun or demonstrative is ambiguous. Replace with the specific noun. "This" as a sentence opener without a following noun ("This shows...") is almost always ambiguous — use "This result shows..." or "This pattern shows..."
- [ ] ★ **Information density balance**: No paragraph introducing >4 genuinely new concepts (terms, methods, results). No paragraph that restates known information without adding anything new. Uneven density creates cognitive whiplash — the reader is overwhelmed then bored in alternation.
- [ ] ★ **Sentence-level clarity ceiling**: No sentence requiring >2 re-reads by a domain expert. If a domain-knowledgeable reader struggles, the sentence is too complex regardless of its technical accuracy. Decompose into multiple sentences or restructure.
- [ ] ◆ **Parallel structure in lists and comparisons**: Items in a list, elements of a comparison, and steps in a sequence use consistent grammatical form. "The method (1) reduces error, (2) faster training, (3) is more robust" mixes verb phrase, noun phrase, and clause. Pick one form.
- [ ] ◆ **Semantic redundancy across paragraphs**: Same point made in different words in nearby paragraphs or across sections without explicit purpose (such as a summary). Redundancy wastes reader attention and signals disorganized drafting.
- [ ] ◆ **Antecedent distance**: A concept introduced in paragraph N and referenced in paragraph N+3 or later without re-anchoring forces the reader to scroll back. Re-establish the referent briefly when distance exceeds ~2 paragraphs.
- [ ] ◆ **Excessive clause embedding**: No more than 2 levels of subordinate clauses per sentence. "The method, which was developed by X, who previously showed that Y, which contradicts Z, ..." is syntactically valid but cognitively hostile. Break into multiple sentences.
- [ ] ◆ **Dangling and misplaced modifiers**: "Using gradient descent, the loss function converged" — gradient descent is not an agent performing convergence. "Trained on ImageNet, we evaluate..." — the authors were not trained on ImageNet. These are common in technical writing and create momentary confusion.

## 23. Rendered Document Inspection

Visual defects that exist only in the compiled PDF, invisible from source alone.
This pass requires reading the actual rendered output.

- [ ] ★ **Figure text legibility**: All text within figures (axis labels, tick labels, annotations, legend entries) readable at the actual rendered size. Minimum ~8pt equivalent at print scale. Figures shrunk to column width often render annotations illegible.
- [ ] ★ **Axis label overlap and rotation**: Tick labels that overlap, collide, or require rotation to be readable. Common with categorical axes (>10 categories), date axes, or long feature names. Rotation should be applied in the plotting script, not assumed from source.
- [ ] ★ **Legend occlusion**: Legends that cover data points, trend lines, or other meaningful content. Legend placement outside the plot area or in a data-free region.
- [ ] ★ **Float placement proximity**: Figures and tables appear within ~1 page of their first text reference. LaTeX float placement (`[htbp]`) often pushes figures pages away from the referring paragraph. The reader encounters "as shown in Figure 3" and Figure 3 is three pages later.
- [ ] ★ **Table rendering integrity**: Tables render without column overflow, text wrapping that destroys alignment, or content truncation. Multi-column tables at column width are the usual failure mode.
- [ ] ★ **Page break placement**: No page breaks splitting: a table in half, an equation from its preceding sentence, a figure from its caption, a section header from its first paragraph. These are typographic failures that damage readability.
- [ ] ◆ **Margin overflow**: No content (figures, equations, tables, URLs) bleeding outside page margins. Common with wide tables, long equations, and unbroken URLs.
- [ ] ◆ **Font size consistency across figures**: All figures use comparable font sizes for equivalent elements (axis labels, titles, annotations). A 14pt title on Figure 1 and 8pt title on Figure 2 is visually jarring.
- [ ] ◆ **White space distribution**: No orphaned section headers at page bottoms (header with no following content on the same page). No excessive white space from float placement forcing large gaps.
- [ ] ◆ **Caption proximity**: Captions render immediately adjacent to their figure or table, not separated by a page break or intervening content. LaTeX occasionally places captions on a different page than their figure.
- [ ] ◆ **Color in print/grayscale**: If the venue or audience may print in grayscale, figures remain interpretable without color. Lines/markers distinguishable by shape/pattern, not color alone.
- [ ] ○ **Hyperlink rendering**: URLs and cross-references render as clickable links (if hyperref is used) and don't overflow margins or break awkwardly across lines.
- [ ] ○ **Header/footer consistency**: Page numbers, running headers, and footers consistent and correctly formatted throughout.

**Detection method:** Open the compiled PDF. Inspect every page. For each figure, zoom to actual print size (100% at print DPI) and verify legibility. For each table, check column alignment at rendered width. For each float, measure distance from first reference to actual placement.

---

## 24. Cross-Element Coherence

The manuscript is an integrated system. Prose, figures, tables, captions, macros,
and cross-references must be mutually consistent — not just individually correct.

- [ ] ★ **Prose-figure alignment**: Every prose claim about a figure matches what the figure actually shows. "Figure 3 shows convergence after 50 epochs" — verify the figure shows convergence, and around epoch 50, not epoch 200. "The gap widens at higher values" — verify the figure shows a widening gap.
- [ ] ★ **Prose-table alignment**: Every prose interpretation of a table matches the table data. "Method A outperforms all baselines" — verify Table N confirms this for all reported metrics, not just one. "The difference is statistically significant" — verify the table includes significance indicators.
- [ ] ★ **Caption-content currency**: Every caption describes the current version of its figure or table. Stale captions from previous manuscript versions are common: the figure changed but the caption still describes the old version. Check that specific values, axis descriptions, and qualitative claims in captions match the actual visual.
- [ ] ★ **Macro-prose coherence**: When a macro injects a value into prose, the surrounding language must be appropriate for that value. "\bestf{} represents a marginal improvement" — if `\bestf` = 14.3%, "marginal" is wrong. "Our method achieves \accuracy{}" — if `\accuracy` = 0.51, the upbeat framing is inappropriate. The prose was often written for a different value during an earlier draft.
- [ ] ★ **Cross-reference accuracy**: Every `\ref{fig:X}` points to the correct figure AND the surrounding text describes what that figure actually contains. A renumbered or reordered figure set can leave references pointing to the wrong visual. "Figure 2 shows the architecture" but Figure 2 is now a training curve because a figure was inserted before it.
- [ ] ★ **Value consistency across elements**: The same quantity appearing in text, tables, figures, and captions has the same value everywhere. An abstract claiming "14.3% improvement", Table 2 showing 14.28%, and Figure 4's annotation showing 14.3% are consistent. But "14.3%" in text and "13.8%" in the table for the same metric is a defect.
- [ ] ◆ **Figure ordering vs. narrative**: Figures appear in the document in approximately the order the narrative references them. If the text discusses Figure 1, then Figure 4, then Figure 2, the narrative structure or figure numbering needs revision.
- [ ] ◆ **Terminology consistency across elements**: The same method/dataset/metric uses the same name in prose, figure legends, table headers, and captions. "BERT-large" in text, "BERT-L" in the table header, "bert_large" in the figure legend = three names for one thing.
- [ ] ◆ **Table-figure consistency**: When a table and figure present related data (e.g., Table 2 has exact numbers, Figure 3 plots them), the values are consistent. The figure's visual impression matches the table's numbers.
- [ ] ◆ **Temporal consistency**: All elements reflect the same experimental run or version. A figure from run A, a table from run B, and prose interpreting run C is a coherence failure even if each element is individually valid.
- [ ] ○ **Supplementary-main alignment**: Claims in the main text about supplementary content ("see Appendix A for ablation results") match what the supplementary actually contains.

**Detection method:** For each figure and table, read (1) the visual/data itself, (2) its caption, (3) every prose passage that references it, (4) any macro values appearing nearby. Check four-way consistency. For macro-injected values, read the value and the sentence it sits in — does the qualitative language match the quantitative value?

---

## 19. Final Quality Check (Recommendations)

- [ ] ◆ **Cold read**: Reading after time away helps catch clarity issues. Recommended.
- [ ] ◆ **Critical read**: Consider potential criticisms and address proactively. Strengthens arguments.
- [ ] ◆ **Weak language sweep**: Consider removing filler words like "very", "really", "quite", "basically", "essentially". Improves precision. Not mandatory for arXiv.
- [ ] N/A **Orphan/widow check**: Typesetting detail. Not relevant for arXiv.
- [ ] ★ **Hyperlink verification**: Broken links damage credibility. Test URLs and DOIs.
- [ ] ◆ **PDF metadata**: Clean metadata is professional. Not critical for arXiv.
- [ ] N/A **Venue guidelines check**: ArXiv has minimal requirements. For journal resubmission, review venue guidelines.

---

## Priority Legend

- **★ High Priority** — Impacts technical credibility, reproducibility, or clarity. Focus here for arXiv quality.
- **◆ Recommended** — Quality improvements that strengthen the work. Address if time permits.
- **N/A** — Not applicable for arXiv submissions. Relevant for journal/conference submissions.

**ArXiv Review Focus:**

- Technical rigor (§6-7): reproducibility, assumptions, baselines, statistics
- Claims-evidence calibration (§20): every claim matched to evidence strength
- Narrative flow (§21): logical coherence at sentence, paragraph, and section level
- Clarity (§1-2, 4): coherent structure, clear contributions, complete abstract
- Prose microstructure (§22): referential clarity, information density, readability
- Rendered inspection (§23): visual defects only visible in compiled PDF
- Cross-element coherence (§24): prose, figures, tables, macros mutually consistent
- Citations (§11): proper attribution, no orphans
- Code/data availability (§17): strongly recommended for reproducibility

**Flexible for ArXiv:**

- Strict formatting (§18): N/A
- Prose mechanics (§13): recommendations, not requirements
- Compliance statements (§17): optional but recommended
- Marketing language: acceptable with evidence
