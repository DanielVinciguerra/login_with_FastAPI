from pydantic import BaseModel
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.ext.declarative import DeclarativeMeta
from fastapi.templating import Jinja2Templates
from pathlib import Path


class Settings(BaseModel):
    DB_URL: str = 'sqlite+aiosqlite:///./_app/_database/database.db'
    DBBaseModel: DeclarativeMeta = declarative_base()
    TEMPLATES: Jinja2Templates = Jinja2Templates(directory='templates')
    MEDIA: Path = Path('media')
    AUTH_COOKIE_NAME: str = 'loginsystemtoken'
    SALTY: str = 'AnyKwYandMA7o6Cz0MTksByXHriT2fRuAO2p-0y3SbhR3Ou1PnItPFX7zL3cXo861PA9ByalGBneR7O27QRvWw'


    class Config:
        arbitrary_types_allowed = True
        case_sensitive = True

settings: Settings = Settings()