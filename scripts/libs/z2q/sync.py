import json
import subprocess
from pathlib import Path
import re
from .config import config
from .front_matter import ZennFrontMatter, QiitaFrontMatter, FM_SEPARATOR
from ..utils import get_logger

class ZennToQiita(object):
    ROOT = config.repository_root
    ZENN_ARTICLE_DIRECTORY = config.zenn_article_directory
    QIITA_ARTICLE_DIRECTORY = config.qiita_article_directory
    QIITA_CLI = config.node_modules_directory / ".bin" / "qiita"

    def __init__(self, zenn_article_id: str, log_level: int = 2):
        self._zenn_article_id = zenn_article_id
        self._zenn_front_matter = self._extract_zenn_front_matter()
        self._zenn_body = self._extract_zenn_article_body()
        self._qiita_article_id = ""
        self._logger = get_logger(log_level)

    @property
    def logger(self):
        return self._logger

    @property
    def zenn_article_id(self) -> str:
        # ID of the article of Zenn to convert
        return self._zenn_article_id

    @property
    def zenn_article(self) -> Path:
        return self.ZENN_ARTICLE_DIRECTORY / f"{self.zenn_article_id}.md"

    @property
    def zenn_front_matter(self) -> ZennFrontMatter:
        return self._zenn_front_matter

    @property
    def zenn_body(self) -> list[str]:
        return self._zenn_body

    @property
    def tentative_article(self):
        return self.QIITA_ARTICLE_DIRECTORY / f"{self.zenn_article_id}.md"

    @property
    def qiita_article_id(self) -> str:
        return self._qiita_article_id

    @property
    def qiita_article(self) -> Path:
        return self.QIITA_ARTICLE_DIRECTORY / f"{self.qiita_article_id}.md"

    def _does_zenn_article_exist(self) -> bool:
        return self.zenn_article.exists()

    def _does_qiita_article_exist(self) -> bool:
        return self.qiita_article.exists()

    def _get_synced_qiita_article_id(self) -> str|None:
        return next(iter([re.sub('<!-- qiita article id: (.*) -->\n', r'\1', line)
                          for line in self.zenn_body
                          if re.search('<!-- qiita article id: .* -->', line)]),
                    None)

    def _stamp_synced_qiita_article_id(self) -> None:
        with self.zenn_article.open("a") as f:
            f.write(f"\n<!-- qiita article id: {self.qiita_article_id} -->\n")

    def _stamp_synced_zenn_article_id(self, body: list[str]) -> list[str]:
        return body + [f"\n<!-- zenn article id: {self.zenn_article_id} -->\n"]

    def _create_qiita_article(self) -> None:
        fm = QiitaFrontMatter(title="", tags=[], private=True)
        fm.title = self.zenn_front_matter.title
        fm.tags = self.zenn_front_matter.topics
        fm_string = fm.create_string()
        body_string = self._convert_body()
        self._write_out(self.tentative_article, fm_string, body_string)
        completed_proc = subprocess.run([
            self.QIITA_CLI.as_posix(),
            "publish", self.zenn_article_id,
            "--root", self.ROOT.as_posix()],
            stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        if completed_proc.returncode != 0:
            raise RuntimeError(f"Failed to create a new Qiita article: {completed_proc.stderr!r}")
        fm = self._extract_qiita_front_matter(self.tentative_article)
        self._qiita_article_id = fm.id
        self.tentative_article.rename(self.qiita_article)

    def _extract_zenn_front_matter(self) -> ZennFrontMatter:
        with self.zenn_article.open("r") as f:
            lines = f.readlines()
        is_fm_started = False
        fm = []
        for line in lines:
            if re.fullmatch(rf'^{FM_SEPARATOR}\n$', line) and is_fm_started:
                break
            if is_fm_started:
                fm.append(line)
            if re.fullmatch(rf'^{FM_SEPARATOR}\n$', line):
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

    def _extract_qiita_front_matter(self, file_path: Path) -> QiitaFrontMatter:
        with file_path.open("r") as f:
            lines = f.readlines()
        is_fm_started = False
        fm = []
        for line in lines:
            if re.fullmatch(rf'^{FM_SEPARATOR}\n$', line) and is_fm_started:
                break
            if is_fm_started:
                fm.append(line)
            if re.fullmatch(rf'^{FM_SEPARATOR}\n$', line):
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

    def _convert_front_matter(self) -> str:
        fm = self._extract_qiita_front_matter(self.qiita_article)
        fm.title = self.zenn_front_matter.title
        fm.tags = self.zenn_front_matter.topics
        fm.private = not self.zenn_front_matter.published
        return fm.create_string()

    def _extract_zenn_article_body(self) -> list[str]:
        with self.zenn_article.open("r") as f:
            lines = f.readlines()
        is_fm_started = False
        is_fm_ended = False
        body = []
        for line in lines:
            if is_fm_started and is_fm_ended:
                body.append(line)
            if re.fullmatch(rf'^{FM_SEPARATOR}\n$', line) and is_fm_started:
                is_fm_ended = True
            if re.fullmatch(rf'^{FM_SEPARATOR}\n$', line):
                is_fm_started = True
        return body

    @classmethod
    def _convert_info_note(cls, line: str) -> str:
        return re.sub(r'^:::message$', r':::note info', line)

    @classmethod
    def _convert_alert_note(cls, line: str) -> str:
        return re.sub(r'^:::message alert$', r':::note alert', line)

    @classmethod
    def _remove_synced_qiita_article_id(cls, line: str) -> str:
        return re.sub(r'<!-- qiita article id: .* -->\n', '', line)

    @classmethod
    def _mark_footnote(cls, line: str) -> str:
        return re.sub(r'\^\[.*\]', '__FOOTNOTE__', line)

    @classmethod
    def _extract_footnotes_from_line(cls, line: str) -> list[str]:
        footnotes = re.findall(r'\^\[.*\]', line)
        return [re.sub(r'^\^\[(.*)\]$', r'\1', footnote) for footnote in footnotes]

    @classmethod
    def _extract_footnotes(cls, body: list[str]) -> list[str]:
        extracted = [cls._extract_footnotes_from_line(line)
                     for line in body]
        return [footnote for footnotes in extracted for footnote in footnotes]

    @classmethod
    def _convert_footnotes(cls, body: list[str]) -> str:
        footnotes: list[str] = cls._extract_footnotes(body)
        if len(footnotes):
            body = [cls._mark_footnote(line) for line in body]
            body.append("\n")
            body.extend([f'[^{i}]: {footnote}\n'
                        for i, footnote in enumerate(footnotes, 1)])
            body_string = "".join(body)
            for i in range(1, len(footnotes) + 1):
                body_string = re.sub(rf'__FOOTNOTE__', f'[^{i}]', body_string, count=1)
        else:
            body_string = "".join(body)
        return body_string

    def _convert_image_path(self, line: str) -> str:
        # ローカルの画像パス + 幅指定あり
        path = re.sub(rf'!\[(.*)\]\(/(images/{self.zenn_article_id}/.*) =([0-9]*)x\)', r'<img src="https://raw.githubusercontent.com/aYukiYoshida/tips/main/\2" alt="\1" width="\3">', line)
        # ローカルの画像パス + 幅指定なし
        path = re.sub(rf'!\[(.*)\]\(/(images/{self.zenn_article_id}/.*)\)', r'<img src="https://raw.githubusercontent.com/aYukiYoshida/tips/main/\2" alt="\1">', path)
        # 画像のURL + 幅指定あり
        path = re.sub(rf'!\[(.*)\]\((.*) =([0-9]*)x\)', r'<img src="\2" alt="\1" width="\3">', path)
        # 画像パスのURL + 幅指定なし
        path = re.sub(rf'!\[(.*)\]\((.*)\)', r'<img src="\2" alt="\1">', path)
        return path

    def _convert_body(self) -> str:
        body = [self._convert_info_note(line) for line in self.zenn_body]
        body = [self._convert_alert_note(line) for line in body]
        body = [self._convert_image_path(line) for line in body]
        body = [self._remove_synced_qiita_article_id(line) for line in body]
        body = self._stamp_synced_zenn_article_id(body)
        # NOTE: 必ず self._convert_footnotes(body: list[str]) を戻り値にする
        return self._convert_footnotes(body)

    @classmethod
    def _write_out(cls, file_path: Path, fm: str, body: str) -> None:
        with file_path.open("w") as f:
            f.write(fm + body)

    def sync(self) -> None:
        self.logger.info(f"Convert Zenn to Qiita")
        if self._does_zenn_article_exist():
            self.logger.info(f"Zenn article: {self.zenn_article}")
        else:
            raise FileNotFoundError(f"{self.zenn_article} does not exist.")

        _synced_qiita_article_id = self._get_synced_qiita_article_id()
        if _synced_qiita_article_id is None:
            self._create_qiita_article()
            self.logger.info(f"Qiita article: {self.qiita_article}")
            self._stamp_synced_qiita_article_id()
        else:
            self._qiita_article_id = _synced_qiita_article_id
            if self._does_qiita_article_exist():
                self.logger.info(f"Qiita article: {self.qiita_article}")
            else:
                raise FileNotFoundError(f"{self.qiita_article} does not exist.")
        fm = self._convert_front_matter()
        body = self._convert_body()
        self._write_out(self.qiita_article, fm, body)
