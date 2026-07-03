import express from 'express'

const app = express()
const PORT = process.env.PORT || 3000

app.use(express.json())

// Route loading — each route file exports a named `handler`
// Example: import { handler as userProfile } from './routes/user-profile.js'
// app.get('/api/users/:id', userProfile)

app.listen(PORT, () => {
  console.log(`Server running on http://localhost:${PORT}`)
})
