from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """
    Classe para gerenciar as configurações da aplicação.
    As variáveis são carregadas de um arquivo .env.
    """

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")
    DATABASE_URL: str
    SECRET_KEY: str
    GOOGLE_API_KEY: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    BASE_URL: str = "http://localhost:8000"

    @property
    def static_dir(self) -> Path:
        """Retorna o diretório de arquivos estáticos."""
        return Path(__file__).parent.parent / "static"

    @property
    def images_dir(self) -> Path:
        """Retorna o diretório de imagens geradas."""
        images_path = self.static_dir / "images"
        images_path.mkdir(parents=True, exist_ok=True)
        return images_path


settings = Settings()
