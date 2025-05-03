from pydantic import BaseModel, Field, EmailStr, field_validator


class SignUpDto(BaseModel):
    email: EmailStr = Field(
        ...,
    )
    password: str
    name: str = Field(
        ...,
        min_length=2,
        max_length=16,
    )

    @field_validator("password")
    @classmethod
    def check_password(cls, v: str) -> str:
        if not (4 <= len(v) <= 32):
            raise ValueError("비밀번호는 4~32자여야 해요")
        if not any(c.isalpha() for c in v):
            raise ValueError("비밀번호에 최소 하나 이상의 영문자가 있어야 해요")
        if not any(c.isdigit() for c in v):
            raise ValueError("비밀번호에 최소 하나 이상의 숫자가 있어야 해요")
        return v


class SignInDto(BaseModel):
    email: EmailStr = Field(
        ...,
    )
    password: str
