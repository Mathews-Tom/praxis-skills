# Manuscript Provenance Report

**Manuscript:** [Title]
**Codebase:** [Repository/directory path]
**Audit Date:** [Date]
**Companion Report:** [Link to manuscript-review report if exists, or "Not yet run"]

---

## 1. Provenance Summary

**Overall Provenance Score:** [X / Y artifacts traced] ([Z]%)

| Category      | Traced | Untraced | Stale | Manual | Total |
| ------------- | ------ | -------- | ----- | ------ | ----- |
| Inline values |        |          |       |        |       |
| Table cells   |        |          |       |        |       |
| Figures       |        |          |       |        |       |
| LaTeX macros  |        |          |       |        |       |
| Terminology   |        |          |       |        |       |
| Orderings     |        |          |       |        |       |
| **Total**     |        |          |       |        |       |

**Verdict:** [Fully traceable | Mostly traceable | Significant gaps | Not reproducible]

**Pipeline Status:** [Complete | Partial | Missing]

**Top 5 Remediation Actions:**

1. [CRITICAL/HIGH item — location and action]
2. [CRITICAL/HIGH item — location and action]
3. [CRITICAL/HIGH item — location and action]
4. [HIGH/MEDIUM item — location and action]
5. [HIGH/MEDIUM item — location and action]

---

## 2. Provenance Map

### 2a. Value Provenance

| Manuscript Location | Value | Status        | Source Script            | Output File            | Config Key                  |
| ------------------- | ----- | ------------- | ------------------------ | ---------------------- | --------------------------- |
| Abstract, L3        | 94.2% | TRACED        | `scripts/evaluate.py:47` | `results/metrics.json` | —                           |
| §4.1, L12           | 0.001 | CONFIG-TRACED | —                        | —                      | `config.toml:learning_rate` |
| §4.3, L8            | 1.47× | UNTRACED      | —                        | —                      | —                           |
| ...                 |       |               |                          |                        |                             |

**Summary:** [X] values traced, [Y] untraced, [Z] stale.

### 2b. Table Provenance

| Table   | Status    | Generation Script        | Data Source            | Ordering                     | Notes                   |
| ------- | --------- | ------------------------ | ---------------------- | ---------------------------- | ----------------------- |
| Table 1 | GENERATED | `scripts/make_table1.py` | `results/main.csv`     | CODE-ORDERED (desc accuracy) |                         |
| Table 2 | PARTIAL   | `scripts/make_table2.py` | `results/ablation.csv` | MANUAL-ORDER                 | Rows 3-5 manually added |
| Table 3 | MANUAL    | —                        | —                      | MANUAL-ORDER                 | No generation script    |
| ...     |           |                          |                        |                              |                         |

**Summary:** [X] tables fully generated, [Y] partial, [Z] manual.

### 2c. Figure Provenance

| Figure | Status      | Generation Script          | Data Source            | Seed | Post-edited                |
| ------ | ----------- | -------------------------- | ---------------------- | ---- | -------------------------- |
| Fig 1  | GENERATED   | `scripts/plot_main.py`     | `results/main.csv`     | 42   | No                         |
| Fig 2  | STALE       | `scripts/plot_ablation.py` | `results/ablation.csv` | 42   | No                         |
| Fig 3  | POST-EDITED | `scripts/plot_arch.py`     | —                      | —    | Yes (Illustrator metadata) |
| Fig 4  | MANUAL      | —                          | —                      | —    | —                          |
| ...    |             |                            |                        |      |                            |

**Summary:** [X] figures generated, [Y] stale, [Z] post-edited, [W] manual.

### 2d. LaTeX Macro Audit

**Generated macro files:**

| File                       | Source Script               | Macro Count | Status  |
| -------------------------- | --------------------------- | ----------- | ------- |
| `generated/metrics.tex`    | `scripts/export_metrics.py` | 12          | CURRENT |
| `generated/data-stats.tex` | `scripts/data_summary.py`   | 8           | STALE   |
| ...                        |                             |             |         |

**Inline macro definitions (in .tex source — suspect):**

| File       | Line | Macro          | Value     | Verdict                    |
| ---------- | ---- | -------------- | --------- | -------------------------- |
| `main.tex` | 15   | `\nsamples`    | `10,432`  | DATA — should be generated |
| `main.tex` | 16   | `\projectname` | `DeepFoo` | EDITORIAL — acceptable     |
| ...        |      |                |           |                            |

