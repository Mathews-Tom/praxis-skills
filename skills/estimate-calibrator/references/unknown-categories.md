# Unknown Categories

Types of unknowns that affect estimates, with identification techniques and mitigation strategies.

---

## Technical Unknowns

Things we don't know how to do or whether they'll work.

| Unknown | Impact | Mitigation |
|---------|--------|------------|
| New technology | Learning curve, unexpected limitations | Spike: prototype for 1-2 days first |
| Performance at scale | Code works but may be slow | Define threshold, build benchmark early |
| Integration complexity | Third-party API may not behave as documented | Test integration earliest possible |
| Data quality | Input data may be messier than expected | Sample and analyze data before estimating |
| Algorithm suitability | Chosen approach may not work | Prototype with real data before committing |

### Detection Questions

- "Have we used this technology before?"
- "Does this depend on undocumented behavior?"
- "Are we making assumptions about data quality?"
- "Will this work at production scale?"

---

## Scope Unknowns

Things that may change what we're building.

| Unknown | Impact | Mitigation |
|---------|--------|------------|
| Requirements may change | Rework, wasted effort | Implement core first, defer details |
| Edge cases not yet identified | Additional work discovered mid-implementation | Edge case brainstorm session upfront |
| Design not finalized | UI/UX changes after implementation starts | Get design approval before starting |
| Acceptance criteria unclear | "Done" is ambiguous | Define testable criteria before starting |
| Feature creep | Scope grows during implementation | Freeze scope, defer additions to next iteration |

### Detection Questions

- "Is the specification complete?"
- "Have all stakeholders agreed on the scope?"
- "What would the user say if we showed them this spec?"
- "What's explicitly out of scope?"

---

## External Unknowns

Things outside our control.

| Unknown | Impact | Mitigation |
|---------|--------|------------|
| External API availability | Blocked if API is down or access delayed | Request access early, mock while waiting |
| Dependency release | Waiting for a library fix/feature | Use workaround, contribute fix upstream |
| Third-party approval | Waiting for partner/vendor action | Start early, have alternative plan |
| Infrastructure provisioning | Waiting for servers, databases, permissions | Request infrastructure in Phase 1 |
| Legal/compliance review | Waiting for approval | Submit for review as early as possible |

### Detection Questions

- "Does this depend on anyone outside the team?"
- "Are we waiting for any external input?"
- "What happens if the external dependency is delayed by 2 weeks?"

---

## Integration Unknowns

Things that emerge when components connect.

| Unknown | Impact | Mitigation |
|---------|--------|------------|
| Interface mismatch | Components don't connect as expected | Define interfaces in Foundation phase |
| Data format differences | Serialization/deserialization issues | Test integration points early |
| Performance interaction | Components fast alone, slow together | Integration test with realistic data |
| Error propagation | Error in A causes cascade through B, C | Design error handling across boundaries |
| State management | Shared state between components | Define state ownership early |

### Detection Questions

- "Where do components communicate?"
- "Have we tested the interfaces between components?"
- "What happens when one component fails?"

---

## Organizational Unknowns

Things about people and process.

| Unknown | Impact | Mitigation |
|---------|--------|------------|
| Team availability | Key person on vacation, sick, pulled to another project | Identify backup, document everything |
| Review bottleneck | Code review takes days, not hours | Set review SLA, pair program instead |
| Decision delay | Architecture decision needed, no one available to decide | Identify decisions upfront, escalate early |
| Knowledge gap | Only one person understands the system | Pair sessions, documentation |
| Priority shift | Project deprioritized mid-sprint | Accept risk, plan for minimum viable delivery |

---

## Unknown Impact Matrix

| Category | Typical Impact on Worst Case | Frequency |
|----------|-----------------------------|-----------|
| Technical | 2-5x the likely estimate | Common |
| Scope | 1.5-3x | Common |
| External | 0 or complete block | Uncommon but severe |
| Integration | 1.5-2x | Common |
| Organizational | 1.2-2x | Moderate |

---

## When Unknowns Dominate

If unknowns dominate the estimate (worst case > 3x best case):

1. **Spike first** — Invest 1-2 days investigating the biggest unknown
2. **Re-estimate after spike** — New information narrows the range
3. **Timebox** — If you can't reduce uncertainty, timebox: "We'll work on this for 5 days and see where we are"
4. **Accept uncertainty** — Communicate the wide range honestly rather than pretending certainty
