from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm.session import sessionmaker

DB_USER = "postgres"
DB_PASSWORD = "test123"
DB_HOST = "localhost"
DB_PORT = 5432
DB_DB = "DB_TEST"

PG_DSN = f"postgresql+asyncpg://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_DB}"
engine = create_async_engine(PG_DSN)
# if not database_exists(engine.url):
#     create_database(engine.url)
#     print(f"База данных  {DB_DB} создана")
# else:
#     print(f"База данных  {DB_DB} уже существует")
Session = sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False)
Base = declarative_base()


class SwapiPerson(Base):
    __tablename__ = 'swapi_person'
    id = Column(Integer, primary_key=True)

    name = Column(String)
    birth_year = Column(String)
    gender = Column(String)
    eye_color = Column(String)
    hair_color = Column(String)
    height = Column(String)
    planets = Column(String)
    mass = Column(String)
    films = Column(String)
    skin_color = Column(String)
    species = Column(String)
    starships = Column(String)
    vehicles = Column(String)
