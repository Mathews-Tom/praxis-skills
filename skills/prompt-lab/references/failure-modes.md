# Failure Modes

Common prompt failure taxonomy with detection strategies and mitigations.

---

## Failure Taxonomy

### 1. Instruction Misinterpretation

**Symptom:** Model does something different from what was intended.

| Cause | Example | Mitigation |
|-------|---------|------------|
| Ambiguous instruction | "Summarize this" — model writes 3 sentences vs 3 paragraphs | Specify length: "Summarize in 2-3 sentences" |
| Overloaded instruction | "Analyze and fix this code" — model does both poorly | Split into two prompts |
| Implicit assumption | "Fix the bug" without specifying which bug | Be explicit about the target |

### 2. Format Violation

**Symptom:** Output is correct but in the wrong format.

| Cause | Example | Mitigation |
|-------|---------|------------|
| No format specified | Asked for JSON, got prose | Specify format explicitly with example |
| Format specified but buried | Format instruction in the middle of a long prompt | Put format instruction at the end (recency bias) |
| Conflicting format signals | Examples in one format, instruction asks for another | Ensure examples match requested format |

### 3. Hallucination

**Symptom:** Model states false information as fact.

| Type | Example | Mitigation |
|------|---------|------------|
| Fabricated facts | Invents statistics, citations | Add "Only state facts supported by the provided context" |
| Fabricated reasoning | Plausible-sounding but incorrect logic | Use CoT to make reasoning visible and checkable |
| Confident wrong answers | States incorrect answer with high confidence | Add "If unsure, say so explicitly" |

### 4. Refusal / Over-Caution

**Symptom:** Model refuses to answer or adds excessive caveats.

| Cause | Mitigation |
|-------|------------|
| Safety filter triggered | Reframe the task to be clearly benign |
| Task seems risky to model | Provide context explaining the legitimate use |
| Model uncertain | Explicitly allow uncertainty: "It's OK to be approximate" |

### 5. Repetition / Verbosity

**Symptom:** Model repeats itself or generates unnecessary content.

| Cause | Mitigation |
|-------|------------|
| No length constraint | Add: "Maximum 200 words" or "Be concise" |
| Instruction encourages elaboration | Remove "explain in detail" if not needed |
| Few-shot examples are verbose | Use concise examples |

### 6. Anchoring to Examples

**Symptom:** Model copies patterns from examples too literally.

| Cause | Mitigation |
|-------|------------|
| Examples too similar | Diversify examples across different cases |
| Examples contain irrelevant patterns | Model copies format details, not the underlying logic |
| Too many examples | Reduce to 2-3 diverse examples |

### 7. Ignoring Context

**Symptom:** Model doesn't use provided context/information.

| Cause | Mitigation |
|-------|------------|
| Context too long | Highlight relevant sections: "Pay special attention to..." |
| Context placement | Move context closer to the question (recency effect) |
| Instruction doesn't reference context | Explicitly: "Using ONLY the information above, answer..." |

### 8. Sycophancy / Agreement Bias

**Symptom:** Model agrees with the user's stated opinion instead of giving an honest answer.

| Cause | Mitigation |
|-------|------------|
| User states opinion before asking | Ask the question before revealing your view |
| Prompt frames one option favorably | Present options neutrally |
| "Do you agree?" framing | Ask "Evaluate the pros and cons" instead |

---

## Detection Strategies

| Failure Mode | Detection Method |
|-------------|-----------------|
| Misinterpretation | Compare output structure to expected structure |
| Format violation | Parse output with expected format parser |
| Hallucination | Cross-reference claims against source material |
| Refusal | Check for "I cannot", "I'm sorry", "As an AI" |
| Verbosity | Word count comparison against target length |
| Example anchoring | Run without examples, compare output diversity |
| Context ignoring | Check if key facts from context appear in output |
| Sycophancy | Ask the same question with opposite framing |

---

## Failure Mode by Task Type

| Task Type | Most Common Failures |
|-----------|---------------------|
| Classification | Misinterpretation, anchoring to examples |
| Extraction | Incomplete extraction, hallucinated fields |
| Summarization | Verbosity, missing key points |
| Analysis | Hallucination, sycophancy |
| Code generation | Format violation, subtle logic errors |
| Creative writing | Verbosity, generic output |
| RAG / grounded QA | Hallucination, context ignoring |
