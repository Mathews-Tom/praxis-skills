# Statistical Signals of AI-Generated Text

12 distributional signals used by AI-text detection systems. These measure structural regularity, predictability, and distributional patterns that differ between machine-generated and human-written text.

Claude cannot compute most of these metrics numerically. Instead, use the **target behaviors** column during Phase 4 to produce text that falls within human-typical ranges.

---

## Signal Reference Table

| # | Signal | What detectors measure | Human-typical range | AI-typical pattern | Target behavior during rewrite |
|---|--------|----------------------|--------------------|--------------------|-------------------------------|
| 1 | Perplexity | How predictable text is to a language model | Higher, variable | Lower, uniform | Use specific/concrete words over high-frequency generic ones. Prefer "the auth module crashed" over "the system encountered an error" |
| 2 | Burstiness | Variance in token predictability across a passage | High variance | Low variance | Alternate between predictable phrasings and unexpected expressions. Let some sentences be plain, others surprising |
| 3 | Sentence length variance | Standard deviation of words per sentence | SD 7-15 words | Narrow SD | Mix sentences from 3-8 words to 20-30 words within paragraphs. No three consecutive sentences within 5 words of each other |
| 4 | Token probability distribution | Distribution of word likelihood scores | Long tail of low-probability tokens | Clustered mid-to-high probability | Include specific nouns, unusual adjectives, domain jargon, and concrete details that a generic model would not predict |
| 5 | Type-token ratio | Unique words / total words | 0.45-0.65 | Often lower (repetitive) | Maintain vocabulary breadth through restructuring (pronouns, sentence merging), not synonym cycling |
| 6 | N-gram frequency | Distribution of common word sequences | More rare bigrams/trigrams | Heavy reliance on stock phrases | Break phrase templates: "plays a role in" -> name the action. "In terms of" -> delete. "It is worth noting" -> delete |
| 7 | Sentence entropy | Information density per sentence | Moderate to high, variable | Moderate but uniform | Vary density: some sentences carry 3-4 facts, others carry one reaction or pivot. Do not distribute information evenly |
| 8 | Function word distribution | Usage patterns of the/and/but/because/however | Personalized, consistent per author | Standardized, textbook-like | Develop preferences within a piece: favor "but" over "however", use "still" or "and yet" instead of always defaulting to the same connector |
| 9 | Clause density | Average clauses per sentence | 1.2-2.5, varied | More uniform | Mix simple sentences (one clause) with compound-complex (2-3 clauses). Do not write 10 consecutive simple sentences or 10 consecutive complex ones |
| 10 | Semantic similarity between sentences | Cosine similarity of adjacent sentence embeddings | 0.3-0.6 | Often higher (tightly related) | Allow topic micro-shifts: a brief aside, a contextual expansion, a perspective shift. Not every sentence must directly continue the previous one |
| 11 | Transition phrase frequency | Discourse markers per 1,000 words | 3-8 | Often higher | Remove 60-80% of formal transitions. Replace half with nothing, the rest with short conjunctions (but, so, still) or paragraph breaks |
| 12 | Structural symmetry | Uniformity of sentence/paragraph/clause patterns | High irregularity | Balanced, mirror-like | Break symmetry: unequal paragraph lengths, varied sentence openings, mixed clause structures. Avoid A-B-A-B patterns |

---

## Applying Signals by Phase

### Phase 1 (Detection): What to scan for

Assess the input text for these regularity indicators:

- **Sentence length uniformity**: Are most sentences within a 5-word range of each other? Flag if yes.
- **Clause density uniformity**: Does every sentence have the same structure (all simple, or all compound)? Flag if yes.
- **Transition overuse**: Count formal transitions (however, furthermore, additionally, moreover, in addition, therefore, consequently, nevertheless). Flag if above ~8 per 1,000 words.
- **Phrase template density**: Are stock collocations repeated? ("plays a role", "it is important to note", "in terms of", "serves as a", "a wide range of"). Flag clusters.
- **Structural symmetry**: Are paragraphs roughly equal length? Do sentences follow predictable patterns? Flag visible uniformity.
- **Inter-sentence tightness**: Does every sentence directly continue the previous with no shifts, asides, or expansions? Flag if the text reads as a single unbroken logical chain.

### Phase 4 (Entropy): What to target

Use the human-typical ranges as guidelines, not formulas:

**Sentence-level targets:**
- In any 5-sentence window: at least one under 8 words, at least one over 20 words
- No three consecutive sentences with the same clause structure
- At least one sentence per paragraph that shifts density (heavy detail -> light reaction, or vice versa)

**Paragraph-level targets:**
- Visible length variation across paragraphs (some 1-2 sentences, some 4-6)
- At least one paragraph break that is not preceded by a transition phrase

**Document-level targets:**
- 2-3 small topic micro-shifts or asides per 500 words (brief digressions that a thinking human would include)
- Function word preferences should be roughly consistent within the piece (if you use "but" early, don't switch to "however" later without reason)
- Formal transition count under 8 per 1,000 words

---

## Signals Claude Cannot Directly Compute

These require language model inference or embedding computation that is not available during skill execution:

| Signal | Why it's not computable | Proxy behavior |
|--------|------------------------|----------------|
| Perplexity (absolute score) | Requires running a reference LM on the output | Use specific, concrete, domain-appropriate vocabulary instead of generic high-frequency words |
| Token probability distribution | Requires token-level probability access | Include proper nouns, precise numbers, domain jargon — tokens a model would assign low probability |
| Semantic similarity (cosine) | Requires sentence embeddings | Introduce visible topic variation: asides, perspective shifts, contextual jumps |
| N-gram rarity scores | Requires corpus frequency data | Break stock phrases, use fresh constructions, avoid "plays a role in / wide range of / it is important" templates |

The proxy behaviors achieve the same *effect* on detector scores without requiring numerical computation.
