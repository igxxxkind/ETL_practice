from pydantic import BaseModel, Field, field_validator, model_validator, computed_field
from datetime import date, timedelta
from typing import Optional, Dict, List, Union
from enum import Enum

from sqlmodel import SQLModel

from greenhouse import Schedule, Fertilizer, NPKRatio, Soil, Plant, WateringSchedule, Harvest, Garden


class FertilizerBase(SQLModel):
    name: str
    type: str
    n: Optional[float] = None
    p: Optional[float] = None
    k: Optional[float] = None
    application_method: Optional[str] = None
    application_frequency: Optional[str] = None

    @classmethod
    def from_basemodel(cls, obj: Fertilizer) -> "FertilizerBase":
        """ Transform BaseModel class into a flat SQLModel that is ready for table creation."""
        return cls(
            name=obj.name,
            type=obj.type,
            n=obj.NPK_ratio.n if obj.NPK_ratio else None,
            p=obj.NPK_ratio.p if obj.NPK_ratio else None,
            k=obj.NPK_ratio.k if obj.NPK_ratio else None,
            application_method=obj.application_method,
            application_frequency=obj.application_frequency
        )

    def to_basemodel(self) -> Fertilizer:
        """ Transform a flat SQLModel class into a complex BaseModel class."""
        return Fertilizer(
            name=self.name,
            type=self.type,
            NPK_ratio = NPKRatio(n=self.n, p=self.p, k=self.k),
            application_method=self.application_method,
            application_frequency=self.application_frequency
        )
        
if __name__ == "__main__":
    
    
    object = Fertilizer(name="PermaBloom", type = "Liquid", NPK_ratio = NPKRatio(n=1.0, p=2.0, k=5.0), application_method = "Fertigation", application_frequency = "Twice a Month")
    object_base = FertilizerBase.from_basemodel(object)
    print(object_base)
    # transform back to BaseModel
    object_back = object_base.to_basemodel()
    print(object_back)
    print("Success")