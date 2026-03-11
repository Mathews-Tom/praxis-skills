# Transformation Rules

Structural rewrite strategies (Phase 2) and entropy techniques (Phase 4).

---

## Structural Transformations

### Paragraph Restructuring

AI text tends toward uniform paragraph length (3-5 sentences each, roughly equal). Human writing varies.

Techniques:
- Split a long paragraph into a short declarative statement + a longer elaboration paragraph
- Merge two related short paragraphs into one cohesive block
- Allow single-sentence paragraphs at impact positions (conclusions, transitions, revelations)
- Break the "topic sentence + support + conclusion" template — not every paragraph needs all three

### Sentence Merging and Splitting

AI produces uniform sentence length. Target: visible variance.

- Merge two short related sentences: "The system is fast. It handles 10K requests." -> "The system handles 10K requests per second."
- Split compound sentences where the conjunction adds no meaning: "The team reviewed the code and they found three bugs" -> "The team reviewed the code. Three bugs."
- Introduce subordinate clauses where they reduce total word count: "X happened. This was because of Y." -> "X happened because of Y."

### List-to-Narrative Conversion

Not all lists should become narrative. Convert when:
- The list has 3 items and reads as Rule of Three (Pattern 10)
- The list items are complete sentences disguised as bullets
- The list has inline bold headers (Pattern 15)

Keep lists when:
- Items are genuinely parallel (feature comparisons, step-by-step instructions)
- Items are short noun phrases or values
- The context is technical documentation

### Clause Reordering

AI follows predictable clause order: setup -> detail -> significance. Human writing varies:

- Lead with the specific detail, then provide context: "Three bugs in the auth module — the team found them during Friday's review."
- Start with a consequence, then explain: "The deployment failed. The config file was missing a required field."
- Bury the attribution mid-sentence: "The river supports, according to a 2019 CAS survey, several endemic fish species."

---

## Entropy and Variation Techniques

These techniques target the statistical regularity signals documented in `statistical-signals.md`. The goal: produce text that falls within human-typical distributional ranges.

### Sentence Length Variance (Signal 3)

Target distribution across any 5-sentence window:
- At least one sentence under 8 words
- At least one sentence over 20 words
- No three consecutive sentences within 5 words of each other in length

Human-typical SD: 7-15 words. This is a guideline, not a formula. The goal is visible variance, not mechanical alternation.

### Clause Density Variation (Signal 9)

Human writing mixes simple, compound, and complex sentences. Human-typical range: 1.2-2.5 clauses per sentence, varied.

- Do not write 5 consecutive simple sentences (all one clause)
- Do not write 5 consecutive complex sentences (all 2-3 clauses)
- Mix: "The deployment failed." (simple) + "The config file was missing a required field, which the CI pipeline should have caught but didn't because the validation step was skipped." (complex)
- Subordinate clauses add density naturally: "because", "although", "which", "where", "when"

### Information Density Variation (Signal 7)

AI distributes information evenly — every sentence carries roughly the same load. Human writing varies:

- **Heavy sentences**: pack 3-4 facts or details: "The survey covered 450 participants across 12 departments, ran from March to May, and used both Likert-scale and open-ended questions."
- **Light sentences**: carry one reaction, pivot, or summary: "That's a lot of data." or "The results were mixed."
- Alternate heavy and light within paragraphs. Do not let every sentence carry the same information weight.

### Syntactic Variation

Rotate sentence openings across a paragraph. Avoid:
- Three sentences starting with "The [noun]..."
- Two consecutive sentences starting with the same word
- Subject-verb-object in every sentence

Introduce:
- Occasional inverted structures: "Gone is the assumption that..."
- Adverbial openers: "By Friday, the team had..."
- Participial openers (sparingly — avoid creating Pattern 3): "Having reviewed the data, the team concluded..."
- Prepositional openers: "In the auth module, three bugs surfaced."

### Lexical Diversity (Signal 5)

Target type-token ratio: 0.45-0.65. Replace repeated words through restructuring, not synonym cycling (Pattern 11).

