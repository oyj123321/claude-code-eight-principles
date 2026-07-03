# Convention Project

## Project Conventions

### File Naming
- All files use **kebab-case**: `user-profile.js`, not `userProfile.js` or `UserProfile.js`
- Route files go in `src/routes/`
- Test files mirror the source tree under `tests/`

### Exports
- **Named exports only** — no `export default`
- Route handlers: `export const handler = (req, res) => { ... }`

### Code Style
- 2-space indentation
- Single quotes for strings
- Trailing commas in multi-line objects
- No semicolons (ASI style)

### API Patterns
- Route path: `src/routes/<resource-name>.js`
- Each route file exports exactly one `handler`
- Handlers are async: `export const handler = async (req, res) => { ... }`
- Use `res.json()` for all responses, never `res.send()` or `res.end()`

### Dependencies
- Express v4
- No TypeScript — plain JavaScript (ES modules)
- No ORM — raw SQL via `better-sqlite3`
