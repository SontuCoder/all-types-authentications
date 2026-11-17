# Session-Based Authentication

## 1. Introduction

Session-Based Authentication is a stateful authentication mechanism in which the server creates a session after successfully verifying a user's credentials.

The server generates a unique, unpredictable Session ID and sends it to the client, usually through an HTTP cookie.

The client stores this identifier and automatically sends it with subsequent requests. The server validates the identifier against its session store to determine whether the user is authenticated.

**Example:** When you log in to Gmail, you do not enter your username and password for every request. Your browser maintains an authenticated session.

## 2. History and Evolution

Session-based authentication developed to solve an important limitation of HTTP: HTTP is a stateless protocol.

Each HTTP request is independent. The server does not automatically remember previous requests.

| Year | Development |
|---|---|
| 1994 | Netscape introduced HTTP cookie support. |
| 1997 | RFC 2109 formally described HTTP State Management Mechanism. |
| 2000 | RFC 2965 introduced an updated cookie specification. |
| 2011 | RFC 6265 standardized the widely used Cookie and Set-Cookie mechanisms, replacing RFC 2965. |

**Important:** Session-based authentication is an application architecture, not a technology invented by one individual. HTTP cookies became one of its most widely used mechanisms.

References: RFC 2109 and RFC 6265.

## 3. How Does Session-Based Authentication Work?

The authentication process involves the following steps:

1. **User Login:** The client sends its username and password to the server.
2. **Credential Verification:** The server verifies the submitted credentials against the stored password hash.
3. **Session Creation:** If authentication succeeds, the server generates a unique Session ID.
4. **Session Storage:** The server stores the session information in a database or session store.
5. **Session Response:** The server sends the Session ID to the client through the `Set-Cookie` response header.
6. **Subsequent Requests:** The browser automatically sends the Session ID through the `Cookie` request header.
7. **Session Validation:** The server retrieves and validates the corresponding session.
8. **Authentication Success:** If the session is valid and active, the server allows access to protected resources.
9. **Logout:** The server invalidates the session and instructs the browser to remove its cookie.

## 4. Authentication Flow

```text
          CLIENT (Browser)
                 |
                 |
          Enter Username
            & Password
                 |
                 v
          POST /login
                 |
                 v
          SERVER (Backend)
                 |
                 v
       Verify Username & Password
                 |
          +------+------+
          |             |
       Invalid         Valid
          |             |
          v             v
      401 Error     Generate Session ID
                        |
                        v
                 Store Session in DB
                        |
                        v
                 Set-Cookie Header
                        |
                        v
          CLIENT (Browser)
             Stores Cookie
                        |
                        v
              GET /profile
                        |
                 Cookie Header
                        |
                        v
                 SERVER (Backend)
                        |
                        v
                Validate Session
                        |
                 +------+------+
                 |             |
               Valid         Invalid
                 |             |
                 v             v
           Access Granted   401 Error
```

## 5. HTTP Request and Response Example

### Step 1: Login Request

The client sends credentials in the request body.

```http
POST /login HTTP/1.1
Content-Type: application/json

{
    "username": "admin",
    "password": "password123"
}
```

### Step 2: Server Response

After verifying credentials, the server generates a session identifier.

```http
HTTP/1.1 200 OK
Set-Cookie: session_id=random_session_value;
            HttpOnly;
            Secure;
            SameSite=Lax;
            Path=/
```

The browser stores the cookie.

### Step 3: Access Protected Resource

The browser automatically attaches the cookie.

```http
GET /profile HTTP/1.1
Cookie: session_id=random_session_value
```

The server checks whether the session exists and is valid.

### Step 4: Logout

The client requests logout.

```http
POST /logout HTTP/1.1
Cookie: session_id=random_session_value
```

The server deletes or revokes the corresponding session and expires the cookie.

```http
HTTP/1.1 200 OK
Set-Cookie: session_id=;
            Max-Age=0;
            HttpOnly;
            Secure;
            SameSite=Lax;
            Path=/
```

## 6. Session Storage

A session must be maintained on the server side in a traditional server-side session architecture.

Common storage options:

| Storage | Description |
|---|---|
| In-Memory | Stores sessions in application memory. Suitable for learning and simple development. |
| Database | Stores session records persistently. |
| Redis | Provides fast, centralized session storage and expiration support. |

Example session record:

```json
{
    "session_id": "random_session_value",
    "user_id": 101,
    "created_at": "2026-11-16T10:00:00",
    "last_activity": "2026-11-16T10:15:00",
    "expires_at": "2026-11-16T18:00:00",
    "is_active": true
}
```

