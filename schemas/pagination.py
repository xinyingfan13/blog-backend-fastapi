import json
from datetime import datetime
from typing import Optional

from fastapi import Query, HTTPException
from pydantic import BaseModel

from common.constant import FILTER_JSON_NOT_VALID
from common.operators import (
    OPERATORS,
    OP_IN,
    OP_NOT_IN,
    OP_BETWEEN,
    OP_LIKE,
    OP_ILIKE,
    OP_EQ,
    OP_GT,
    OP_LT,
    OP_GTE,
    OP_LTE,
    OP_NOT_EQ,
)


class BaseQuerySchema(BaseModel):
    page: Optional[int] = Query(ge=1, default=1)
    page_size: Optional[int] = Query(ge=1, default=10)
    order: Optional[str] = Query(None, description="Order by this field. Add '-' for descending order.")
    search: Optional[str] = Query(None, description="Global search for all text fields")
    filter: Optional[str] = Query(None, description="It should be only json string. Filter by multiple fields.")

    @property
    def offset(self):
        return self.page_size * (self.page - 1)

    @property
    def limit(self):
        return self.page_size

    @property
    def order_by(self):
        if self.order and self.order.startswith("-"):
            return self.order[1:]
        return self.order

    @property
    def desc(self):
        return True if self.order and self.order.startswith("-") else False

    @property
    def custom_order(self):
        return False

    @property
    def filter_obj(self):
        if not self.filter:
            return []
        try:
            parsed_filters = []
            filter_json = json.loads(self.filter)
            for key, value in filter_json.items():
                field, op = key.rsplit("__", 1)
                if op not in OPERATORS:
                    raise HTTPException(status_code=400, detail=FILTER_JSON_NOT_VALID)
                if op in [OP_IN, OP_NOT_IN, OP_BETWEEN]:
                    if not isinstance(value, list):
                        raise HTTPException(status_code=400, detail=FILTER_JSON_NOT_VALID)
                    if op in [OP_BETWEEN] and len(value) != 2:
                        raise HTTPException(status_code=400, detail=FILTER_JSON_NOT_VALID)
                if op in [OP_LIKE, OP_ILIKE]:
                    value = "%{}%".format(value)
                parsed_filters.append((field, op, value))
            return parsed_filters
        except Exception:
            raise HTTPException(status_code=400, detail=FILTER_JSON_NOT_VALID)


class PaginationResponse(BaseModel):
    total: int
    items: list


def validate_schema(filter_obj, schema):
    type_operators = {
        "string": [OP_LIKE, OP_ILIKE, OP_EQ, OP_NOT_IN, OP_GT, OP_LT, OP_GTE, OP_LTE, OP_NOT_EQ],
        "number": [OP_EQ, OP_GT, OP_GTE, OP_LT, OP_LTE, OP_BETWEEN, OP_NOT_IN, OP_NOT_EQ, OP_IN],
        "boolean": [OP_EQ, OP_NOT_EQ],
        "datetime": [OP_BETWEEN, OP_GT, OP_GTE, OP_LT, OP_LTE, OP_EQ, OP_NOT_EQ],
    }
    valid_filter = []
    for field, op, value in filter_obj:
        if field not in schema:
            raise HTTPException(status_code=400, detail=FILTER_JSON_NOT_VALID)
        field_type = schema[field]
        if op not in type_operators[field_type]:
            raise HTTPException(status_code=400, detail=FILTER_JSON_NOT_VALID)
        if field_type == "string" and type(value) == list:
            value = [str(v) if type(v) != str else v for v in value]
        if field_type == "string" and type(value) != str and type(value) != list:
            value = str(value)
        if field_type == "number" and type(value) != float and type(value) != int and type(value) != list:
            raise HTTPException(status_code=400, detail=FILTER_JSON_NOT_VALID)
        if field_type == "number" and type(value) == list:
            for v in value:
                if type(v) != float and type(v) != int:
                    raise HTTPException(status_code=400, detail=FILTER_JSON_NOT_VALID)
        if field_type == "boolean" and type(value) != bool:
            raise HTTPException(status_code=400, detail=FILTER_JSON_NOT_VALID)
        if field_type == "datetime" and type(value) != list:
            try:
                value = datetime.strptime(value, "%Y-%m-%dT%H:%M:%S")
            except Exception:
                raise HTTPException(status_code=400, detail=FILTER_JSON_NOT_VALID)
        if field_type == "datetime" and type(value) == list:
            new_value = []
            for v in value:
                try:
                    v = datetime.strptime(v, "%Y-%m-%dT%H:%M:%S")
                    new_value.append(v)
                except Exception:
                    raise HTTPException(status_code=400, detail=FILTER_JSON_NOT_VALID)
            value = new_value
        valid_filter.append((field, op, value))
    return valid_filter
