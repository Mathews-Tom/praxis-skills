# Domain Style Profiles

Voice calibration rules per writing domain. Apply the matching profile during Phase 3 (Vocabulary and Style Pass).

---

## Academic

**Register:** Formal, measured, evidence-based.
**Audience:** Researchers, reviewers, graduate students.

Rules:
- Maintain hedging where epistemically appropriate ("suggests" vs. "proves") — but remove *excessive* hedging (Pattern 23)
- Preserve citation structure and in-text references exactly
- Passive voice is acceptable where convention demands it (methods sections)
- Do not inject personality or first-person unless the original uses it
- Avoid contractions
- Replace AI-inflated significance claims with measured statements: "This study examines..." not "This groundbreaking study delves into..."
- Technical jargon is expected — do not simplify domain-specific terms
- Sentence length: longer is acceptable, but vary within paragraphs

**Preserve:** Citation formats, section headings (Introduction/Methods/Results/Discussion), figure/table references, statistical notation.

**Target tells to fix:** Significance inflation (Pattern 1), AI vocabulary (Pattern 7), formulaic challenges/future-work sections (Pattern 6), vague attributions (Pattern 5).

---

## Technical

**Register:** Precise, direct, information-dense.
**Audience:** Engineers, developers, technical practitioners.

Rules:
- Clarity over style — if a sentence is clear but boring, leave it
- Code blocks, terminal output, config snippets pass through unchanged
- Numbered steps and bullet lists are natural in technical writing — do not convert all lists to prose
- Contractions are fine
- First person ("I configured...", "we deployed...") is natural in technical blogs and docs
- Replace promotional language with specifics: "blazing fast" -> "handles 10K requests/second"
- Remove all chatbot artifacts aggressively (Pattern 19)

**Preserve:** Code blocks, command-line examples, version numbers, API endpoints, configuration values, error messages.

**Target tells to fix:** Promotional language (Pattern 4), copula avoidance (Pattern 8), AI vocabulary (Pattern 7), inline-header lists (Pattern 15).

---

## Blog

**Register:** Conversational, opinionated, personal.
**Audience:** General readers, tech-curious non-specialists.

Rules:
- First person is expected and natural
- Contractions, fragments, rhetorical questions all allowed
- Opinions and reactions are good — "I genuinely don't know how to feel about this"
- Humor and asides are human signals — preserve or introduce where natural
- Vary rhythm aggressively: short punchy sentences mixed with longer explanatory ones
- Analogies should be concrete and from everyday life
- Remove ALL promotional language — blog readers detect it instantly
- Remove significance inflation — readers came for the author's perspective, not Wikipedia-style importance claims

**Preserve:** Personal anecdotes, named sources, specific experiences, the author's apparent opinions.

**Target tells to fix:** All HIGH priority patterns, plus structural patterns (Rule of Three, Negative Parallelisms).

---

## Social

**Register:** Casual, compressed, direct.
**Audience:** Reddit, Twitter/X, forum users.

Rules:
- Extremely short paragraphs (1-3 sentences)
- Fragments and incomplete sentences are natural
- Slang and informal language acceptable
- No hedging — social media writing is assertive
- No significance inflation — users will mock it
- Remove ALL chatbot artifacts — these are the most obvious tell on social platforms
- Contractions mandatory — "do not" reads as AI on Reddit
- Lowercase acceptable for casual tone
- Swearing is fine if the original contains it

**Preserve:** Links, usernames/handles, quoted text, platform-specific formatting.

**Target tells to fix:** Communication artifacts (Pattern 19-21), hedging (Pattern 23), filler (Pattern 22), promotional language (Pattern 4).

---

## Professional

**Register:** Clear, neutral, competent. Business correspondence tone.
**Audience:** Colleagues, clients, stakeholders.

Rules:
- Polite but not sycophantic — remove "I hope this finds you well" only if it reads as filler
- Contractions acceptable in internal communication, avoid in external/formal
- No promotional language unless the context is genuinely marketing
- Action items and next steps should be clear and direct
- Remove AI vocabulary but preserve business terminology where standard
- Moderate formality — neither stiff nor casual
- First person is natural ("I'll follow up on...", "We reviewed...")

**Preserve:** Names, dates, action items, deadlines, project references, organizational terminology.

**Target tells to fix:** Sycophantic tone (Pattern 21), filler phrases (Pattern 22), AI vocabulary (Pattern 7), generic conclusions (Pattern 24).

---

## Marketing

**Register:** Persuasive but authentic. Benefits-focused.
**Audience:** Potential customers, users, decision-makers.

Rules:
- Some promotional language is expected — but it must be specific, not generic
- "Blazing fast" is AI slop; "loads in 0.3 seconds" is marketing with substance
- Remove vague superlatives, keep specific claims
- Social proof should cite real numbers or real customers, not "industry experts agree"
- CTA (call to action) is expected — do not remove it, but make it specific
- Bullet lists and feature comparisons are natural format for marketing
- Remove AI tells that undermine trust: chatbot artifacts, hedging, generic conclusions

**Preserve:** Product names, feature lists, pricing, CTAs, testimonials (if sourced), comparison data.

**Target tells to fix:** Vague attributions (Pattern 5), generic positive conclusions (Pattern 24), AI vocabulary (Pattern 7), significance inflation (Pattern 1).
