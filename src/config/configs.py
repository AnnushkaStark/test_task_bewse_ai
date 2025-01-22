from pathlib import Path

from .base import BaseSetting

BASE_DIR = Path(__file__).parent.parent


class DBSettings(BaseSetting):
    POSTGRES_HOST: str
    POSTGRES_PORT: int
    POSTGRES_DB: str
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str


class JWTSettings(BaseSetting):
    JWT_SECRET_KEY: str
    JWT_ALGORITHM: str
    JWT_ACCESS_TOKEN_EXPIRES: int  # minutes
    JWT_REFRESH_TOKEN_EXPIRES: int  # minutes
    ACCESS_TOKEN_COOKIE_KEY: str
    REFRESH_TOKEN_COOKIE_KEY: str


class KafkaSettrings(BaseSetting):
    BOOTSTAP_URL: str


kafka_settings = KafkaSettrings()
db_settings = DBSettings()
jwt_settings = JWTSettings()
