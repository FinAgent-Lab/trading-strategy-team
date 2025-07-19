import os
from dotenv import load_dotenv

load_dotenv()


class Global:
    class env:
        DATABASE_URL: str = os.getenv("DATABASE_URL")
        OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY")
        KIS_APP_KEY: str = os.getenv("KIS_APP_KEY")
        KIS_SECRET_KEY: str = os.getenv("KIS_SECRET_KEY")
        KIS_ACCOUNT_NUMBER: str = os.getenv("KIS_ACCOUNT_NUMBER")

        # TAVILY_API_KEY: str = os.getenv("TAVILY_API_KEY")

        JWT_SECRET: str = os.getenv("JWT_SECRET")

    @classmethod
    def validate_env(cls):
        from pydantic import BaseModel, Field

        class EnvValidator(BaseModel):
            DATABASE_URL: str = Field(
                ..., min_length=1, description="데이터베이스 연결 URL"
            )
            OPENAI_API_KEY: str = Field(..., min_length=1, description="OpenAI API 키")
            KIS_APP_KEY: str = Field(..., min_length=1, description="KIS 앱 키")
            KIS_SECRET_KEY: str = Field(..., min_length=1, description="KIS 시크릿 키")

            # TAVILY_API_KEY: str = Field(..., min_length=1, description="Tavily API 키")

            JWT_SECRET: str = Field(..., min_length=1, description="JWT 시크릿 키")

        try:
            EnvValidator(
                DATABASE_URL=cls.env.DATABASE_URL,
                OPENAI_API_KEY=cls.env.OPENAI_API_KEY,
                KIS_APP_KEY=cls.env.KIS_APP_KEY,
                KIS_SECRET_KEY=cls.env.KIS_SECRET_KEY,
                # TAVILY_API_KEY=cls.env.TAVILY_API_KEY,
                JWT_SECRET=cls.env.JWT_SECRET,
            )
        except Exception as e:
            raise ValueError(f"환경변수 검증 실패: {str(e)}")
