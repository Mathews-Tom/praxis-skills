# QA Report Template

## Header
- **Date**: YYYY-MM-DD
- **Mode**: full | quick | regression
- **Application URL**: [URL]
- **Browser automation**: [method used]
- **Duration**: [time spent]

## Health Score: [0-100] / 100

| Category | Weight | Score | Issues |
|----------|--------|-------|--------|
| Console | 15% | /100 | |
| Links | 10% | /100 | |
| Functional | 20% | /100 | |
| UX | 15% | /100 | |
| Accessibility | 15% | /100 | |
| Visual | 10% | /100 | |
| Performance | 10% | /100 | |
| Content | 5% | /100 | |

## Issues by Severity

### Critical (blocks usage)
[List or "None found"]

### Major (degrades experience)
[List or "None found"]

### Minor (cosmetic/polish)
[List or "None found"]

## Issue Detail

For each issue:
- **ID**: QA-NNN
- **Severity**: critical | major | minor
- **Category**: [from taxonomy]
- **Page**: [URL or page name]
- **Description**: [what's wrong]
- **Expected**: [what should happen]
- **Actual**: [what actually happens]
- **Steps to reproduce**: [if applicable]

## Regression Delta (regression mode only)
- **New issues**: [count]
- **Resolved issues**: [count]
- **Persistent issues**: [count]

## Recommendations
Top 3 priority fixes based on severity x user impact.