- If "system" appears 5 times in a paragraph, restructure so 2-3 instances become pronouns or are eliminated through sentence merging
- Domain-specific terms should NOT be varied — "API" stays "API", not "interface" then "endpoint" then "service boundary"
- Common verbs (is, has, does, makes, gets) are invisible to readers — repeating them is fine

### Phrase Template Breaking (Signal 6)

AI text relies on stock collocations — high-frequency bigrams and trigrams that detectors measure via n-gram rarity scores.

Common templates to break:
- "plays a role in" -> name the specific action
- "a wide range of" -> specify the range or delete
- "in terms of" -> delete, restructure the sentence
- "it is worth noting that" -> state the fact directly
- "serves as a" -> use "is"
- "has the potential to" -> "can" or "might"
- "in the context of" -> "in" or "for" or delete

The goal is not to avoid all common phrases — just to prevent them from dominating. A few stock phrases in 500 words is normal. A dozen is a signal.

### Inter-Sentence Cohesion Variation (Signal 10)

AI text produces tightly chained sentences where each directly continues the previous. Human-typical cosine similarity between adjacent sentences: 0.3-0.6.

Introduce:
- **Topic micro-shifts**: "The API handled authentication well. On the deployment side, things were rougher." (shift from feature to infrastructure)
- **Brief asides**: "The team shipped on Friday — not the best day for a deploy, but deadlines."
- **Perspective pivots**: "The metrics looked good. Whether they'll hold under real traffic is a different question."
- **Contextual expansions**: after a specific claim, briefly widen scope before returning

Target: 2-3 small topic shifts or asides per 500 words.

### Function Word Personalization (Signal 8)

AI uses connectors and prepositions in standardized distributions. Human authors show consistent but personalized patterns.

Within a single piece:
- Pick preferred connectors and use them consistently: if you use "but" early, don't switch to "however" without reason
- Vary connector type: "but", "still", "and yet", "though" — not the same one every time
- Allow some sentences to connect with no explicit marker at all
- Avoid defaulting to the most formal option ("furthermore", "moreover", "additionally") — these are the strongest transition-frequency signals

### Controlled Imperfection (Signal 2 — Burstiness)

Human writing alternates between predictable and unexpected. This burstiness is one of the strongest statistical differentiators.

- Occasional fragments: "Not ideal." or "Three bugs. All in auth."
- Parenthetical asides: "The team (all six of them) reviewed the code."
- Self-corrections: "The system is fast — well, fast enough."
- Concessive turns: "Granted, the sample size is small."
- Unexpected specificity: "The meeting ran 47 minutes" (not "about an hour")

Use sparingly. One fragment per 500 words maximum. These are seasoning, not structure.

### Transition Reduction (Signal 11)

AI overuses transitions: "Additionally", "Furthermore", "Moreover", "In conclusion", "However". Human-typical range: 3-8 formal transitions per 1,000 words.

Human writing uses:
- No transition (just start the next thought)
- Short conjunctions: "But", "And", "So", "Still"
- Paragraph breaks as implicit transitions
- Semantic connection (the ideas themselves connect, no signpost needed)

Target: remove 60-80% of formal transitional phrases. Replace half with nothing. Replace the rest with short conjunctions or restructured sentences.

### Structural Symmetry Breaking (Signal 12)

AI produces balanced, mirror-like structures. Human writing is irregular.

- Vary paragraph lengths visibly: some 1-2 sentences, some 4-6
- Do not alternate short-long-short-long in a predictable pattern
- Allow one paragraph to be noticeably longer than its neighbors
- Break any A-B-A-B or A-B-C-A-B-C patterns in list or argument structures

---

## Preservation Checklist

Before delivering the rewrite, verify:

- [ ] Every factual claim in the original is present in the rewrite
- [ ] All numbers, dates, and proper nouns are unchanged
- [ ] Citations and references are intact (format may change, content must not)
- [ ] Code blocks, tables, and structured data are untouched
- [ ] The argument flows in the same logical order (unless reordering was explicitly requested)
- [ ] Technical terminology is preserved — no simplification of domain terms
- [ ] URLs, file paths, and identifiers are exact
