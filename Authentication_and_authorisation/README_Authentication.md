# 🚀 FastAPI Master Authentication Lab (Stateful Sessions + Stateless JWT + RBAC)

A comprehensive, production-grade reference implementation built with **FastAPI** and Python that unifies **Stateful Cookie-Based Sessions**, **Stateless JSON Web Tokens (JWT)**, and **Role-Based Access Control (RBAC)** into a single clean module.

---

## 🛠️ Tech Stack & Libraries

* **Framework:** FastAPI
* **Server:** Uvicorn
* **Security & Cryptography:** 
  * `PyJWT` (Token encoding/decoding & signature verification)
  * `Passlib` with `Bcrypt` (Secure one-way password hashing)
  * FastAPI Security Utilities (`APIKeyCookie`, `OAuth2PasswordBearer`)
* **Data Validation:** Pydantic v2

---

## 📂 

1. **Stateful Session Authentication:**
   * User login generates a unique session ID stored in a server-side dictionary (`session_store`).
   * Delivers an `HttpOnly` cookie to protect against Cross-Site Scripting (XSS) token theft.
   * Includes dedicated session verification dependency and logout cleanup.

2. **Stateless JWT Authentication (OAuth2 / Bearer Token):**
   * Cryptographically signed tokens using custom function implementation.
   * Embeds user claims (`sub` for identity and `role` for authorization).
   * Automatically parses incoming headers via `Authorization: Bearer <token>.

-
