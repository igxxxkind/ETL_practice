from pydantic import BaseModel, Field, field_validator, model_validator, computed_field
from datetime import date, timedelta
from typing import Optional, Dict, List, Union
from enum import Enum

from sqlmodel import SQLModel, Relationship
from sqlmodel import Field as SQLField 
from ..greenhouse import Schedule, Fertilizer, NPKRatio, Soil, Plant, WateringSchedule, Harvest, Garden


class FertilizerBase(SQLModel, table = True):
    id: int | None = SQLField(default=None, primary_key=True)
    brand: str
    form_factor: str
    NPK_ratio: Optional[int] = SQLField(default=None, foreign_key='npkratio.id')
    application_method: Optional[str] = None
    application_frequency: Optional[str] = None

    @classmethod
    def from_basemodel(cls, obj: Fertilizer, npk_ratio_id: int) -> "FertilizerBase":
        """ Transform BaseModel class into a flat SQLModel that is ready for table creation."""
        return cls(
            brand=obj.brand,
            form_factor=obj.form_factor,
            NPK_ratio=npk_ratio.id,
            application_method=obj.application_method,
            application_frequency=obj.application_frequency
        )

    def to_basemodel(self) -> Fertilizer:
        """ Transform a flat SQLModel class into a complex BaseModel class."""
        return Fertilizer(
            brand=self.brand,
            form_factor=self.form_factor,
            NPK_ratio = self.NPK_ratio,
            application_method=self.application_method,
            application_frequency=self.application_frequency
        )


class NPKRatioBase(SQLModel, table = True):
    id: int | None = SQLField(default=None, primary_key=True)
    n: Optional[float] = None
    p: Optional[float] = None
    k: Optional[float] = None
    NPK_ratio: Optional[str] = None
    
    @classmethod
    def from_basemodel(cls, obj: NPKRatio) -> "NPKRatioBase":
        "Transform basemodel class into a flat SQLModel that is ready for table creation."
        return cls(
            n=obj.n,
            p=obj.p,
            k=obj.k,
            NPK_ratio=obj.NPK_ratio
        )
        
    def to_basemodel(self) -> NPKRatio:
        "Transform a flat SQL Model into a Basemodel class."
        return NPKRatio(
            n = self.n,
            p = self.p,
            k = self.k,
            NPK_ratio = self.NPK_ratio
        )


class SoilBase(SQLModel, table=True):
    id: int | None = SQLField(default=None, primary_key=True)
    soil_type: Optional[str] = None
    drainage_type: Optional[str] = None
    moisture_level: Optional[str] = None
    ph_level: Optional[float] = None

    @classmethod
    def from_basemodel(cls, obj: Soil) -> "SoilBase":
        return cls(
            soil_type = obj.soil_type,
            drainage_type = obj.drainage_type,
            moisture_level = obj.moisture_level,
            ph_level = obj.ph_level
        )
    
    def to_basemodel(self) -> Soil:
        return Soil(
            soil_type = self.soil_type,
            drainage_type = self.drainage_type,
            moisture_level = self.moisture_level,
            ph_level = self.ph_level
        )

