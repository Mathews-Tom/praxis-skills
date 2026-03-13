# AI Writing Detection Patterns

Source: [Wikipedia:Signs of AI writing](https://en.wikipedia.org/wiki/Wikipedia:Signs_of_AI_writing), maintained by WikiProject AI Cleanup. Last synced: 2025-01.

24 patterns organized by detection priority. Each pattern includes signal words, the problem it creates, and a before/after example.

---

## HIGH Priority — Content Inflation

### Pattern 1: Significance and Legacy Inflation

**Signal words:** stands/serves as, is a testament/reminder, vital/significant/crucial/pivotal/key role/moment, underscores/highlights importance, reflects broader, symbolizing ongoing/enduring/lasting, setting the stage, marking/shaping, represents/marks a shift, key turning point, evolving landscape, focal point, indelible mark, deeply rooted

**Problem:** Puffs up importance by claiming arbitrary aspects represent or contribute to broader topics.

Before:
> The Statistical Institute of Catalonia was officially established in 1989, marking a pivotal moment in the evolution of regional statistics in Spain.

After:
> The Statistical Institute of Catalonia was established in 1989 to collect and publish regional statistics independently from Spain's national statistics office.

### Pattern 2: Notability and Media Emphasis

**Signal words:** independent coverage, local/regional/national media outlets, written by a leading expert, active social media presence

**Problem:** Hits readers over the head with claims of notability without context.

Before:
> Her views have been cited in The New York Times, BBC, Financial Times, and The Hindu. She maintains an active social media presence with over 500,000 followers.

After:
> In a 2024 New York Times interview, she argued that AI regulation should focus on outcomes rather than methods.

### Pattern 3: Superficial -ing Analyses

**Signal words:** highlighting/underscoring/emphasizing..., ensuring..., reflecting/symbolizing..., contributing to..., cultivating/fostering..., encompassing..., showcasing...

**Problem:** Tacks present participle phrases onto sentences to add fake depth.

Before:
> The temple's color palette resonates with the region's natural beauty, symbolizing Texas bluebonnets, reflecting the community's deep connection to the land.

After:
> The temple uses blue, green, and gold colors. The architect said these were chosen to reference local bluebonnets and the Gulf coast.

### Pattern 4: Promotional Language

**Signal words:** boasts a, vibrant, rich (figurative), profound, enhancing its, showcasing, exemplifies, commitment to, natural beauty, nestled, in the heart of, groundbreaking (figurative), renowned, breathtaking, must-visit, stunning

**Problem:** Cannot maintain neutral tone, especially for cultural heritage topics.

Before:
> Nestled within the breathtaking region of Gonder, Alamata Raya Kobo stands as a vibrant town with a rich cultural heritage and stunning natural beauty.

After:
> Alamata Raya Kobo is a town in the Gonder region of Ethiopia, known for its weekly market and 18th-century church.

### Pattern 5: Vague Attributions

**Signal words:** Industry reports, Observers have cited, Experts argue, Some critics argue, several sources/publications

**Problem:** Attributes opinions to vague authorities without specific sources.

Before:
> Experts believe it plays a crucial role in the regional ecosystem.

After:
> The river supports several endemic fish species, according to a 2019 survey by the Chinese Academy of Sciences.

### Pattern 6: Formulaic Challenges Sections

**Signal words:** Despite its... faces several challenges..., Despite these challenges, Challenges and Legacy, Future Outlook

**Problem:** Formulaic "Challenges" sections that inflate and then dismiss problems.

Before:
> Despite its industrial prosperity, Korattur faces challenges typical of urban areas. Despite these challenges, Korattur continues to thrive.

After:
> Traffic congestion increased after 2015 when three new IT parks opened. The municipal corporation began a stormwater drainage project in 2022.

---

## HIGH Priority — Vocabulary

### Pattern 7: AI-Frequency Vocabulary

**Overused words:** Additionally, align with, crucial, delve, emphasizing, enduring, enhance, fostering, garner, highlight (verb), interplay, intricate/intricacies, key (adjective), landscape (abstract), pivotal, showcase, tapestry (abstract), testament, underscore (verb), valuable, vibrant

**Problem:** These words appear at statistically anomalous frequency in post-2023 text and often co-occur.

Before:
> Additionally, a distinctive feature is the incorporation of camel meat. An enduring testament to Italian colonial influence is the widespread adoption of pasta in the local culinary landscape.

After:
> Somali cuisine also includes camel meat, which is considered a delicacy. Pasta dishes, introduced during Italian colonization, remain common in the south.

### Pattern 8: Copula Avoidance

**Signal words:** serves as/stands as/marks/represents [a], boasts/features/offers [a]

**Problem:** Substitutes elaborate constructions for simple "is", "are", "has".

Before:
> Gallery 825 serves as LAAA's exhibition space. The gallery features four separate spaces and boasts over 3,000 square feet.

After:
> Gallery 825 is LAAA's exhibition space. The gallery has four rooms totaling 3,000 square feet.

### Pattern 22: Filler Phrases

Common substitutions:
- "In order to achieve this goal" -> "To achieve this"
- "Due to the fact that" -> "Because"
- "At this point in time" -> "Now"
- "In the event that" -> "If"
- "has the ability to" -> "can"
- "It is important to note that" -> (delete, state the fact directly)

### Pattern 23: Excessive Hedging

**Problem:** Over-qualifying every statement.

Before:
> It could potentially possibly be argued that the policy might have some effect on outcomes.

After:
> The policy may affect outcomes.

---

## MEDIUM Priority — Structure

### Pattern 9: Negative Parallelisms

**Problem:** "Not only...but..." and "It's not just about..., it's..." constructions are overused.

Before:
> It's not just about the beat; it's part of the aggression. It's not merely a song, it's a statement.

After:
> The heavy beat adds to the aggressive tone.

### Pattern 10: Rule of Three

**Problem:** Forces ideas into groups of three to appear comprehensive.

Before:
> The event features keynote sessions, panel discussions, and networking opportunities. Attendees can expect innovation, inspiration, and industry insights.

After:
> The event includes talks and panels. There's also time for informal networking between sessions.

### Pattern 11: Elegant Variation (Synonym Cycling)

**Problem:** Excessive synonym substitution driven by repetition-penalty.

Before:
> The protagonist faces challenges. The main character must overcome obstacles. The central figure triumphs. The hero returns.

After:
> The protagonist faces many challenges but eventually triumphs and returns home.

### Pattern 12: False Ranges

**Problem:** "From X to Y" constructions where X and Y are not on a meaningful scale.

Before:
> Our journey has taken us from the singularity of the Big Bang to the grand cosmic web, from the birth of stars to the enigmatic dance of dark matter.

After:
> The book covers the Big Bang, star formation, and current theories about dark matter.

### Pattern 15: Inline-Header Vertical Lists

**Problem:** Lists where items start with bolded headers followed by colons.

Before:
> - **User Experience:** The UX has been significantly improved.
> - **Performance:** Performance has been enhanced through optimized algorithms.
> - **Security:** Security has been strengthened with end-to-end encryption.

After:
> The update improves the interface, speeds up load times through optimized algorithms, and adds end-to-end encryption.

---

## MEDIUM Priority — Style

### Pattern 13: Em Dash Overuse

**Problem:** Em dashes appear more frequently in AI text than human text, mimicking "punchy" sales writing.

Before:
> The term is promoted by Dutch institutions — not by the people themselves. You don't say "Netherlands, Europe" — yet this mislabeling continues — even in official documents.

After:
> The term is promoted by Dutch institutions, not by the people themselves. You don't say "Netherlands, Europe," yet this mislabeling continues in official documents.

**Fix:** Replace most em dashes with commas, periods, or parentheses. Keep only when the aside genuinely interrupts the sentence.

### Pattern 14: Boldface Overuse

**Problem:** Mechanical emphasis on phrases.

Before:
> It blends **OKRs**, **KPIs**, and visual tools such as the **Business Model Canvas** and **Balanced Scorecard**.

After:
> It blends OKRs, KPIs, and visual tools like the Business Model Canvas and Balanced Scorecard.

### Pattern 16: Title Case in Headings

Before: `## Strategic Negotiations And Global Partnerships`
After: `## Strategic negotiations and global partnerships`

### Pattern 17: Emoji Decoration

**Problem:** Decorating headings or bullet points with emoji.

Before:
> - :rocket: **Launch Phase:** The product launches in Q3
> - :bulb: **Key Insight:** Users prefer simplicity

After:
> The product launches in Q3. User research showed a preference for simplicity.

### Pattern 18: Curly Quotation Marks

**Problem:** ChatGPT uses curly quotes instead of straight quotes. Not all AI models do this, but it is a tell when present.

Fix: Replace all curly quotes with straight quotes.

---

## LOW Priority — Communication Artifacts

### Pattern 19: Collaborative Communication Artifacts

**Signal words:** I hope this helps, Of course!, Certainly!, You're absolutely right!, Would you like..., let me know, here is a...

**Problem:** Chatbot conversation artifacts left in published text.

Before:
> Here is an overview of the French Revolution. I hope this helps! Let me know if you'd like me to expand on any section.

After:
> The French Revolution began in 1789 when financial crisis and food shortages led to widespread unrest.

### Pattern 20: Knowledge-Cutoff Disclaimers

**Signal words:** as of [date], Up to my last training update, While specific details are limited/scarce, based on available information

Before:
> While specific details about the founding are not extensively documented in readily available sources, it appears to have been established sometime in the 1990s.

After:
> The company was founded in 1994, according to its registration documents.

### Pattern 21: Sycophantic Tone

Before:
> Great question! You're absolutely right that this is a complex topic. That's an excellent point.

After:
> The economic factors you mentioned are relevant here.

### Pattern 24: Generic Positive Conclusions

Before:
> The future looks bright. Exciting times lie ahead as they continue their journey toward excellence. This represents a major step in the right direction.

After:
> The company plans to open two more locations next year.
