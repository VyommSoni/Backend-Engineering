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

    # Transformation: Clean up messy raw strings before type checking
    @field_validator("email", mode="before")
    @classmethod
    def sanitize_email(cls, v: str) -> str:
        if isinstance(v, str):
            return v.strip().lower()
        return v

    # Semantic Validation: Check domain-specific constraints
    @field_validator("username")
    @classmethod
    def check_username(cls, v: str) -> str:
        reserved = {"admin", "root", "system"}
        if v.lower() in reserved:
            raise ValueError(f"Username '{v}' is restricted.")
        return v

    # Complex Validation: Cross-field business logic
    @model_validator(mode="after")
    def validate_dates(self) -> "UserRegistrationSchema":
        if self.start_date > self.end_date:
            raise ValueError("start_date cannot be later than end_date.")
        return self

