from pydantic import BaseModel


class DraftEmail(BaseModel):
    recipient: str
    subject: str
    body: str
    attachment: str | None = None

