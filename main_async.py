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
            person = await response.json()
            print(f"Запрос выполнен: {person}")
            return person
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
        async with ClientSession() as client_session:
            
            for character_data in json_value:
                if character_data is not None:

                    films = await get_value_url(character_data["films"], "title"),          # --- URL
                    planets = await get_value_url(character_data["homeworld"], "name"),     # --- URL
                    species = await get_value_url(character_data["species"], "name"),       # --- URL
                    starships = await get_value_url(character_data["starships"], "name"),   # --- URL
                    vehicles = await get_value_url(character_data["vehicles"], "name"),     # --- URL

                    value_add = SwapiPerson(
                        name=character_data["name"],
                        birth_year=character_data["birth_year"],
                        gender=character_data["gender"],
                        eye_color=character_data["eye_color"],
                        hair_color=character_data["hair_color"],
                        height=character_data["height"],
                        mass=character_data["mass"],
                        skin_color=character_data["skin_color"],
                        films=films,            # --- URL
                        planets=planets,        # --- URL
                        species=species,        # --- URL
                        starships=starships,    # --- URL
                        vehicles=vehicles,      # --- URL
                    )

                    session.add(value_add)
                    print("Запись в БД выполнена")
                    await session.commit()


async def main():
    # =================================================================
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
        await conn.commit()

    async with ClientSession() as session:
        coro = [get_person(people_id, session=session) for people_id in range(1, 10)]
        people = await asyncio.gather(*coro)
        asyncio.create_task(add_person(people))

    tasks = set(asyncio.all_tasks()) - {asyncio.current_task()}
    for task in tasks:
        await task


if __name__ == '__main__':
    asyncio.run(main())
