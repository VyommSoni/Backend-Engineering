# RESTful API Design Guide

A comprehensive reference guide to RESTful API design, focusing on industry-standard practices that allow backend engineers to prioritize business logic over configuration confusion. This guide emphasizes consistency, intuitive interface design, and adherence to established architectural constraints.

---

## Table of Contents

1. [The History and Philosophy of REST](#1-the-history-and-philosophy-of-rest)
2. [URL Structure and Design Best Practices](#2-url-structure-and-design-best-practices)
3. [HTTP Methods and Idempotency](#3-http-methods-and-idempotency)
4. [API Design Workflow: From Nouns to CRUD](#4-api-design-workflow-from-nouns-to-crud)
5. [Pagination, Sorting, and Filtering](#5-pagination-sorting-and-filtering)
6. [Consistency and Developer Experience](#6-consistency-and-developer-experience)

---

## 1. The History and Philosophy of REST

* **Origins of the Web:** Dates back to Tim Berners-Lee in 1990, introducing **URI**, **HTTP**, and **HTML** to share global knowledge.
* **REST (Representational State Transfer):** An architectural style built around core constraints:
  * **Client-Server Model:** Separation of concerns between user interface and data storage/business logic.
  * **Statelessness:** Each request from a client contains all the information needed to understand and process it.
  * **Cacheability:** Responses must explicitly define themselves as cacheable or non-cacheable to improve efficiency.
  * **Layered System:** Clients cannot ordinarily tell whether they are connected directly to the end server or to an intermediary.
  * **Uniform Interface:** Standardized communication between client and server that simplifies and decouples the architecture.

---

## 2. URL Structure and Design Best Practices

* **Hierarchical and Intuitive:** URLs should clearly reflect resource relationships and hierarchy.
* **Standard Base Pattern & Versioning:** Use a dedicated API subdomain or path prefix with explicit versioning (e.g., `https://api.example.com/v1/`).
* **Path Naming Rules:**
  * Use **plural nouns** for resource names (e.g., `/books`).
  * Use **lowercase letters** consistently.
  * Replace spaces with **hyphens** (`-`) for readability (e.g., `/books/harry-potter`).

---

## 3. HTTP Methods and Idempotency

* **Idempotency:** An operation is *idempotent* if performing it multiple times produces the exact same effect as performing it once.
* **Core HTTP Methods:**
  * `GET`: Fetching data (idempotent).
  * `POST`: Creating new resources (non-idempotent by default).
  * `PUT` / `PATCH`: Updating existing resources (`PUT` is idempotent; `PATCH` depends on implementation).
  * `DELETE`: Removing resources (idempotent).

| Method | Action | Idempotent |
| :--- | :--- | :--- |
| `GET` | Read / Fetch resource(s) | Yes |
| `POST` | Create a new resource | No |
| `PUT` | Replace an existing resource | Yes |
| `PATCH` | Partially update a resource | Depends |
| `DELETE` | Remove a resource | Yes |

---

## 4. API Design Workflow: From Nouns to CRUD

1. **Identify Resources (Nouns):** Extract core domain entities from project wireframes, Figma designs, or product requirements (e.g., `Organizations`, `Projects`, `Tasks`).
2. **Map Resources to CRUD Operations:** Define the API interface by mapping each resource to **Create**, **Read**, **Update**, and **Delete** operations using standard HTTP methods and routes.

---

## 5. Pagination, Sorting, and Filtering

* **Pagination:** Use query parameters such as `page` and `limit` to avoid loading massive datasets at once, improving database performance and reducing serialization overhead.
* **Sorting:** Implement `sortBy` and `sortOrder` query parameters so clients can request deterministic response ordering.
* **Filtering:** Use field-based query parameters (e.g., `?status=active`) to narrow down query results cleanly.

Example request:
```http
GET /v1/projects?status=active&sortBy=createdAt&sortOrder=desc&page=1&limit=20
```

---

## 6. Consistency and Developer Experience

* **JSON Standards:** Consistently use `camelCase` for JSON payload keys and maintain uniform field naming across different resources.
* **Smart Defaults:** Provide sensible server-side default values for pagination (`page`, `limit`) and filters (`status`) so API consumers do not have to rely on guesswork.
* **Interactive Documentation:** Use tools like **Swagger / OpenAPI** to provide clear, interactive, and readable documentation for API consumers.