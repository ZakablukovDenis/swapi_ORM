import asyncio
# import datetime
import aiohttp
import requests
from sqlalchemy.orm import Session

from model import engine, SwapiPerson, Base


# ОПРЕДЕЛЯЕМ КОЛИЧЕСТВО ПЕРСОНАЖЕЙ
# PERSON_COUNT = requests.get(f"https://swapi.dev/api/people").json()["count"]


# ПОЛУЧАЕМ СТРАНИЦУ ПЕСОНАЖА
async def get_person(person_id: int):
    session = aiohttp.ClientSession()
    response = await session.get(f"https://swapi.dev/api/people/{person_id}")
    json_data = await response.json()
    await session.close()
    return json_data


# ПОЛУЧАЕМ ДАННЫЕ СО СТРАНЫЦЫ ПО URL
async def get_value_url(urls_list, column: str):
    value_list = []
    if isinstance(urls_list, str):
        value_list.append(requests.get(f"{urls_list}").json()[column])
    else:
        for url in urls_list:
            value_list.append(requests.get(f"{url}").json()[column])
    return value_list


# ПАРСИМ ДАННЫЕ СО СТРАНИЦЫ
# И ДОБАВЛЯЕМ В БД
async def add_person(json_value):
    # session = Session(bind=engine)
    async with Session() as session:
        value_add = SwapiPerson(
            name=json_value["name"],
            birth_year=json_value["birth_year"],
            gender=json_value["gender"],
            eye_color=json_value["eye_color"],
            hair_color=json_value["hair_color"],
            height=json_value["height"],
            mass=json_value["mass"],
            skin_color=json_value["skin_color"],
            films=get_value_url(json_value["films"], "title"),          # --- URL
            planets=get_value_url(json_value["homeworld"], "name"),     # --- URL
            species=get_value_url(json_value["species"], "name"),       # --- URL
            starships=get_value_url(json_value["starships"], "name"),   # --- URL
            vehicles=get_value_url(json_value["vehicles"], "name"),     # --- URL
        )
    session.add(value_add)
    # print(session.new)
    await session.commit()


async def main():
    # =================================================================
    # Base.metadata.drop_all(engine)
    # Base.metadata.create_all(engine)
    # start = datetime.datetime.now()
    # for person_id in range(1, 10):
    #     add_person(get_person(person_id))
    # print('Время выполнения - ', datetime.datetime.now() - start)
    # =================================================================
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
        await conn.commit()


if __name__ == '__main__':
    asyncio.run(main())
