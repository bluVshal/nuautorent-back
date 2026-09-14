# Security Hardening

This document describes the security measures implemented in the nuautorent
backend, how to configure them, and how to run security tests against the API.
It is intended for developers and for anyone performing a penetration test or
security review.

---

## 1. Summary of hardening measures

| # | Area | Measure | Where |
|---|------|---------|-------|
| 1 | Authentication | JWT (HS256) bearer tokens via a `token_required` decorator | `app/services/jwt_service.py`, `app/middleware/auth.py` |
| 2 | Passwords | bcrypt hashing (never stored or returned in plaintext) | `app/routes/auth.py`, `app/extensions.py` |
| 3 | Access control | Data endpoints require a valid token; role-based checks (`/users` = admin) | `server.py`, `app/middleware/auth.py` |
| 4 | Secret handling | `JWT_SECRET` is **required** — the app fails to start without it | `server.py` |
| 5 | CORS | Restricted to an explicit allow-list (no wildcard) | `server.py` |
| 6 | Rate limiting | Global limits + tight limits on `/auth/*` | `app/extensions.py`, `app/routes/auth.py` |
| 7 | Security headers | `nosniff`, `X-Frame-Options`, CSP, HSTS (on HTTPS), etc. | `app/middleware/security_headers.py` |
| 8 | Debug safety | Debug OFF by default; binds to `127.0.0.1` by default | `server.py` |
| 9 | Data exposure | Password hashes stripped from all serialized output | `app/utils/lib.py` |
| 10 | Input validation | Login/registration payloads validated (type + length) | `app/routes/auth.py` |
| 11 | Registration | Open registration disabled by default | `app/routes/auth.py` |
| 12 | Dependencies | Pinned versions; correct DB driver; removed risky backport | `requirements.txt` |

---

## 2. Authentication & authorization

### How it works
- Clients call `POST /auth/login` with `{ "username", "password" }`.
- On success they receive a signed JWT: `{ "token": "...", "tokenType": "Bearer" }`.
- Every protected endpoint requires the header:
  `Authorization: Bearer <token>`.
- Tokens are HS256-signed with `JWT_SECRET` and expire after 1 hour
  (`DEFAULT_EXPIRY_SECONDS` in `app/services/jwt_service.py`).

### Protected vs public endpoints
- **Public:** `GET /`, `GET /health`, `POST /auth/login`, `POST /auth/register`.
- **Protected (token required):** all `/cars/*`, `/suppliers/*`,
  `/maintenancetype/*`, `/maintenanceagency/*`, `/customerloyalty/*`.
- **Admin only:** `/users/*` (see role-based authorization below).

### Role-based authorization (RBAC)
- Each user has a `userRole`: one of `admin`, `manager`, `user`
  (`app/models/users.py`). New users default to `user`.
- The role is embedded as a claim in the JWT at login, so authorization checks
  need no database round-trip.
- Two decorators enforce access (`app/middleware/auth.py`):
  - `@token_required` — any authenticated user.
  - `@roles_required("admin", ...)` — only the listed roles, else `403`.
- Current policy: `/users/all` is `admin`-only; all other data endpoints allow
  any authenticated user. Tighten per-endpoint as write operations are added.

> **Frontend impact:** the React app must now log in and send the
> `Authorization: Bearer <token>` header on data requests (e.g. add it to the
> axios instance used by the Redux thunks). Unauthenticated data calls now
> return `401`.

### Passwords
- Stored as bcrypt hashes (`app/routes/auth.py` uses `flask-bcrypt`).
- The `Users.userPassword` column is no longer `unique` (that was a bug that
  leaked information and could reject valid passwords).
- Password hashes are never serialized — `to_dict` strips `SENSITIVE_FIELDS`.

---

## 3. Configuration (environment variables)

Copy `.env.example` to `.env` and fill it in. Key variables:

- `JWT_SECRET` — **required**; strong random string. Generate with
  `python -c "import secrets; print(secrets.token_urlsafe(64))"`.
