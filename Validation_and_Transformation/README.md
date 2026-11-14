# FastAPI Data Validation & Transformation Guide

This project demonstrates how to implement robust data validation, transformation, and business rule enforcement using **FastAPI** and **Pydantic v2** in `models.py`.

---

## 🔍 Overview of Implemented Validation & Transformation Types

In `models.py`, data flows through multiple layers of security and validation before ever touching your business logic:

### 1. Data Transformation (Pre-processing)
* **Concept:** Cleaning and normalizing raw input strings *before* Pydantic performs type checking.
* **Implementation:** Using `@field_validator("email", mode="before")`.
* **Example:** Stripping leading/trailing whitespace and converting uppercase characters to lowercase for emails (e.g., `"  JOHN@EXAMPLE.COM  "` becomes `"john@example.com"`).

### 2. Type Checking & Syntactic Validation
* **Concept:** Ensuring that incoming values match the expected data types and structural formats.
* **Implementation:** Standard field definitions (`username: str`, `age: int`, `start_date: date`) and specialized types like `EmailStr`.
* **Example:** Automatically catching errors if a user passes a string instead of an integer for `age`, or if an email address lacks a valid domain structure.

### 3. Semantic Validation
* **Concept:** Validating individual field values against domain-specific rules and business constraints.
* **Implementation:** Standard `@field_validator("username")`.
* **Example:** Checking if a syntactically correct string username belongs to a list of restricted or reserved keywords (`admin`, `root`, `system`).

### 4. Complex / Cross-Field Validation
* **Concept:** Validating the logical relationship between two or more fields after individual fields have been successfully parsed.
* **Implementation:** Using `@model_validator(mode="after")`.
* **Example:** Ensuring that the `start_date` does not occur chronologically later than the `end_date`.

---

## 📂 Code Reference (`models.py`)

```python
from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel, Field, EmailStr, field_validator, model_validator
from datetime import date
from typing import Optional

app = FastAPI(title="End-to-End Validation Backend")

class UserRegistrationSchema(BaseModel):
    username: str = Field(..., min_length=3, max_length=30)
    age: int = Field(..., ge=18, le=120)
    email: EmailStr
    start_date: date
    end_date: date

    # 1. Transformation: Clean up messy raw strings before type checking
    @field_validator("email", mode="before")
    @classmethod
    def sanitize_email(cls, v: str) -> str:
        if isinstance(v, str):
            return v.strip().lower()
        return v

    # 2. Semantic Validation: Check domain-specific constraints
    @field_validator("username")
    @classmethod
    def check_username(cls, v: str) -> str:
        reserved = {"admin", "root", "system"}
        if v.lower() in reserved:
            raise ValueError(f"Username '{v}' is restricted.")
        return v

    # 3. Complex Validation: Cross-field business logic
    @model_validator(mode="after")
    def validate_dates(self) -> "UserRegistrationSchema":
        if self.start_date > self.end_date:
            raise ValueError("start_date cannot be later than end_date.")
        return self
```