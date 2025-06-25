import re
from pydantic import BaseModel, field_validator
from typing import Dict, Any

ALLOWED_OPERATORS = {"=", "<", ">", "<=", ">=", "!="}
ALLOWED_LOGIC = {"AND", "OR"}

class FiltersExpression(BaseModel):
    filter_exp: str
    filter_val: Dict[str, Any]

    @field_validator('filter_exp')
    @classmethod
    def validate_expression(cls, v):
        token_pattern = r"([a-zA-Z_]\w*)\s*(=|<|>|<=|>=|!=)\s*(\w+)"
        logic_pattern = r"\s+(AND|OR)\s+"
        # tokens grouped by: [expr1, 'OR', expr2, 'AND', expr3, ...]
        tokens = re.split(logic_pattern, v)
        for i, token in enumerate(tokens):
            if i % 2 == 0:  # expression
                if not re.fullmatch(token_pattern, token.strip()):
                    raise ValueError(f"Invalid filter expression: {token}")
            else:  # operator
                if token.strip() not in ALLOWED_LOGIC:
                    raise ValueError(f"Invalid operator: {token}")
        return v
