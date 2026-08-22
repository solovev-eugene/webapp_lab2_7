import os

from dotenv import load_dotenv
from flask import Flask, abort, jsonify, request
from flasgger import Swagger

from utils import *
from config import *
from models import Disease, db

load_dotenv()  # подгрузка переменных из .env

app = Flask(__name__)

swagger_template = {
    "swagger": "2.0",
    "info": {
        "title": "Diseases API",
        "description": "REST API для работы с данными о заболеваниях",
        "version": "1.0.0",
    },
}

swagger = Swagger(
    app,
    template=swagger_template
)

# CSRF и DEBUG
app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY")
app.config["DEBUG"] = os.getenv("DEBUG", "false").lower() == "true"

# База данных
app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)


@app.get("/api/diseases")
def get_diseases(model=Disease, fields=DISEASE_API_FIELDS):
    '''
    Получить список случаев заболевания

    ---
    parameters:
      - name: sort
        in: query
        type: string
        description: Поле для сортировки

      - name: order
        in: query
        type: string
        enum: [asc, desc]
        default: asc
        description: Порядок сортировки

      - name: limit
        in: query
        type: integer
        minimum: 1
        description: Количество записей

    responses:
        200:
            description: Список заболеваний
        400:
            description: Некорректный запрос
    '''
    sort_field = request.args.get("sort")
    order = request.args.get("order", default="asc")
    limit = request.args.get("limit", type=int)

    if sort_field:
        if not validate_field(sort_field, fields):
            abort(400)
        if not validate_order(order):
            abort(400)

        query = build_sorted_query(
            model, fields, sort_field, order
        )
    else:
        query = build_query(model, fields)

    if limit is not None:
        if limit < 1:
            abort(400)
        query = query.limit(limit)

    result = db.session.execute(query).mappings().all()

    return jsonify([dict(row) for row in result])


@app.get("/api/diseases/metrics")
def get_disease_metrics(model=Disease, fields=DISEASE_CREATE_FIELDS):
    '''
    Получить максимальное/минимальное/среднее значение

    ---
    parameters:
      - name: field
        in: query
        type: string
        required: true
        enum:
        - population
        - cases
        - deaths
        - recovered
        description: Поле, для которого вычисляется значение

      - name: func
        in: query
        type: string
        required: true
        enum: [max, min, avg]
        description: Агрегатная функция

    responses:
        200:
            description: Полученное значение
        400:
            description: Некорректный запрос
    '''
    field = request.args.get("field")
    operation = request.args.get("func")

    if field is None or operation is None:
        abort(400)

    if not validate_field(field, fields):
        abort(400)

    if not validate_func(operation):
        abort(400)

    query = build_func_query(model, field, operation)

    return jsonify(db.session.scalar(query)), 200


@app.post("/api/diseases")
def add_disease(
    model=Disease,
    fields_types=DISEASE_FIELDS_TYPES,
    create_fields=DISEASE_CREATE_FIELDS
):
    '''
    Добавить запись о случаях заболевания

    ---
    consumes:
    - application/json

    parameters:
      - name: data
        in: body
        required: true
        schema:
        type: object
        required:
            - country
            - region
            - population
            - cases
            - deaths
            - recovered
        properties:
            country:
                type: string
            region:
                type: string
            population:
                type: integer
            cases:
                type: integer
            deaths:
                type: integer
            recovered:
                type: integer

    responses:
        200:
            description: Запись создана
        400:
            description: Некорректные данные
    '''
    data = request.get_json()

    if not validate_fields(data, fields_types):
        abort(400)

    record = model(
        **{
            field: data[field]
            for field in create_fields
        }
    )

    db.session.add(record)
    db.session.commit()

    return jsonify(record.to_dict()), 201


@app.get("/api/diseases/<int:id>")
def get_disease(id: int, model=Disease):
    '''
    Получить запись о случаях заболевания по идентификатору

    ---
    parameters:
      - name: id
        in: path
        type: integer
        required: true
        description: Номер записи

    responses:
        200:
            description: Запись случаев заболевания
        404:
            description: Запись не найдена
    '''
    record = db.get_or_404(model, id)

    return jsonify(record.to_dict()), 200


@app.delete("/api/diseases/<int:id>")
def delete_disease(id: int, model=Disease):
    '''Удалить запись о случаях заболевания

    ---
    parameters:
      - name: id
        in: path
        type: integer
        required: true

    responses:
        200:
            description: Запись удалена
        404:
            description: Запись не найдена
    '''
    record = db.get_or_404(model, id)

    db.session.delete(record)
    db.session.commit()

    return jsonify({"response": "Disease deleted"}), 200


@app.patch("/api/diseases/<int:id>")
def patch_disease(
    id: int,
    model=Disease,
    fields_types=DISEASE_FIELDS_TYPES,
    create_fields=DISEASE_CREATE_FIELDS
):
    '''
    Обновить данные в записи по идентификатору

    ---

    consumes:
    - application/json

    parameters:
      - name: id
        in: path
        type: integer
        required: true

      - name: data
        in: body
        schema:
        type: object
        properties:
            country:
                type: string
            region:
                type: string
            population:
                type: integer
            cases:
                type: integer
            deaths:
                type: integer
            recovered:
                type: integer

    responses:
        200:
            description: Запись частично обновлена
        400:
            description: Некорректный запрос
        404:
            description: Запись не найдена
    '''
    record = db.get_or_404(model, id)
    data = request.get_json()

    if not validate_fields(data, fields_types):
        abort(400)

    for field in create_fields:
        if field in data:
            setattr(record, field, data[field])

    db.session.commit()

    return jsonify(record.to_dict()), 200


@app.put("/api/diseases/<int:id>")
def put_disease(
    id: int,
    model=Disease,
    fields_types=DISEASE_FIELDS_TYPES,
    create_fields=DISEASE_CREATE_FIELDS
):
    '''
    Полностью заменить данные в записи по идентефикатору

    ---
    consumes:
    - application/json

    parameters:
      - name: id
        in: path
        type: integer
        required: true

      - name: data
        in: body
        required: true
        schema:
        type: object
        required:
            - country
            - region
            - population
            - cases
            - deaths
            - recovered
        properties:
            country:
                type: string
            region:
                type: string
            population:
                type: integer
            cases:
                type: integer
            deaths:
                type: integer
            recovered:
                type: integer

    responses:
        200:
            description: Запись полностью обновлена
        400:
            description: Некорректный запрос
        404:
            description: Запись не найдена
    '''
    record = db.get_or_404(model, id)
    data = request.get_json()

    if not validate_fields_put(data, fields_types):
        abort(400)

    for field in create_fields:
        setattr(record, field, data[field])

    db.session.commit()

    return jsonify(record.to_dict()), 200


@app.errorhandler(404)
def not_found(error):
    return jsonify({"error": "Not found"}), 404


@app.errorhandler(400)
def bad_request(error):
    return jsonify({"error": "Bad request"}), 400


debug = os.getenv("DEBUG", "false").lower() == "true"

if __name__ == "__main__":
    app.run(
        debug=app.config["DEBUG"]
    )
