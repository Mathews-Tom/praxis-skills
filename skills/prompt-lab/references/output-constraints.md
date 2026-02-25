# Output Constraints

Techniques for constraining LLM output format, enforcing structure, and ensuring
parseable responses.

---

## Prompt-Level Constraints

### Length Constraints

```
Respond in exactly 3 bullet points.
Maximum 100 words.
One sentence only.
Between 2 and 5 paragraphs.
```

### Format Constraints

```
Respond in valid JSON matching this schema:
{"category": "string", "confidence": "number 0-1", "reasoning": "string"}

Respond as a markdown table with columns: Feature, Pros, Cons

Respond as a numbered list. Each item must start with an action verb.
```

### Content Constraints

```
ONLY use information from the provided context. Do not add external knowledge.
If the answer is not in the context, respond with "Not found in context."
Do not include opinions or recommendations. State facts only.
Do not use technical jargon. Write for a non-technical audience.
```

---

## API-Level Constraints

### JSON Mode (OpenAI)

```python
response = client.chat.completions.create(
    model="gpt-4",
    messages=[...],
    response_format={"type": "json_object"},
)
```

Guarantees valid JSON output. Still need to specify the schema in the prompt.

### Tool Use / Function Calling (Claude, OpenAI)

```python
# Define the expected output schema as a tool
tools = [{
    "name": "classify_ticket",
    "description": "Classify a support ticket",
    "input_schema": {
        "type": "object",
        "properties": {
            "category": {"type": "string", "enum": ["billing", "technical", "general"]},
            "priority": {"type": "string", "enum": ["low", "medium", "high"]},
            "summary": {"type": "string"},
        },
        "required": ["category", "priority", "summary"],
    },
}]
```

Forces the model to respond with a structured object matching the schema.

### Structured Output (OpenAI)

```python
from pydantic import BaseModel

class Classification(BaseModel):
    category: str
    confidence: float
    reasoning: str

response = client.beta.chat.completions.parse(
    model="gpt-4o",
    messages=[...],
    response_format=Classification,
)
```

---

## Constraint Placement

### Position Matters

Models have recency bias — instructions at the end of the prompt are followed more
reliably than those at the beginning.

```
{Context / input data}

{Main instruction}

{Format constraint — place last for best compliance}
```

### Repetition Reinforces

For critical constraints, state them twice:

```
Important: Respond ONLY in valid JSON.

{Task instruction}

{Input}

Remember: Your response must be valid JSON. No text outside the JSON object.
```

---

## Common Constraint Failures

| Constraint | Failure Mode | Fix |
|-----------|-------------|-----|
| "Respond in JSON" | Model wraps JSON in markdown code blocks | "Respond with raw JSON only. No markdown, no code blocks." |
| "Maximum 3 sentences" | Model writes 3 long sentences | "Maximum 3 sentences, each under 30 words" |
| "Only use provided context" | Model adds common knowledge | "If you add ANY information not in the context, mark it as [inferred]" |
| "No opinions" | Model hedges with "some might say" | "State each point as a factual observation" |
| "Use this template" | Model modifies the template structure | Provide the template with clear markers: `{FILL THIS}` |

---

## Validation After Generation

Even with constraints, validate the output programmatically:

```python
import json

def validate_output(text: str, expected_keys: list[str]) -> bool:
    """Validate that output is valid JSON with expected keys."""
    try:
        data = json.loads(text)
    except json.JSONDecodeError:
        return False

    return all(key in data for key in expected_keys)
```

### Retry Strategy

If validation fails:
1. Parse the error
2. Include the error in a follow-up prompt
3. Ask the model to fix its output
4. Maximum 2 retries before failing

```python
for attempt in range(3):
    response = generate(prompt)
    if validate_output(response):
        return response
    prompt = f"Your previous response was invalid: {error}. Please fix it.\n\n{original_prompt}"
raise ValueError("Failed to generate valid output after 3 attempts")
```
