from pydantic import ValidationError, BaseModel, field_validator
from typing import Optional, Literal


class CancerType(BaseModel):
    label: str
    group: Literal["Differentiated thyroid carcinoma", "Medullary thyroid carcinoma", "Anaplastic thyroid carcinoma"]


class Json(BaseModel):
    age: Optional[int]
    T: Optional[Literal["T1", "T1a", "T1b", "T2", "T3", "T3a", "T3b", "T4", "T4a", "T4b", "INSUFFICIENT_INFORMATION"]]
    N: Optional[Literal["Nx", "NX", "N0", "N0a", "N0b", "N1", "N1a", "N1b","INSUFFICIENT_INFORMATION"]]
    M: Optional[Literal["Mx", "MX", "M0", "M1", "INSUFFICIENT_INFORMATION"]]
    cancer_type: CancerType

    @field_validator('age')
    def validate_age(cls, value):
        if value <= 0:
            raise ValueError(f"Age: {value} is not valid")
        return value

    @field_validator('cancer_type')
    def validate_cancer_group(cls, value):
        valid_groups = ["Differentiated thyroid carcinoma",
                        "Medullary thyroid carcinoma",
                        "Anaplastic thyroid carcinoma"
                        ]
        if value.group not in valid_groups:
            raise ValueError(f"Cancer group: {value.group} is not valid")
        return value


def validate_json(data: dict) -> Json:
    try:
        return Json(**data)
    except ValidationError as e:
        raise e

