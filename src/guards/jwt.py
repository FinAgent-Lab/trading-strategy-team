from typing_extensions import Self
from jose import jwt


class JwtService:

    _instance = None

    def __new__(cls, *args, **kwargs) -> Self:
        if cls._instance is None:
            cls._instance = super().__new__(cls, *args, **kwargs)
        return cls._instance

    def __init__(self):
        # 초기화 코드 (한 번만 호출됨)
        if not hasattr(
            self, "_initialized"
        ):  # 이미 초기화된 경우는 다시 초기화하지 않음
            self._initialized = True

    def encode(self, payload: dict, secret: str, algorithm: str):
        # if expires_delta:
        #     expire = datetime.now(timezone.utc) + expires_delta
        # else:
        #     expire = datetime.now(timezone.utc) + timedelta(minutes=15)
        # to_encode.update({"exp": expire})
        return jwt.encode(payload, key=secret, algorithm=algorithm)

    def decode(self, token: str, secret: str, algorithm: str):
        return jwt.decode(token=token, key=secret, algorithms=[algorithm])
