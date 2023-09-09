from .convert import ZennToQiita

def z2q(article_id: str, log_level: int) -> None:
    z2q = ZennToQiita(article_id, log_level)
    z2q.convert()