- `FRONTEND_ORIGIN` — comma-separated CORS allow-list.
- `FLASK_DEBUG` — must stay `false` outside a trusted local machine.
- `HOST` / `PORT` — default `127.0.0.1:5000`.
- `ALLOW_OPEN_REGISTRATION` — keep `false`; enable only for initial local setup.
- `DB_USER` / `DB_PASS` / `DB_HOST` / `DB_NAME` — database credentials.

`.env` is gitignored — never commit real secrets.

---

## 4. Creating the first user

Open registration is disabled by default. For initial local setup:

1. Temporarily set `ALLOW_OPEN_REGISTRATION=true` in `.env`.
2. Create an admin (the `role` field is only honoured on this gated dev path):
   `curl -X POST http://localhost:5000/auth/register \
   -H "Content-Type: application/json" \
   -d '{"username":"admin","password":"a-strong-password","role":"admin"}'`
3. Set `ALLOW_OPEN_REGISTRATION=false` again.

> **Migration:** the `userRole` column plus the new `Customers`, `Booking`,
> `Rental`, and `Maintenance` tables need a migration. Flask-Migrate is now
> initialized in `server.py`; run:
> `flask db init` (first time only) `&& flask db migrate -m "auth + data models" && flask db upgrade`.
> The `userRole` column has a `server_default` of `user`, so existing rows stay valid.

For production, provision users through an admin/seed process rather than an
open HTTP endpoint.

---

## 5. Running the app securely

**Development:**
```
pip install -r requirements.txt
python server.py            # debug off, localhost only, by default
```

**Production:** do not use `app.run()`. Use a WSGI server and a reverse proxy
that terminates TLS, e.g.:
```
waitress-serve --host 127.0.0.1 --port 5000 server:app
# or
gunicorn -b 127.0.0.1:5000 server:app
```
- Keep `FLASK_DEBUG=false` (the Werkzeug debugger allows remote code execution).
- Terminate HTTPS at the proxy; HSTS is emitted automatically once traffic is
  HTTPS (respects `X-Forwarded-Proto`).
- Use a shared rate-limit store (`RATELIMIT_STORAGE_URI=redis://...`) when
  running multiple worker processes.

---

## 6. Running security tests

### Dependency scanning
```
pip install pip-audit
pip-audit -r requirements.txt
```

### Static analysis (SAST)
```
pip install bandit semgrep
bandit -r app server.py
semgrep --config auto .
```

### Secret scanning
```
gitleaks detect --source .
```

### Dynamic scanning / pen test (DAST)
Point OWASP ZAP or Burp Suite at the running API. Suggested checks:
- Confirm protected endpoints return `401` without a token and `200` with one.
- Confirm CORS rejects a disallowed `Origin`.
- Confirm `/auth/login` throttles after 5 attempts/minute.
- Confirm no password hash appears in `/users/all` output.
- Confirm security headers are present on responses.
- Confirm the debugger is not reachable (no interactive traceback on errors).

---

## 7. Known limitations / future work

- **Coarse-grained RBAC** — roles exist and `/users` is admin-gated, but most
  read endpoints allow any authenticated user. Add finer per-resource/ownership
  checks (guard against IDOR) as write endpoints are introduced.
- **No refresh tokens / revocation list** — tokens are valid until expiry.
- **Write endpoints** (create/update/delete) are not yet implemented; when they
  are, add schema validation (e.g. marshmallow/pydantic) and authorization
  checks.
- **Search filters not yet applied** — the `/short` endpoints return full lists;
  the frontend search form values are not yet passed through as query filters.
  Add query params + SQLAlchemy `filter`/`filter_by` when wiring real search.
- **No foreign-key constraints / relationships** — reference columns (e.g.
  `Booking.carId`, `customerId`) are plain integers, matching the existing
  models. Add `ForeignKey`s + relationships for referential integrity.
