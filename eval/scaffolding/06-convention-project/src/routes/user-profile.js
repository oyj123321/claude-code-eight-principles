// Example route following project conventions:
// - kebab-case filename: user-profile.js
// - Named export: handler
// - Async handler pattern
// - res.json() for responses

export const handler = async (req, res) => {
  const { id } = req.params

  if (!id) {
    return res.json({ error: 'Missing user id' }, 400)
  }

  // Stub — real implementation would query the DB
  const user = {
    id,
    name: 'Example User',
    email: 'user@example.com'
  }

  return res.json({ data: user })
}
