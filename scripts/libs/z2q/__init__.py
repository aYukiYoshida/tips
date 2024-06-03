from .convert import ZennToQiita

def z2q(article_id: str, log_level: int) -> None:
    converter = ZennToQiita(article_id, log_level)
    converter.convert()
