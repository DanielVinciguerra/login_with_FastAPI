from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.ext.asyncio import AsyncEngine
from sqlalchemy.ext.asyncio import AsyncSession

from _app.core.configs import settings

from _app.core.configs import settings

# Assuming your settings.DB_URL points to an SQLite database
engine : AsyncEngine = create_async_engine(settings.DB_URL, echo=False, future=True)


def get_session() -> AsyncSession:
    __async_session = sessionmaker(
        autocommit=False,
        autoflush=False,
        expire_on_commit=False,
        class_=AsyncSession,
        bind=engine
    )
    
    session: AsyncSession = __async_session()

    return session


async def create_tables() -> None:
    import _app.models.__all_models
    print('Criando as tabelas no banco de dados')
    async with engine.begin() as conn:
        await conn.run_sync(settings.DBBaseModel.metadata.drop_all)
        await conn.run_sync(settings.DBBaseModel.metadata.create_all)
    print('Tabelas criadas com sucesso')

