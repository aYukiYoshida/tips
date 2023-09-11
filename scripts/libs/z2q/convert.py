import json
from pathlib import Path
import re
from .config import config
from .front_matter import ZennFrontMatter, QiitaFrontMatter
from ..utils import get_logger

class ZennToQiita(object):
    ZENN_ARTICLE_DIRECTORY = config.zenn_article_directory
    QIITA_ARTICLE_DIRECTORY = config.qiita_article_directory
    FM_SEPARATOR = "---"

    def __init__(self, article_id: str, log_level: int = 2):
        self._article_id = article_id
        self._zenn_front_matter = self._extract_zenn_front_matter()
        self._zenn_body = self._extract_zenn_article_body()
        self._logger = get_logger(log_level)

    @property
    def logger(self):
        return self._logger

    @property
    def article_id(self) -> str:
        # ID of the article of Zenn to convert
        return self._article_id

    @property
    def zenn_article(self) -> Path:
        return self.ZENN_ARTICLE_DIRECTORY / f"{self.article_id}.md"

    @property
    def zenn_front_matter(self) -> ZennFrontMatter:
        return self._zenn_front_matter

    @property
    def zenn_body(self) -> list[str]:
        return self._zenn_body

    @property
    def qiita_article(self) -> Path:
        return self.QIITA_ARTICLE_DIRECTORY / f"{self.article_id}.md"

    def _does_zenn_article_exist(self) -> bool:
        return self.zenn_article.exists()

    def _does_qiita_article_exist(self) -> bool:
        return self.qiita_article.exists()

    def _extract_zenn_front_matter(self) -> ZennFrontMatter:
        with self.zenn_article.open("r") as f:
            lines = f.readlines()
        is_fm_started = False
        fm = []
        for line in lines:
            if re.fullmatch(rf'^{self.FM_SEPARATOR}\n$', line) and is_fm_started:
                break
            if is_fm_started:
                fm.append(line)
            if re.fullmatch(rf'^{self.FM_SEPARATOR}\n$', line):
                is_fm_started = True
        title = next(re.sub(r'title: \"(.*)\"\n', r'\1', s)
                     for s in fm if s.startswith("title:"))
        type_ = next(re.sub(r'type: \"(.*)\".*\n', r'\1', s)
                     for s in fm if s.startswith("type:"))
        emoji = next(re.sub(r'emoji: \"(.*)\"\n', r'\1', s)
                     for s in fm if s.startswith("emoji:"))
        topics = json.loads(next(re.sub(r'topics: (\[.*\])\n', r'\1', s)
                                 for s in fm if s.startswith("topics:")))
        published = next(re.sub(r'published: (.*)\n', r'\1', s)
                         for s in fm if s.startswith("published:")) == "true"
        return ZennFrontMatter(title=title, emoji=emoji, type=type_, topics=topics, published=published)

    def _extract_qiita_front_matter(self) -> QiitaFrontMatter:
        # NOTE: Qiita の article が既に存在している場合にのみ実行する想定
        with self.qiita_article.open("r") as f:
            lines = f.readlines()
        is_fm_started = False
        fm = []
        for line in lines:
            if re.fullmatch(rf'^{self.FM_SEPARATOR}\n$', line) and is_fm_started:
                break
            if is_fm_started:
                fm.append(line)
            if re.fullmatch(rf'^{self.FM_SEPARATOR}\n$', line):
                is_fm_started = True
        updated_at = next(re.sub(r'updated_at: \'(.*)\'\n', r'\1', s)
                     for s in fm if s.startswith("updated_at:"))
        id_ = next(re.sub(r'id: (.*)\n', r'\1', s)
                         for s in fm if s.startswith("id:"))
        org_url_name = next(re.sub(r'organization_url_name: (.*)\n', r'\1', s)
                            for s in fm if s.startswith("organization_url_name:"))
        return QiitaFrontMatter(title="", tags=[], private=False,
                                updated_at=updated_at, id=id_,
                                organization_url_name=org_url_name)

    def _convert_front_matter(self) -> QiitaFrontMatter:
        if self._does_qiita_article_exist():
            fm = self._extract_qiita_front_matter()
        else:
            fm = QiitaFrontMatter(title="", tags=[], private=False)
        fm.title = self.zenn_front_matter.title
        fm.tags = self.zenn_front_matter.topics
        fm.private = not self.zenn_front_matter.published
        return fm

    def _extract_zenn_article_body(self) -> list[str]:
        with self.zenn_article.open("r") as f:
            lines = f.readlines()
        is_fm_started = False
        is_fm_ended = False
        body = []
        for line in lines:
            if is_fm_started and is_fm_ended:
                body.append(line)
            if re.fullmatch(rf'^{self.FM_SEPARATOR}\n$', line) and is_fm_started:
                is_fm_ended = True
            if re.fullmatch(rf'^{self.FM_SEPARATOR}\n$', line):
                is_fm_started = True
        return body

    @classmethod
    def _convert_info_note(cls, line: str) -> str:
        return re.sub(r'^:::message$', r':::note info', line)

    @classmethod
    def _convert_alert_note(cls, line: str) -> str:
        return re.sub(r'^:::message alert$', r':::note alert', line)

    def _convert_image_path(self, line: str) -> str:
        # ローカルの画像パス + 幅指定あり
        path = re.sub(rf'!\[(.*)\]\(/(images/{self.article_id}/.*) =([0-9]*)x\)', r'<img src="https://raw.githubusercontent.com/aYukiYoshida/tips/main/\2" alt="\1" width="\3">', line)
        # ローカルの画像パス + 幅指定なし
        path = re.sub(rf'!\[(.*)\]\(/(images/{self.article_id}/.*)\)', r'<img src="https://raw.githubusercontent.com/aYukiYoshida/tips/main/\2" alt="\1">', path)
        # 画像のURL + 幅指定あり
        path = re.sub(rf'!\[(.*)\]\((.*) =([0-9]*)x\)', r'<img src="\2" alt="\1" width="\3">', path)
        # 画像パスのURL + 幅指定なし
        path = re.sub(rf'!\[(.*)\]\((.*)\)', r'<img src="\2" alt="\1">', path)
        return path

    def _convert_body(self) -> list[str]:
        body = [self._convert_info_note(line) for line in self.zenn_body]
        body = [self._convert_alert_note(line) for line in body]
        body = [self._convert_image_path(line) for line in body]
        return body

    def _create_qiita_article(self, fm: QiitaFrontMatter, body:list[str]) -> None:
        fm_string = []
        fm_string.append(self.FM_SEPARATOR)
        fm_string.append(f"title: {fm.title}")
        fm_string.append(f"tags:")
        fm_string.extend([f"  - {tag}" for tag in fm.tags])
        fm_string.append(f"private: {str(fm.private).lower()}")
        fm_string.append(f"updated_at: '{fm.updated_at}'")
        fm_string.append(f"id: {fm.id}")
        fm_string.append(f"organization_url_name: {fm.organization_url_name}")
        fm_string.append(f"slide: {str(fm.slide).lower()}")
        fm_string.append(self.FM_SEPARATOR)
        with self.qiita_article.open("w") as f:
            f.write("\n".join(fm_string) + "".join(body))

    def convert(self) -> None:
        self.logger.info(f"Convert Zenn to Qiita")
        self.logger.info(f"Zenn article:  {self.zenn_article}")
        self.logger.info(f"Qiita article: {self.qiita_article}")
        if not self._does_zenn_article_exist():
            raise FileNotFoundError(f"{self.zenn_article} does not exist.")
        fm = self._convert_front_matter()
        body = self._convert_body()
        self._create_qiita_article(fm, body)
