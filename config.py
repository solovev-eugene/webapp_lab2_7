'''
Модуль config.py - настройки приложения Flask.

Этот модуль содержит:
- Переменные для API и допустимые операции
'''

OPERATIONS = {
    "max",
    "min",
    "avg"
}

DISEASE_FIELDS_TYPES = {
    "id": int,
    "country": str,
    "region": str,
    "population": int,
    "cases": int,
    "deaths": int,
    "recovered": int,
}
DISEASE_API_FIELDS = [
    "id",
    "country",
    "region",
    "population",
    "cases",
    "deaths",
    "recovered"
]
DISEASE_CREATE_FIELDS = [
    # "id",
    "country",
    "region",
    "population",
    "cases",
    "deaths",
    "recovered"
]
