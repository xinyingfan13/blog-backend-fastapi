import inspect
from typing import Type, Any

from fastapi import Form
from pydantic import BaseModel
from pydantic.fields import FieldInfo


def as_form(cls: Type[BaseModel]):
    new_parameters = []

    for field_name, field_info in cls.model_fields.items():  # Use `model_fields` in Pydantic v2
        field_info: FieldInfo  # Ensure correct typing

        default = Form(...) if field_info.is_required() else Form(field_info.default)
        new_parameters.append(
            inspect.Parameter(
                field_name,
                inspect.Parameter.POSITIONAL_OR_KEYWORD,  # Changed to POSITIONAL_OR_KEYWORD for flexibility
                default=default,
                annotation=field_info.annotation if field_info.annotation is not None else Any,
            )
        )

    async def as_form_func(**data):
        return cls(**data)

    sig = inspect.signature(as_form_func)
    sig = sig.replace(parameters=new_parameters)
    as_form_func.__signature__ = sig  # type: ignore[attr-defined]
    setattr(cls, "as_form", as_form_func)
    return cls