**Bare numbers (not macro-wrapped):**

| File          | Line | Value    | Context             | Severity |
| ------------- | ---- | -------- | ------------------- | -------- |
| `results.tex` | 42   | `94.2\%` | Main accuracy claim | CRITICAL |
| `method.tex`  | 18   | `128`    | Hidden layer size   | HIGH     |
| ...           |      |          |                     |          |

### 2e. Terminology Provenance

| Manuscript Term | Code Identifier                       | Status       | Location (manuscript) | Location (code)                    |
| --------------- | ------------------------------------- | ------------ | --------------------- | ---------------------------------- |
| "Greedy Search" | `GreedySearch`                        | CODE-DEFINED | §3.2                  | `src/search.py:class GreedySearch` |
| "Adaptive Mode" | —                                     | UNMAPPED     | §4.1                  | Not found                          |
| "Feature Set A" | `feature_group_a`                     | MAPPED       | Table 2               | `config.toml:feature_groups.a`     |
| "Deep Analysis" | `deep_analysis` / `detailed_analysis` | INCONSISTENT | §3.4                  | `src/analyze.py` uses both         |
| ...             |                                       |              |                       |                                    |

### 2f. Ordering Provenance

| Location          | Items    | Ordering Criterion  | Status       | Code Source                                 |
| ----------------- | -------- | ------------------- | ------------ | ------------------------------------------- |
| Table 1, rows     | Methods  | Descending accuracy | CODE-ORDERED | `scripts/make_table1.py:sort_values('acc')` |
| §4.2, enumeration | Features | —                   | MANUAL-ORDER | No ordering logic found                     |
| Table 3, columns  | Metrics  | —                   | MANUAL-ORDER | Columns hardcoded in script                 |
| ...               |          |                     |              |                                             |

---

## 3. Infrastructure Assessment

### 3a. Pipeline

**Entry point:** [Path to Makefile/snakemake/etc., or "MISSING"]

**Pipeline coverage:**

```
[Raw Data] → [Processing] → [Analysis] → [Results] → [Artifacts] → [PDF]
    ✓            ✓              ✓            ✓           ✗            ✗
```

**Steps covered:** [X / Y]

**Missing steps:**

- [Step description — what is not automated]
- [Step description — what is not automated]

**Pipeline issues:**

- [Issue — e.g., "Step 3 requires manual intermediate file placement"]
- [Issue — e.g., "No error handling — pipeline silently continues on failure"]

### 3b. Config Separation

**Config files found:**

| File          | Format | Keys | Issues                             |
| ------------- | ------ | ---- | ---------------------------------- |
| `config.toml` | TOML   | 23   | —                                  |
| `params.yaml` | YAML   | 8    | Duplicates 3 keys from config.toml |
| ...           |        |      |                                    |

**Hardcoded values found in scripts:**

| Script        | Line | Value      | Should Be                            |
| ------------- | ---- | ---------- | ------------------------------------ |
| `train.py`    | 42   | `lr=0.001` | `config.toml:training.learning_rate` |
| `evaluate.py` | 18   | `"gpt-4"`  | `config.toml:model.name`             |
| ...           |      |            |                                      |

### 3c. Version Pinning

| Artifact            | Status                             | Location            |
| ------------------- | ---------------------------------- | ------------------- |
| Python dependencies | [Pinned / Unpinned / Missing]      | `requirements.txt`  |
| Python version      | [Specified / Missing]              | `.python-version`   |
| Data versions       | [Tracked / Untracked]              | `dvc.lock`          |
| Container           | [Exists / Missing]                 | `Dockerfile`        |
| Random seeds        | [Documented / Scattered / Missing] | `config.toml:seeds` |

### 3d. Stale Outputs

| Output File             | Generating Script      | Output Modified | Script Modified | Delta | Status  |
| ----------------------- | ---------------------- | --------------- | --------------- | ----- | ------- |
| `results/main.csv`      | `scripts/run_eval.py`  | 2024-01-10      | 2024-01-15      | -5d   | STALE   |
| `figures/plot1.pdf`     | `scripts/plot_main.py` | 2024-01-12      | 2024-01-12      | 0d    | CURRENT |
| `generated/metrics.tex` | `scripts/export.py`    | 2024-01-08      | 2024-01-14      | -6d   | STALE   |
| ...                     |                        |                 |                 |       |         |

**Orphaned outputs** (no generating script):

- [File path — no script writes to this location]

**Unrun scripts** (no output found):

