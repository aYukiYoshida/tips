from pathlib import Path

from pydantic_settings import BaseSettings


class Config(BaseSettings):
    zenn_article_directory: Path = Path(__file__).parents[3] / "articles"
    qiita_article_directory: Path = Path(__file__).parents[3] / "public"


config = Config()
