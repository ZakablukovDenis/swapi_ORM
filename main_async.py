import asyncio
import requests
from aiohttp import ClientSession
from model import engine, SwapiPerson, Base, Session

# ОПРЕДЕЛЯЕМ КОЛИЧЕСТВО ПЕРСОНАЖЕЙ
PERSON_COUNT = requests.get(f"https://swapi.dev/api/people").json()["count"]


# ПОЛУЧАЕМ СТРАНИЦУ ПЕСОНАЖА
async def get_person(person_id: int, session: ClientSession):
    async with session.get(f'https://swapi.dev/api/people/{person_id}') as response:
        if response.ok:
            person = await response.json()
            print(f'Запрос по персонажу {person["name"]} выполнен')
            return person
        else:
            pass


# ПОЛУЧАЕМ ДАННЫЕ СО СТРАНИЦЫ ПО URL
# async def get_value_url(urls_list, column: str):
#     session = aiohttp.ClientSession()
#     value_list = []
#     if isinstance(urls_list, str):
#         response = await session.get(f"{urls_list}")
#         value_list.append(response.json()[column])
#     else:
#         for url in urls_list:
#             response = await session.get(f"{url}")
#             value_list.append(response.json()[column])
#     await session.close()
#     return value_list


async def get_url(url, key, session):
    async with session.get(f'{url}') as response:
        data = await response.json()
        return data[key]


async def get_urls(urls, key, session):
    tasks = (asyncio.create_task(get_url(url, key, session)) for url in urls)
    for task in tasks:
        yield await task


async def get_value_url(urls, key, session):
    data_list = []
    async for el in get_urls(urls, key, session):
        data_list.append(el)
    return ', '.join(data_list)


# ПАРСИМ ДАННЫЕ СО СТРАНИЦЫ
# И ДОБАВЛЯЕМ В БД
async def add_person(json_value):
    async with Session() as session:
        async with ClientSession() as client_session:

            for character_data in json_value:
                print(f"Начинаем запись персонажа {character_data['name']} в Базу Данных")
                if character_data is not None:

                    films = await get_value_url(character_data["films"], "title", client_session)  # --- URL
                    planets = await get_value_url([character_data["homeworld"]], "name", client_session)  # --- URL
                    species = await get_value_url(character_data["species"], "name", client_session)  # --- URL
                    starships = await get_value_url(character_data["starships"], "name", client_session)  # --- URL
                    vehicles = await get_value_url(character_data["vehicles"], "name", client_session)  # --- URL

                    value_add = SwapiPerson(
                        name=character_data["name"],
                        birth_year=character_data["birth_year"],
                        gender=character_data["gender"],
                        eye_color=character_data["eye_color"],
                        hair_color=character_data["hair_color"],
                        height=character_data["height"],
                        mass=character_data["mass"],
                        skin_color=character_data["skin_color"],
                        films=films,  # --- URL
                        planets=planets,  # --- URL
                        species=species,  # --- URL
                        starships=starships,  # --- URL
                        vehicles=vehicles,  # --- URL
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
        coroutines = [get_person(people_id, session=session) for people_id in range(1, 10)]
        people = await asyncio.gather(*coroutines)
        asyncio.create_task(add_person(people))

    tasks = set(asyncio.all_tasks()) - {asyncio.current_task()}
    for task in tasks:
        await task


if __name__ == '__main__':
    asyncio.run(main())
    # asyncio.run(main(), debug=True)
