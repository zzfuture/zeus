from pydantic import BaseModel


class LongUrl(BaseModel):
    long_url: str

class ShortUrl(BaseModel):
    short_url: str