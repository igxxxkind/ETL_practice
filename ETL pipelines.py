from pydantic import BaseModel, Field, field_validator
from datetime import date
from typing import Optional

    # There are three layers of validation:
    # 1. Type coercion - recognition of inputted data as they fall into fields with predefined types
    # 2. Field validators. These are methods decorated with @field_validator that perform validation on individual fields. They can also transform the data as needed.
    # 3. Model Validators. These are methods decorated with @model_validator that perform validation across multiple fields or the entire model. They can also transform the data as needed.

    
class Crops(BaseModel):
    crop_type: str
    quantity: int # this is the first layer of data validation
    planting_date: date
    watering_schedule: Optional[str] = None
    fertilizing_schedule: Optional[str] = None
    
    @field_validator('quantity') # this is the second layer of data validation
    @classmethod
    def quantity_must_be_positive(cls, value):
        if value<=0:
            raise ValueError("Quantity must be positive")
        return value
    
    @field_validator('planting_date')
    @classmethod
    def planting_date_cannot_be_future(cls, value):
        if value> date.today():
            raise ValueError("Planting date cannot be in the future")
        return value
    
    

if __name__ == "__main__":
    
    Betalux = Crops(crop_type="Tomatoes", quantity=20, planting_date=date(2026, 4, 23))
    Des_Andes = Crops(crop_type="Tomatoes", quantity=20, planting_date=date(2026, 4, 23))
    CaliforniaWonder= Crops(crop_type="Bell Papers", quantity=30, planting_date=date(2026, 4, 23))
    Basil_Black = Crops(crop_type="Basil", quantity=30, planting_date=date(2026, 4, 23))
    Basil = Crops(crop_type="Basil", quantity=30, planting_date=date(2026, 4, 23))
    Cilantro = Crops(crop_type="Cilantro", quantity=15, planting_date=date(2026, 5, 10))

    
    