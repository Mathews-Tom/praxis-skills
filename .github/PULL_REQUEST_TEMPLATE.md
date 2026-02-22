## Summary

<!-- Brief description of what this PR adds or changes. -->

## Skill Evaluator Results

<!-- Run the skill-evaluator against your skill and paste the scorecard below.
     Minimum score for acceptance: 70% (Adequate). No CRITICAL or HIGH findings.

     To run:
       claude --add-dir skills/skill-evaluator --add-dir skills/your-skill-name
       Then: "Run a quick audit on skills/your-skill-name"
-->

```
(paste scorecard here)
```

## Checklist

- [ ] `SKILL.md` has valid YAML frontmatter with `name` and `description`
- [ ] Skill name is kebab-case, under 64 characters
- [ ] Description is 200-1024 characters with trigger phrases and "Use when" clause
- [ ] No angle brackets or pushy language in description
- [ ] No secrets, credentials, or internal URLs in any file
- [ ] Tested locally with Claude Code
- [ ] All file references in `SKILL.md` resolve to existing files
- [ ] Skill evaluator score is 70% or above
- [ ] No CRITICAL or HIGH findings from skill evaluator