- [Script path — output file missing or not detectable]

---

## 4. Defect Registry

All provenance failures, sorted by severity.

### CRITICAL

1. **[Defect ID]** — [Checklist §X.Y]
   - **Artifact:** [What is untraced]
   - **Location:** [Manuscript file:line]
   - **Issue:** [Specific provenance failure]
   - **Remediation:** [Concrete fix]
   - **Effort:** [Low | Medium | High]

### HIGH

1. **[Defect ID]** — [Checklist §X.Y]
   - **Artifact:** [What is untraced]
   - **Location:** [Manuscript file:line]
   - **Issue:** [Specific provenance failure]
   - **Remediation:** [Concrete fix]
   - **Effort:** [Low | Medium | High]

### MEDIUM

1. **[Defect ID]** — [Checklist §X.Y]
   - **Artifact:** [What is untraced]
   - **Location:** [Manuscript file:line and/or code file:line]
   - **Issue:** [Specific provenance failure]
   - **Remediation:** [Concrete fix]
   - **Effort:** [Low | Medium | High]

### LOW

1. **[Defect ID]** — [Checklist §X.Y]
   - **Artifact:** [What is untraced]
   - **Location:** [Manuscript file:line]
   - **Issue:** [Specific provenance failure]
   - **Remediation:** [Optional fix]
   - **Effort:** [Low | Medium | High]

---

## 5. Remediation Queue

Issues ranked by (severity × inverse effort). Fix high-severity, low-effort
items first.

### Quick Wins (HIGH severity, LOW effort)

1. **[Issue]** — [Checklist §X] — [Location]
   - **Action:** [Specific step]
   - **Estimated effort:** < 1 hour

### Major Fixes (HIGH/CRITICAL severity, MEDIUM-HIGH effort)

1. **[Issue]** — [Checklist §X] — [Location]
   - **Action:** [Specific step]
   - **Estimated effort:** [Time range]

### Maintenance Items (MEDIUM severity)

1. **[Issue]** — [Checklist §X] — [Location]
   - **Action:** [Specific step]

### Polish (LOW severity)

1. **[Issue]** — [Checklist §X] — [Location]
   - **Action:** [Specific step]

---

## 6. Checklist Status

### §1. Value Provenance — Inline Numbers

- [✓] Abstract metrics — all traced to `scripts/evaluate.py`
- [✗] Headline results — **FAIL** — 2 values in §4.3 untraced
- [✓] Methodology parameters — all in `config.toml`
- [✗] Baseline comparisons — **FAIL** — baseline numbers manually entered
- [✓] Statistical measures
- [✓] Dataset statistics
- [✓] Computational cost
- [✓] Illustrative values

### §2. Table Provenance

- [✗] Results tables — **FAIL** — Table 3 manually constructed
- [✓] Cell value matching
- [✗] Row ordering — **FAIL** — Table 2 rows manually ordered
- [✓] Column ordering
- [✓] Header labels
- [✗] Formatting rules — **FAIL** — Bold applied manually in Table 1
- [✓] Ablation tables
- [N/A] Supplementary tables
- [✓] Table notes

### §3. Figure Provenance

- [✓] Main result figures
- [✗] Script-file traceability — **FAIL** — Fig 4 has no generation script
- [✓] Deterministic generation
- [✓] Data source traceability
- [✗] No post-editing — **FAIL** — Fig 3 edited in Illustrator
- [✓] Caption-data consistency
- [✓] Axis ranges
- [✓] Color/style consistency
- [N/A] Schematic figures
- [✓] Figure format

### §4. LaTeX Macro Audit

- [✗] No magic numbers — **FAIL** — 3 macros with hardcoded values in main.tex
- [✓] Generated macro files
- [✗] Macro-value consistency — **FAIL** — generated/metrics.tex is stale
- [✗] Complete macro coverage — **FAIL** — 5 bare numbers in results.tex
- [✓] Macro naming convention
- [✓] Macro organization
- [✓] No unused macros
- [✓] Formatting macros
- [✗] Bare number detection — **FAIL** — 8 bare numbers found in results/methodology
- [✗] Macro manifest generation — **PENDING** — run after fixing above

### §5. Terminology Provenance

- [✓] Mode/variant names
- [✗] Consistent naming — **FAIL** — "Deep Analysis" vs `detailed_analysis`
- [✓] Complete coverage
- [✗] Display-name mapping — **FAIL** — No explicit mapping file
- [✓] Category consistency
- [✓] Acronym-code alignment
- [✓] Deprecated terms

