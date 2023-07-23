import requests
import datetime
from model import engine, SwapiPerson
from sqlalchemy.orm import Session, sessionmaker

# person_count = requests.get(f"https://swapi.dev/api/people").json()["count"]


def get_person(person_id):
    json_data = requests.get(f"https://swapi.dev/api/people/{person_id}").json()
    return json_data


def get_value_url(urls_list, column):
    value_list = []
    if isinstance(urls_list, str):
        value_list.append(requests.get(f"{urls_list}").json()[column])
    else:
        for url in urls_list:
            value_list.append(requests.get(f"{url}").json()[column])
    return value_list


def add_person(json_value):
    session = Session(bind=engine)
    films_value = get_value_url(json_value["films"], "title")
    planets_value = get_value_url(json_value["homeworld"], "name")
    species_value = get_value_url(json_value["species"], "name")
    starships_value = get_value_url(json_value["starships"], "name")
    vehicles_value = get_value_url(json_value["vehicles"], "name")
    value_add = SwapiPerson(
        name=json_value["name"],
        birth_year=json_value["birth_year"],
        gender=json_value["gender"],
        eye_color=json_value["eye_color"],
        hair_color=json_value["hair_color"],
        height=json_value["height"],
        mass=json_value["mass"],
        skin_color=json_value["skin_color"],
        films=films_value,                   # --- URL
        planets=planets_value,               # --- URL
        species=species_value,               # --- URL
        starships=starships_value,           # --- URL
        vehicles=vehicles_value,             # --- URL
    )
    session.add(value_add)
    print(session.new)
    session.commit()


if __name__ == '__main__':
    start = datetime.datetime.now()

    for person_id in range(1, 10):
        add_person(get_person(person_id))

    print('Время выполнения - ', datetime.datetime.now() - start)
    print("Готово")

