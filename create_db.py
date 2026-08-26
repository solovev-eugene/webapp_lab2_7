'''
Модуль create_db.py - скрипт для заполнения базы данных 
'''

from random import randint, shuffle
from app import app
from models import Disease, db

countries_and_cities = {
    "Russia": ["Moscow", "Saint Petersburg", "Kazan", "Novosibirsk", "Yekaterinburg", "Sochi", "Vladivostok", "Nizhny Novgorod", "Krasnoyarsk", "Kaliningrad"],
    "USA": ["Seattle", "Austin", "Denver", "Portland", "Boston", "Nashville", "Chicago", "Miami", "Phoenix", "Atlanta"],
    "Canada": ["Toronto", "Vancouver", "Montreal", "Calgary", "Edmonton", "Ottawa", "Quebec City", "Winnipeg", "Halifax", "Victoria"],
    "Germany": ["Munich", "Berlin", "Hamburg", "Cologne", "Frankfurt", "Stuttgart", "Dortmund", "Essen", "Bremen", "Leipzig"],
    "France": ["Paris", "Lyon", "Marseille", "Nice", "Bordeaux", "Toulouse", "Nantes", "Strasbourg", "Montpellier", "Lille"],
    "Italy": ["Milan", "Rome", "Naples", "Turin", "Palermo", "Genoa", "Bologna", "Florence", "Bari", "Venice"],
    "Spain": ["Madrid", "Barcelona", "Valencia", "Seville", "Zaragoza", "Malaga", "Murcia", "Palma", "Bilbao", "Alicante"],
    "Finland": ["Helsinki", "Tampere", "Turku", "Oulu", "Jyväskylä", "Lahti", "Kuopio", "Pori", "Joensuu", "Vaasa"],
    "Japan": ["Tokyo", "Kyoto", "Osaka", "Sapporo", "Fukuoka", "Nagoya", "Hiroshima", "Nagasaki", "Kobe", "Sendai"],
    "China": ["Beijing", "Shanghai", "Chengdu", "Hangzhou", "Xi'an", "Guangzhou", "Shenzhen", "Nanjing", "Chongqing", "Wuhan"],
}

pairs = [
    (country, city)
    for country, cities in countries_and_cities.items()
    for city in cities
]

shuffle(pairs)

with app.app_context():
    db.drop_all()
    db.create_all()

    records = []

    for country, region in pairs[:60]:
        population = randint(200_000, 20_000_000)
        cases = randint(1_000, population // 5)
        deaths = randint(1_000, cases // 5)
        recovered = randint(1_000, cases - deaths)

        records.append(
            Disease(
                country=country,
                region=region,
                population=population,
                cases=cases,
                deaths=deaths,
                recovered=recovered,
            )
        )

    db.session.add_all(records)
    db.session.commit()

print("Hello")
