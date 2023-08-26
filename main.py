import requests
import datetime
from model import engine, SwapiPerson, Base
from sqlalchemy.orm import Session, sessionmaker


# ОПРЕДЕЛЯЕМ КОЛИЧЕСТВО ПЕРСОНАЖЕЙ
# PERSON_COUNT = requests.get(f"https://swapi.dev/api/people").json()["count"]


# ПОЛУЧАЕМ СТРАНИЦУ ПЕСОНАЖА
def get_person(person_id: int):
    json_data = requests.get(f"https://swapi.dev/api/people/{person_id}").json()
    return json_data


# ПОЛУЧАЕМ ДАННЫЕ СО СТРАНЫЦЫ ПО URL
def get_value_url(urls_list, column: str):
    value_list = []
    if isinstance(urls_list, str):
        value_list.append(requests.get(f"{urls_list}").json()[column])
    else:
        for url in urls_list:
            value_list.append(requests.get(f"{url}").json()[column])
    return value_list


# ПАРСИМ ДАННЫЕ СО СТРАНИЦЫ
# И ДОБАВЛЯЕМ В БД
def add_person(json_value):
    session = Session(bind=engine)
    value_add = SwapiPerson(
        name=json_value["name"],
        birth_year=json_value["birth_year"],
        gender=json_value["gender"],
        eye_color=json_value["eye_color"],
        hair_color=json_value["hair_color"],
        height=json_value["height"],
        mass=json_value["mass"],
        skin_color=json_value["skin_color"],
        films=get_value_url(json_value["films"], "title"),  # --- URL
        planets=get_value_url(json_value["homeworld"], "name"),  # --- URL
        species=get_value_url(json_value["species"], "name"),  # --- URL
        starships=get_value_url(json_value["starships"], "name"),  # --- URL
        vehicles=get_value_url(json_value["vehicles"], "name"),  # --- URL
    )
    session.add(value_add)
    print(session.new)
    session.commit()


def main():
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)

    start = datetime.datetime.now()

    for person_id in range(1, 10):
        add_person(get_person(person_id))

    print('Время выполнения - ', datetime.datetime.now() - start)


if __name__ == '__main__':
    main()
