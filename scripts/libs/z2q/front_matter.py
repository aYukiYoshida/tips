from collections import deque
from pydantic import BaseModel

FM_SEPARATOR = "---"

class ZennFrontMatter(BaseModel):
    title: str
    emoji: str
    type: str
    topics: list[str]
    published: bool

class QiitaFrontMatter(BaseModel):
    title: str
    tags: list[str]
    private: bool
    updated_at: str = ""
    id: str = "null"
    organization_url_name: str = "null"
    slide: bool = False
    ignore_publish: bool = False

    def create_string(self) -> str:
        fm_string: deque[str] = deque([])
        fm_string.append(FM_SEPARATOR)
        fm_string.append(f"title: {self.title}")
        fm_string.append(f"tags:")
        fm_string.extend([f"  - {tag}" for tag in self.tags])
        fm_string.append(f"private: {str(self.private).lower()}")
        fm_string.append(f"updated_at: '{self.updated_at}'")
        fm_string.append(f"id: {self.id}")
        fm_string.append(f"organization_url_name: {self.organization_url_name}")
        fm_string.append(f"slide: {str(self.slide).lower()}")
        fm_string.append(f"ignorePublish: {str(self.ignore_publish).lower()}")
        fm_string.append(FM_SEPARATOR)
        return "\n".join(fm_string)
