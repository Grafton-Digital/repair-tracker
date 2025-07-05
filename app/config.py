from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic_core import MultiHostUrl
from pydantic import AnyUrl, computed_field

class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file='.env',
        env_file_encoding='utf-8',
        case_sensitive=True,
    )

    # Database settings
    DB_SCHEME: str = 'sqlite' # or 'postgresql+psycopg'
    DB_HOST: str = 'localhost'
    DB_PORT: int = 5432
    DB_NAME: str = 'database.db' # or 'database.db' for SQLite
    DB_USER: str = 'myuser'
    DB_PASSWORD: str = 'mypassword'

    @computed_field  # type: ignore[prop-decorator]
    @property
    def SQLALCHEMY_DATABASE_URI(self) -> str | AnyUrl:
        if self.DB_SCHEME == 'sqlite':
            return f'sqlite:///{self.DB_NAME}'
        else:
            return MultiHostUrl.build(
                scheme=self.DB_SCHEME,
                username=self.DB_USER,
                password=self.DB_PASSWORD,
                host=self.DB_HOST,
                port=self.DB_PORT,
                path=self.DB_NAME,
            )

    # Application settings
    APP_NAME: str = 'My FastAPI App'
    APP_VERSION: str = '1.0.0'
    JWT_ALGORITHM: str = 'HS256'
    SECRET_KEY: str = 'change_this_secret_key'
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 10080 # 7 days
    SECURE_COOKIES: bool = True  # Set to True in production

settings = Settings()