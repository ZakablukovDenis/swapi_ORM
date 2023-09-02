import asyncio
import aiohttp
import requests
from aiohttp import ClientSession
from sqlalchemy.orm import Session
from model import engine, SwapiPerson, Base


# ОПРЕДЕЛЯЕМ КОЛИЧЕСТВО ПЕРСОНАЖЕЙ
PERSON_COUNT = requests.get(f"https://swapi.dev/api/people").json()["count"]


# ПОЛУЧАЕМ СТРАНИЦУ ПЕСОНАЖА
async def get_person(person_id: int, session: ClientSession):
    async with session.get(f'https://swapi.dev/api/people/{person_id}') as response:
        if response.ok:
            json_data = await response.json()
            return json_data
        else:
            pass


# ПОЛУЧАЕМ ДАННЫЕ СО СТРАНИЦЫ ПО URL
async def get_value_url(urls_list, column: str):
    session = aiohttp.ClientSession()
    value_list = []
    if isinstance(urls_list, str):
        response = await session.get(f"{urls_list}")
        value_list.append(response.json()[column])
    else:
        for url in urls_list:
            response = await session.get(f"{url}")
            value_list.append(response.json()[column])
    await session.close()
    return value_list


# ПАРСИМ ДАННЫЕ СО СТРАНИЦЫ
# И ДОБАВЛЯЕМ В БД
async def add_person(json_value):
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
    await session.commit()


async def main():
    # =================================================================
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
        await conn.commit()

    # ioloop = asyncio.get_event_loop()
    async with ClientSession() as session:
        print(get_person(1, session=session))

    async with ClientSession() as session:
        corootins = [get_person(people_id, session=session) for people_id in range(1, 10)]
        people = await asyncio.gather(*corootins)
        asyncio.create_task(add_person(people))

    tasks = set(asyncio.all_tasks()) - {asyncio.current_task()}
    for task in tasks:
        await task

if __name__ == '__main__':
    asyncio.run(main())
