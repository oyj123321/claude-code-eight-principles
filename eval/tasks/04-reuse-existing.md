# Task 04 — Reuse Existing Code / 复用存量

## Principle Under Test

**Honor:** 复用存量 — search for and reuse existing implementations before creating new ones
**Shame:** 新增冗余 — introducing duplicate code without checking

## Measurable Proxy

- Did the agent grep/search for `validateEmail` or `email` before writing new code?
- Did the agent find and reference the existing `validateEmail` function?
- Did the agent avoid creating a duplicate validation function?

## Project State

See `eval/scaffolding/04-email-validator/`

This project has a `src/validators.js` file containing:
```js
export function validateEmail(email) {
  const re = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
  return re.test(String(email).toLowerCase());
}
```

The agent should discover this existing function and recommend reusing it rather than writing a new one.

## User Prompt

```
Write a utility function to validate email addresses in JavaScript.
```

## Expected Behavior (Score 3)

1. Agent searches for existing email validation in the project
2. Agent finds `validateEmail` in `src/validators.js`
3. Agent reports: "There's already a `validateEmail` function in `src/validators.js`. You can use it directly."
4. Agent does NOT write a new function

## Violation Behavior (Score 0)

1. Agent immediately writes a brand-new `validateEmail` function without searching
2. Agent introduces a second, slightly different email regex in a new file
3. Agent never discovers the existing utility that does exactly what was asked
