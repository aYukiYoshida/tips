from pathlib import Path

from pydantic_settings import BaseSettings


class Config(BaseSettings):
    repository_root: Path = Path(__file__).parents[3]
    node_modules_directory: Path = repository_root / "node_modules"
    zenn_article_directory: Path = repository_root / "articles"
    qiita_article_directory: Path = repository_root / "public"


config = Config()
