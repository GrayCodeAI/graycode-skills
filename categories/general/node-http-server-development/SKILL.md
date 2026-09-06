---
name: node-http-server-development
description: "Use when building Node.js HTTP servers and REST APIs with Express — routing, middleware, body parsing, error handling, hardening, and deployment."
license: MIT
tags:
- node
- http
- middleware
- rest-api
- backend
---

# Express.js

Build Node.js web servers and REST APIs with Express — a minimal, unopinionated framework on top of Node's HTTP module.

## Setup

```bash
npm install express
```

```js
import express from "express"
const app = express()
const port = process.env.PORT || 3000

app.listen(port, () => console.log(`listening on ${port}`))
```

`app` is the application object: a function that is the request handler (usable in the Node HTTP server) plus the full routing/middleware API.

## Routing

Define routes with the HTTP-verb methods:

```js
app.get("/", (req, res) => res.send("Hello"))
app.post("/users", handler)
app.put("/users/:id", handler)
app.delete("/users/:id", handler)
app.all("/secret", handler)   // any method
```

- **Params**: `req.params.id` for `:id` segments.
- **Query**: `req.query` (parsed query string).
- **Route patterns**: strings, `:params`, wildcards, and regex.
- **Router**: `express.Router()` to modularize routes into separate files, then `app.use("/users", usersRouter)`.
- **Chaining**: route handlers run in order until one responds or `next()` is called.

## Middleware

Middleware are functions `(req, res, next) => void`. They run in registration order for matching paths.

- Use `app.use(mw)` for every request, `app.use("/api", mw)` for a path, or inline in a route.
- Call `next()` to pass to the next middleware; `next(err)` short-circuits to the error handler.
- `res.send()`/`res.json()` end the response — don't call `next()` after responding.

### Built-in

- `express.json()` — parse JSON bodies.
- `express.urlencoded({ extended: true })` — parse form bodies.
- `express.static("public")` — serve static files from a directory.

## Request and response

- **req**: `req.method`, `req.path`, `req.query`, `req.params`, `req.body`, `req.headers`, `req.ip`.
- **res**: `res.send(data)`, `res.json(obj)`, `res.status(201)`, `res.sendStatus(204)`, `res.redirect(url)`, `res.render("view", data)`, `res.setHeader(k, v)`, `res.set("x-key", v)`, `res.cookie(...)`, `res.end()`.

Always set explicit status codes for APIs: `res.status(201).json({ id })`.

## Error handling

Error-handling middleware has **4 parameters** and must be registered last:

```js
app.use((err, req, res, next) => {
  console.error(err)
  res.status(err.status || 500).json({ error: err.message })
})
```

- Catch async errors with `try/catch` and pass to `next(err)`, or use a small wrapper that forwards rejected promises.
- 404 fallback after all routes: `app.use((req, res) => res.status(404).json({ error: "not found" }))`.

## Production hardening

- **Security**: `helmet` for security headers; `cors` package to configure CORS.
- **Parsing limits**: `express.json({ limit: "1mb" })`.
- **Rate limiting**: `express-rate-limit`.
- **Trust proxy**: `app.set("trust proxy", 1)` when behind a reverse proxy so `req.ip` is accurate.
- **Deployment**: run behind a reverse proxy (nginx/CDN) with HTTPS termination; use an environment-managed `PORT`; keep process managers (PM2/systemd) or a platform like Fly/Railway/Vercel.

## Project structure

```
src/
  app.js        # creates app, wires middleware + routes
  server.js     # starts the server (listens)
  routes/       # express.Router() modules per resource
  middleware/   # auth, validation, logging middleware
  controllers/  # route handlers
```

Keep `app.js` (importable for tests) separate from `server.js` (the listener) so tests can use `supertest` against `app` directly.

## Testing

```bash
npm install -D supertest
```

```js
import request from "supertest"
import app from "../app.js"

test("GET /", async () => {
  const res = await request(app).get("/")
  expect(res.status).toBe(200)
})
```

## See also

- `typescript` skill for typed Express (using `@types/express`).
- `node` skill for async patterns, logging, error handling, and graceful shutdown at the Node.js level.
- Use `fastify` or `nestjs` skills when you need schema validation, structured lifecycle, or batteries-included architecture.