### §6. Ordering Provenance

- [✓] Results table row order
- [✓] Method comparison order
- [✗] Feature listing order — **FAIL** — §4.2 list order is manual
- [✓] Enumeration consistency
- [✓] Table column order
- [✓] Discussion order

### §7. Pipeline Completeness

- [✗] Single entry point — **FAIL** — Makefile missing steps 4-5
- [✓] Data → results
- [✓] Results → artifacts
- [✗] Artifacts → PDF — **FAIL** — LaTeX compilation not in pipeline
- [✗] Dependency tracking — **FAIL** — Makefile uses `.PHONY` for all targets
- [✓] Idempotency
- [✓] Incremental execution
- [✗] Error handling — **FAIL** — `|| true` on step 3
- [N/A] CI/CD integration
- [✓] Pipeline documentation

### §8. Code/Config Separation

- [✗] Hyperparameters in config — **FAIL** — `train.py:42` hardcodes lr
- [✗] Model names in config — **FAIL** — `evaluate.py:18` hardcodes model
- [✓] Thresholds in config
- [✓] File paths relative
- [✗] Single config entry point — **FAIL** — Split across 2 files with duplication
- [✓] Config format consistency
- [✓] No secrets in code
- [✓] Config documentation
- [✓] Default value handling

### §9. Stale Output Detection

- [✗] Script-output freshness — **FAIL** — 2 outputs stale
- [✓] Data-output freshness
- [✓] Orphaned outputs
- [✗] Unrun scripts — **FAIL** — `scripts/new_analysis.py` has no output
- [✗] Generated LaTeX freshness — **FAIL** — `generated/metrics.tex` stale
- [✗] Figure freshness — **FAIL** — `figures/plot2.pdf` stale
- [✓] Intermediate file freshness

### §10. Version Pinning

- [✓] Dependency lock files
- [✓] Language version specified
- [✗] Data versioning — **FAIL** — Raw data not tracked
- [✓] Manuscript-code co-versioning
- [N/A] Container definition
- [✓] OS/hardware dependencies
- [✗] Seed documentation — **FAIL** — Seeds scattered across scripts

### §11. Cross-Reference Integrity

- [✓] Script references in manuscript
- [✗] Appendix code listings — **FAIL** — Listing 1 differs from current source
- [✓] Repository URL validity
- [✓] README accuracy
- [N/A] Line number references

### §12. Manuscript-Review Integration

- [✗] §6 feedback — UNTRACED parameters flagged
- [✗] §7 feedback — UNTRACED results flagged
- [✗] §12 feedback — MANUAL figures flagged
- [✓] §14 feedback — No terminology issues
- [✓] §17 feedback — Code availability present

---

## Appendix: Legend

- **✓** — Provenance verified
- **✗** — Provenance failure (with location and remediation)
- **N/A** — Not applicable

**Provenance Status Codes:**

| Code          | Meaning                                                       |
| ------------- | ------------------------------------------------------------- |
| TRACED        | Full chain: manuscript value → script output → script → input |
| MACRO-TRACED  | Value in a LaTeX macro generated by a script                  |
| CONFIG-TRACED | Value from a config file read by scripts                      |
| UNTRACED      | No provenance chain found                                     |
| STALE         | Chain exists but output older than script                     |
| GENERATED     | Table/figure fully produced by script                         |
| PARTIAL       | Some elements generated, some manual                          |
| MANUAL        | No generation script                                          |
| CODE-DEFINED  | Term matches code identifier                                  |
| MAPPED        | Explicit code→display mapping exists                          |
| UNMAPPED      | Term in manuscript, not in code                               |
| INCONSISTENT  | Term in both but differs                                      |
| CODE-ORDERED  | Ordering matches code output                                  |
| MANUAL-ORDER  | Ordering set manually                                         |
| POST-EDITED   | Generated then manually modified                              |

**Severity Levels:**

- **CRITICAL** — Core result unverifiable. Paper's claims lack computational grounding.
- **HIGH** — Reproducibility gap. Artifact cannot be regenerated from code.
- **MEDIUM** — Consistency/maintenance risk.
- **LOW** — Minor provenance gap, cosmetic.

**Effort Estimates:**

- **Low** — < 1 hour (add macro, update config key, re-run script)
- **Medium** — 1-4 hours (write generation script, refactor config)
- **High** — > 4 hours (build pipeline, restructure codebase)
