# Prompt Patterns

Catalog of prompt structures organized by strategy, with templates and usage guidance.

---

## Zero-Shot

No examples. Direct instruction only.

```
{Role/persona statement — optional}

{Task instruction}

{Input format specification}

{Output format specification}

{Constraints}
```

**When to use:** Simple tasks, capable models (GPT-4, Claude), well-defined output format.

**Risk:** Model may interpret the task differently than intended without examples.

---

## Few-Shot

Provide examples of input → output pairs before the actual task.

```
{Task instruction}

Example 1:
Input: {example input}
Output: {example output}

Example 2:
Input: {example input}
Output: {example output}

Now do the same for:
Input: {actual input}
Output:
```

**When to use:** Pattern-following tasks, classification, formatting, extraction.

**Guidelines:**
- 2-5 examples is typical. More is not always better.
- Examples should cover the range of expected inputs (not all similar).
- Include at least one edge case example.
- Keep examples consistent in format — the model mirrors what it sees.

---

## Chain-of-Thought (CoT)

Ask the model to reason step by step before giving the final answer.

```
{Task instruction}

Think through this step by step:
1. First, consider...
2. Then, analyze...
3. Finally, conclude...

{Input}
```

**When to use:** Multi-step reasoning, math, logical deduction, complex analysis.

**Variants:**
- **Explicit CoT:** "Think step by step" in the instruction
- **Few-shot CoT:** Examples include the reasoning steps
- **Zero-shot CoT:** Just append "Let's think step by step" (surprisingly effective)

---

## Persona/Role

Frame the model as an expert in a specific domain.

```
You are a {role} with expertise in {domain}. You have {years} of experience
with {specific skills}.

Your task is to {instruction}.

{Input}
```

**When to use:** Domain-specific tasks where expertise framing improves output quality.

**Caution:** Personas should be specific and relevant, not generic.
"You are a senior PostgreSQL DBA" > "You are a helpful assistant."

---

## Structured Output

Specify the exact output format the model must follow.

```
{Task instruction}

Respond in the following JSON format:
```json
{
  "field1": "description of what goes here",
  "field2": ["array", "of", "items"],
  "field3": {
    "nested": "object"
  }
}
```

{Input}
```

**When to use:** When output must be machine-parseable (JSON, CSV, YAML).

**Enhancement:** Use JSON mode / structured output API features when available
(OpenAI `response_format`, Anthropic tool use).

---

## Decomposition

Break a complex task into explicit subtasks within the prompt.

```
I need you to complete the following task in steps:

Step 1: {subtask 1}
Step 2: Using the result of Step 1, {subtask 2}
Step 3: Based on Steps 1 and 2, {subtask 3}

Present each step's result before moving to the next.

{Input}
```

**When to use:** Complex tasks that benefit from intermediate checkpoints.

---

## Constraint-Based

Define what the output must and must not contain.

```
{Task instruction}

Rules:
- MUST: {requirement 1}
- MUST: {requirement 2}
- MUST NOT: {prohibition 1}
- MUST NOT: {prohibition 2}
- IF {condition} THEN {behavior}

{Input}
```

**When to use:** Tasks with strict requirements or common failure modes to prevent.

---

## Comparison / Selection Pattern

```
Compare the following options and recommend the best one:

Option A: {description}
Option B: {description}

Evaluation criteria (in order of importance):
1. {criterion 1}
2. {criterion 2}
3. {criterion 3}

For each option, evaluate against each criterion. Then provide your recommendation
with justification.
```

---

## Pattern Selection Guide

| Task Type | Recommended Pattern | Fallback |
|-----------|-------------------|----------|
| Classification | Few-shot | Zero-shot with examples in description |
| Extraction | Few-shot + Structured output | Zero-shot with JSON mode |
| Analysis | Chain-of-thought | Decomposition |
| Generation (creative) | Persona + Constraints | Zero-shot with tone guidance |
| Generation (technical) | Persona + Structured output | Few-shot + Template |
| Summarization | Zero-shot with length constraint | Few-shot with length examples |
| Translation/formatting | Few-shot | Zero-shot with format specification |
| Decision/recommendation | Comparison pattern | Chain-of-thought |