class PlantBase(SQLModel, table=True):
    id: int | None = SQLField(default=None, primary_key=True)
    common_name: str
    plant_family: str
    plant_type: str
    min_temperature: Optional[float] = None
    max_temperature: Optional[float] = None
    growth_stage: str
    sunlight: str
    health_status: str
    soil_id: Optional[int] = SQLField(default = None, foreign_key = "soilbase.id")
    planting_date: Optional[date] = None
    re_planting_date: Optional[date] = None
    last_watered: Optional[date] = None
    last_fertilized: Optional[date] = None
    garden_id: Optional[int] = SQLField(default=None, foreign_key="gardenbase.id")
    garden: Optional["GardenBase"] = Relationship(back_populates = "list_of_plants")
    
    @classmethod
    def from_basemodel(cls, obj: Plant, soil_id: int, garden_id: int) -> "PlantBase":
        return cls(
            common_name = obj.common_name,
            plant_family = obj.plant_family,
            plant_type = obj.plant_type,
            min_temperature = obj.min_temperature,
            max_temperature = obj.max_temperature,
            growth_stage = obj.growth_stage,
            sunlight = obj.sunlight,
            health_status = obj.health_status,
            soil_id = soil_id,
            planting_date = obj.planting_date,
            re_planting_date = obj.re_planting_date,
            last_watered = obj.last_watered,
            last_fertilized = obj.last_fertilized,
            garden_id = garden_id
        )
        
    def to_basemodel(self, soil: Soil) -> Plant:
        return Plant(
            common_name = self.common_name,
            plant_family = self.plant_family,
            plant_type = self.plant_type,
            min_temperature = self.min_temperature,
            max_temperature = self.max_temperature,
            growth_stage = self.growth_stage,
            sunlight = self.sunlight,
            health_status = self.health_status,
            soil = soil,
            planting_date = self.planting_date,
            re_planting_date = self.re_planting_date,
            last_watered = self.last_watered,
            last_fertilized = self.last_fertilized
        )


class WateringScheduleBase(SQLModel, table=True):
    id: int | None = SQLField(default=None, primary_key=True)
    plant_id: int = SQLField(foreign_key='plantbase.id')
    frequency: str
    amount: Optional[float] = None
    time_of_day: str
    rain_detected: bool = False
    
    @classmethod
    def from_basemodel(cls, obj: WateringSchedule, plant_id: int) -> "WateringScheduleBase":
        return cls(
            plant_id = plant_id,
            frequency = obj.frequency,
            amount = obj.amount,
            time_of_day = obj.time_of_day,
            rain_detected = obj.rain_detected
            )
    
    def to_basemodel(self, plant: Plant) -> WateringSchedule:
        return WateringSchedule(
            plant = plant,
            frequency = self.frequency,
            amount = self.amount,
            time_of_day = self.time_of_day,
            rain_detected = self.rain_detected
        )


class HarvestBase(SQLModel, table = True):
    id: int | None = SQLField(default=None, primary_key = True)
    plant_id: int = SQLField(foreign_key = "plantbase.id")
    harvest_date: Optional[date] = None
    quantity: Optional[float] = None
    quality: Optional[str] = None
    notes: Optional[str] = None

    @classmethod
    def from_basemodel(cls, obj: Harvest, plant_id: int) -> "HarvestBase":
        return cls(
            plant_id = plant_id,
            harvest_date = obj.harvest_date,
            quantity = obj.quantity,
            quality = obj.quality,
            notes = obj.notes
        )

    def to_basemodel(self, plant: Plant) -> Harvest:
        return Harvest(
            plant = plant,
            harvest_date = self.harvest_date,
            quantity = self.quantity,
            quality = self.quality,
            notes = self.notes
        )
class GardenBase(SQLModel, table = True):
    id: int | None = SQLField(default=None, primary_key=True)
    name: str
    list_of_plants: List["PlantBase"] = Relationship(back_populates="garden")
    fertilizer: int| None = SQLField(default=None, foreign_key = "fertilizerbase.id")
    
    @classmethod
    def from_basemodel(cls, obj: Garden, plant_id: int) -> "GardenBase":
        return cls(
            plant_id = plant_id,
            name = obj.name,
            fertilizer = obj.fertilizer
        )

    def to_basemodel(self, plant: Plant) -> Harvest:
        return Harvest(
            plant = plant,
            harvest_date = self.harvest_date,
            quantity = self.quantity,
            quality = self.quality,
            notes = self.notes
        )
if __name__ == "__main__":
    
    
    object = Fertilizer(brand="PermaBloom", form_factor = "Liquid", NPK_ratio = NPKRatio(n=1.0, p=2.0, k=5.0), application_method = "Fertigation", application_frequency = "Twice a Month")
    object_base = FertilizerBase.from_basemodel(object)
    print(object_base)
    # transform back to BaseModel
    object_back = object_base.to_basemodel()
    print(object_back)
    print("Success")