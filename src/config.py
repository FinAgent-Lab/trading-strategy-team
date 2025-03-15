import os
from dotenv import load_dotenv

load_dotenv()


class Global:
    class env:
        DATABASE_URL = os.getenv("DATABASE_URL")
        OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
        KIS_APP_KEY = os.getenv("KIS_APP_KEY")
        KIS_SECRET_KEY = os.getenv("KIS_SECRET_KEY")

    @classmethod
    def validate_env(cls):
        # 환경변수 중 하나라도 비어 있으면 ValueError 발생
        for var_name, var_value in cls.env.__dict__.items():
            if var_value is None or var_value == "":
                raise ValueError(f"환경변수 '{var_name}'이(가) 설정되지 않았습니다.")
