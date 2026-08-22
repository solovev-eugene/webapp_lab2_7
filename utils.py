from sqlalchemy import select, func
from config import OPERATIONS


def build_query(model, fields: list[str]):
    return select(*(getattr(model, field) for field in fields))


def build_sorted_query(model, fields: list[str], sort_field: str, order: str = "asc"):
    query = build_query(model, fields)

    column = getattr(model, sort_field)

    match order:
        case "asc":
            query = query.order_by(column.asc())
        case "desc":
            query = query.order_by(column.desc())
        case _:
            raise ValueError(f"Invalid order: {order}")

    return query


def build_func_query(model, field: str, operation: str):
    if operation not in OPERATIONS:
        raise ValueError(f"Unknown operation: {operation}")

    column = getattr(model, field)
    function = getattr(func, operation)

    return select(function(column))


def validate_field(field: str | None, fields: list[str] | dict):
    return field is not None and field in fields


def validate_order(order: str | None):
    return order is not None and order in {"asc", "desc"}


def validate_func(operation: str | None):
    return operation is not None and operation in OPERATIONS


def validate_field_and_type(field: str, value, fields_types: dict[str, type]):
    return validate_field(field, fields_types) and isinstance(value, fields_types[field])


def validate_fields(data: dict, fields_types: dict[str, type]):
    for field, value in data.items():
        if not validate_field_and_type(field, value, fields_types):
            return False
    return True


def validate_fields_put(data: dict, fields_types: dict[str, type]):
    return (
        set(data) != set(fields_types)
        and validate_fields(data, fields_types)
    )
