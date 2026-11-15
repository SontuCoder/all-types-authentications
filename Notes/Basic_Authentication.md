## 1.1 Introduction
Basic Authentication is an HTTP authentication scheme in which a client sends a username and password to a server to authenticate itself.

The client combines the username and password into a single string, encodes that string using Base64, and sends it in the HTTP Authorization header.

The server decodes the Base64 value and validates the credentials.

> [!IMPORTANT]
> Base64 is an encoding mechanism, not encryption. Therefore, Basic Authentication must be used over HTTPS to protect credentials during transmission.

## 1.2 Why Basic Authentication Is Used
Basic Authentication is commonly used when:
- Securing simple REST APIs.
- Authenticating API clients.
- Accessing internal services.
- Integrating third-party applications.
- Testing API endpoints using Postman or cURL.

## 1.3 How Basic Authentication Works

![Basic Auth](./Images/basic-auth.jpg)

### The authentication process involves the following steps:
1. Client Request: The client wants to access a protected API endpoint.
2. Credential Collection: The client provides a username and password.
3. Base64 Encoding: The client combines the credentials in this format:
```bash
   username:password
```
4. Authorization Header: The client encodes the combined string and sends it through the HTTP Authorization header.
5. Server Receives Request: The server extracts the Authorization header.
6. Base64 Decoding: The server decodes the received credentials.
7. Credential Validation: The server checks whether the username and password are valid.
8. Response: The server grants or denies access.

## 1.4 Understanding Base64 Encoding
Let's understand this with an example.

Suppose the credentials are:
```bash
Username: admin
Password: admin123
```

### Step 1: Combine username and password
```bash
admin:admin123
```

### Step 2: Convert the combined string into Base64
```bash
YWRtaW46YWRtaW4xMjM=
```

### Step 3: Send the encoded credentials in the HTTP header
```bash
Authorization: Basic YWRtaW46YWRtaW4xMjM=
```

Notice the format:
```bash
Authorization: Basic <Base64-Encoded-Credentials>
```

> [!IMPORTANT] The client sends the Base64-encoded credentials, not the raw username and password. The server decodes them before validating them.

## 1.5 HTTP Request Example
Suppose we have an API endpoint:
```bash
GET /api/users HTTP/1.1
Host: example.com
Authorization: Basic YWRtaW46YWRtaW4xMjM=
```

## 1.6 Server Response
### Case 1: Successful Authentication

If the credentials are valid:
```bash
HTTP/1.1 200 OK
Content-Type: application/json
```

Response:
```json
{
  "message": "Authentication successful",
  "data": [
    {
      "id": 1,
      "name": "Admin"
    }
  ]
}
```

### Case 2: Failed Authentication

If the credentials are invalid:
```bash
HTTP/1.1 401 Unauthorized
WWW-Authenticate: Basic realm="API"
Content-Type: application/json
```

Response:
```json
{
  "message": "Invalid username or password"
}
```

## 1.7 Advantages
- Simple to understand and implement.
- Supported by almost all HTTP clients.
- No token-generation mechanism required.
- Useful for simple API integrations.
- Easy to test using Postman and cURL.

## 1.8 Disadvantages
- Credentials are sent with every authenticated request.
- Base64 encoding does not provide encryption.
- Compromised credentials can be reused until changed.
- No built-in token expiration or refresh mechanism.
- Requires HTTPS for secure transmission.