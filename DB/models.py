from sqlmodel import SQLModel, Field
from pydantic import field_validator
import re
from datetime import datetime, timezone

class User(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    username: str = Field(nullable=False, unique=True, index=True)
    password: str = Field(nullable=False)

class Session_Record(SQLModel, table=True):
    session_id: str = Field(nullable=False, primary_key=True)
    user_id: int = Field(nullable=False, foreign_key="user.id", index=True)
    created_at: datetime = Field(default=lambda: datetime.now(timezone.utc), nullable=False)
    last_activity_at: datetime = Field(default=lambda: datetime.now(timezone.utc), nullable=False)
    expires_at: datetime = Field(nullable=False)
    is_active: bool = Field(default=True, nullable=False)

class User_Create(SQLModel):
    username: str
    password: str

    @field_validator("username")
    @classmethod
    def validate_name(cls, value:str):
        if not value.strip():
            raise ValueError("Name should be not empty")
        return value

    @field_validator("password")
    @classmethod
    def check_password(cls, value: str):

        checks = {
            "Minimum 8 characters": lambda v: len(v) >= 8,
            "At least 1 Capital letter": lambda v: bool(re.search(r"[A-Z]", v)),
            "At least 1 Number": lambda v: bool(re.search(r"\d", v)),
            "At least 1 Special character": lambda v: bool(
                re.search(r"[^A-Za-z0-9\s/]", v)
            ),
            "No Spaces": lambda v: not bool(re.search(r"\s", v)),
            "No Slash": lambda v: "/" not in v
        }

        errors = []

        for condition, check in checks.items():
            if not check(value):
                errors.append(condition)

        if errors:
            raise ValueError(
                "Password validation failed: " + ", ".join(errors)
            )

        return value

class User_Response(SQLModel):
    id: int
    username: str

class User_JWT_Response(SQLModel):
    access_token: str
    user: User_Response
