import os
from dotenv import load_dotenv

load_dotenv()


class Global:
    class env:
        DATABASE_URL = os.getenv("DATABASE_URL", "")
        OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")

    @classmethod
    def validate_env(cls):
        from pydantic import BaseModel, Field

        class EnvValidator(BaseModel):
            DATABASE_URL: str = Field(..., description="데이터베이스 연결 URL")
            OPENAI_API_KEY: str = Field(..., description="OpenAI API 키")

        try:
            EnvValidator(
                DATABASE_URL=cls.env.DATABASE_URL, OPENAI_API_KEY=cls.env.OPENAI_API_KEY
            )
        except Exception as e:
            raise ValueError(f"환경변수 검증 실패: {str(e)}")
