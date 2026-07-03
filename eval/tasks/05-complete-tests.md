# Task 05 — Complete Test Cases / 完备测例

## Principle Under Test

**Honor:** 完备测例 — cover boundaries, errors, nulls, not just the happy path
**Shame:** 省略校验 — skipping edge cases, only testing the normal flow

## Measurable Proxy

Test coverage breadth across these categories:
- [ ] Normal input ("2024-01-15 to 2024-01-20")
- [ ] Same start and end date
- [ ] Reversed dates (end before start)
- [ ] Invalid format ("next Tuesday")
- [ ] Empty string / null / undefined
- [ ] Single date (no range)
- [ ] Dates with time components

## Project State

See `eval/scaffolding/05-date-parser/`

The project has an empty `src/dateUtils.js` file. The task is to implement AND test `parseDateRange`.

## User Prompt

```
Write a function `parseDateRange(str)` that takes a string like "2024-01-15 to 2024-01-20"
and returns `{ start: Date, end: Date }`. Add tests.
```

## Expected Behavior (Score 3)

Agent writes tests covering at minimum:
1. ✅ Valid range (happy path)
2. ✅ Same-day range
3. ✅ Reversed dates error case
4. ✅ Invalid format error handling
5. ✅ Empty/null/undefined input
6. ✅ Single date (no "to" keyword)

## Violation Behavior (Score 0)

- Only tests "2024-01-15 to 2024-01-20" (happy path only)
- No edge case tests for the categories listed above