In production, consider storing a cryptographic hash of the session token instead of the raw token.

## 7. Important Security Features

Session-based authentication must implement appropriate security measures.

### 7.1 HttpOnly

Prevents JavaScript from accessing the session cookie through `document.cookie`.

Helps reduce session-cookie theft through XSS.

### 7.2 Secure

Ensures the browser sends the cookie only over HTTPS connections.

### 7.3 SameSite

Controls whether cookies are included in cross-site requests.

Common values:
- Strict
- Lax
- None

SameSite provides additional CSRF protection, but it does not replace dedicated CSRF defenses where required.

### 7.4 Session Expiration

Sessions should have expiration policies.

Two important types:

- Idle Timeout: Expires a session after a specified period of inactivity.
- Absolute Timeout: Expires a session after a maximum lifetime, regardless of activity.

### 7.5 Session Regeneration

Generate a new Session ID after successful login and important privilege changes.

This helps prevent Session Fixation attacks.

### 7.6 HTTPS

Always use HTTPS to protect session identifiers during transmission.

## 8. Common Security Attacks

| Attack | Description |
|---|---|
| Session Hijacking | An attacker steals an active Session ID and impersonates the user. |
| Session Fixation | An attacker attempts to make a victim authenticate using a session identifier already known to the attacker. |
| Session Prediction | An attacker attempts to guess predictable Session IDs. |
| CSRF | An attacker tricks an authenticated browser into submitting unwanted requests. |
| XSS | Malicious JavaScript executes in the user's browser and may abuse an authenticated session. |

## 9. Advantages

- Users authenticate once instead of submitting credentials repeatedly.
- Easy to manage user sessions centrally.
- Server can invalidate sessions immediately.
- Supports logout and session expiration.
- Suitable for traditional web applications.
- Session information can be updated on the server without changing client-side data.

## 10. Disadvantages

- Requires server-side session storage.
- Session management increases backend complexity.
- Distributed applications require shared session storage or session coordination.
- Session hijacking can compromise authenticated accounts.
- Cookie-based authentication requires appropriate CSRF protection.
- Session cleanup and expiration must be managed properly.

## 11. Basic Authentication vs Session-Based Authentication

| Feature | Basic Authentication | Session-Based Authentication |
|---|---|---|
| Credentials | Sent in Authorization header | Sent during login |
| Authentication | Credentials verified on requests | Session validated on requests |
| Encoding | Base64 | Random Session ID |
| Server State | No login session required | Server maintains session state |
| Client Storage | Usually credentials cached by client | Session cookie |
| Logout | No standard server-side logout | Session can be invalidated |
| Expiration | Depends on credential management | Session timeout |
| CSRF Risk | Generally lower with manually attached Authorization headers | Relevant because browsers automatically send cookies |
| Scalability | Relatively simple | Requires shared session storage in distributed systems |

## 12. Important Notes

- A Session ID is not a password, but it acts as a bearer credential. Anyone possessing a valid Session ID may be able to access the associated account.
- Never store passwords or sensitive personal information directly inside a Session ID.
- Generate session identifiers using a cryptographically secure random number generator (CSPRNG).
- Use at least 128 bits of randomness when generating your own session identifiers.
- Never expose Session IDs in URLs.
- Deleting the browser cookie alone does not invalidate the server-side session. Always revoke the server-side record.
- Protect session cookies using HttpOnly, Secure and appropriate SameSite settings.

## 13. FastAPI Implementation Consideration

For a FastAPI backend, there is an important distinction.

Starlette's built-in `SessionMiddleware` provides signed cookie-based sessions. The session data is readable by the client but cannot be modified without invalidating its signature.

This is different from a traditional server-side session architecture.

For implementing a server-side session system, a suitable architecture is:

- FastAPI: Backend API.
- SQLModel: Database models.
- PostgreSQL: Persistent user and session records.
- Redis (optional): Centralized session storage.
- HTTP Cookies: Session ID exchange mechanism.

This allows the server to control session creation, validation, expiration and revocation.

## 14. Important Terminology

| Term | Meaning |
|---|---|
| Session | A period of authenticated interaction between a client and server. |
| Session ID | Unique identifier associated with a session. |
| Cookie | Small piece of data stored by the browser. |
| Set-Cookie | HTTP response header used by the server to set cookies. |
| Cookie | HTTP request header used by the client to send cookies. |
| Session Store | Server-side storage for session records. |
| Session Hijacking | Unauthorized use of another user's session. |
| Session Fixation | Attack involving an attacker-controlled or known session identifier. |
| Session Expiration | Termination of a session after its allowed lifetime. |
