from pydantic import BaseModel

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
