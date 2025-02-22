from typing import Type, Optional, Dict
import uuid
from fastapi import HTTPException
from sqlalchemy import or_, select, func, and_
from sqlalchemy.orm import Session

from common.operators import Operators
from schemas.pagination import BaseQuerySchema


class BaseService:
    def __init__(self, session: Session):
        self.session = session

    def get_item_by_id(self, model_class: Type, item_id: uuid.UUID) -> Type:
        item = self.session.get(model_class, item_id)
        return item

    def get_item_by_filter(self, model_class: Type, kwargs: Optional[Dict], exclude_id=None) -> Type:
        query = self.session.query(model_class).filter_by(**kwargs)
        if exclude_id:
            query = query.filter(model_class.id != exclude_id)
        return query.first()

    def get_or_not_found(self, model_class: Type, item_id: uuid.UUID, message=None):
        message = f"{model_class.__name__} not found." if not message else message
        item = self.get_item_by_id(model_class, item_id)
        if item is None:
            raise HTTPException(status_code=404, detail=message)
        return item

    def get_or_bad_request(self, model_class: Type, item_id: uuid.UUID, message=None):
        item = self.get_item_by_id(model_class, item_id)
        if item is None:
            raise HTTPException(status_code=400, detail=message)
        return item

    def get_or_create(self, model: Type, data: Dict, kwargs: Optional[Dict] = None):
        if kwargs:
            return self.session.query(model).filter_by(**kwargs).first()
        item = model()
        for key in data:
            if key in model.__table__.columns:
                setattr(item, key, data[key])
        self.session.add(item)
        self.session.flush()
        return item

    def update_or_not_found(self, model_class: Type, item_id: uuid.UUID, data: dict, message=None):
        item = self.get_or_not_found(model_class, item_id, message=message)
        for key in data:
            # don't update id
            if key == "id":
                continue

            if key in model_class.__table__.columns:
                setattr(item, key, data[key])
        return item

    def get_pagination_data(self, base_query, params: BaseQuerySchema, search_fields=None, filters=None):
        if params.search and search_fields and len(search_fields) > 0:
            or_conditions = [field.ilike(f"%{params.search}%") for field in search_fields]
            base_query = base_query.filter(or_(*or_conditions))

        if filters and isinstance(filters, list) and len(filters) > 0:
            and_conditions = []
            for field, op, value in filters:
                if op in [Operators.between]:
                    param = getattr(field, Operators[op].value)(*value)
                else:
                    param = getattr(field, Operators[op].value)(value)
                and_conditions.append(param)
            base_query = base_query.filter(and_(*and_conditions))

        if params.custom_order is False:
            if params.desc:
                base_query = base_query.order_by(params.order_by.desc())
            else:
                base_query = base_query.order_by(params.order_by)

        base_query_cte = base_query.cte()
        total_query = select(func.count()).select_from(base_query_cte)
        total = self.session.query(total_query).count()

        data_query = base_query.offset(params.offset).limit(params.limit)
        if params.custom_order is False:
            data = self.session.query(data_query).all()
        else:
            data = self.session.query(data_query).count()

        return data, total
