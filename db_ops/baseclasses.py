from pydantic import BaseModel, Field, field_validator, model_validator, computed_field
from datetime import date, timedelta
from typing import Optional, Dict, List, Union
from enum import Enum

from sqlmodel import SQLModel

from ..greenhouse import Schedule, Fertilizer, NPKRatio, Soil, Plant, WateringSchedule, Harvest, Garden


class FertilizerBase(SQLModel):
    name: str
    type: str
    NPK_ratio: Optional[str] = None
    application_method: Optional[str] = None
    application_frequency: Optional[str] = None

    @classmethod
    def from_basemodel(cls, obj: Fertilizer) -> "FertilizerBase":
        """ Transform BaseModel class into a flat SQLModel that is ready for table creation."""
        return cls(
            name=obj.name,
            type=obj.type,
            NPK_ratio=obj.NPK_ratio,
            application_method=obj.application_method,
            application_frequency=obj.application_frequency
        )

    def to_basemodel(self) -> Fertilizer:
        """ Transform a flat SQLModel class into a complex BaseModel class."""
        return Fertilizer(
            name=self.name,
            type=self.type,
            NPK_ratio = self.NPK_ratio,
            application_method=self.application_method,
            application_frequency=self.application_frequency
        )


class NPKRatioBase(SQLModel):
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


class SoilBase(SQLModel):
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

class PlantBase(SQLModel):
    common_name: Optional[str] = None
    plant_family: Optional[str] = None
    plant_type: Optional[str] = None
    min_temperature: Optional[float] = None
    max_temperature: Optional[float] = None
    growth_stage: Optional[str] = None
    sunlight: Optional[str] = None
    health_status: Optional[str] = None
    planting_date: Optional[date] = None
    re_planting_date: Optional[date] = None
    last_watered: Optional[date] = None
    last_fertilized: Optional[date] = None
    
    @classmethod
    def from_basemodel(cls, obj: Plant) -> "PlantBase":
        return cls(
            common_name = obj.common_name,
            plant_family = obj.plant_family,
            plant_type = obj.plant_type,
            min_temperature = obj.min_temperature,
            max_temperature = obj.max_temperature,
            growth_stage = obj.growth_stage,
            sunlight = obj.sunlight,
            health_status = obj.health_status,
            planting_date = obj.planting_date,
            re_planting_date = obj.re_planting_date,
            last_watered = obj.last_watered,
            last_fertilized = obj.last_fertilized
        )
        
    def to_basemodel(self) -> Plant:
        return Plant(
            common_name = self.common_name,
            plant_family = self.plant_family,
            plant_type = self.plant_type,
            min_temperature = self.min_temperature,
            max_temperature = self.max_temperature,
            growth_stage = self.growth_stage,
            sunlight = self.sunlight,
            health_status = self.health_status,
            planting_date = self.planting_date,
            re_planting_date = self.re_planting_date,
            last_watered = self.last_watered,
            last_fertilized = self.last_fertilized
        )


class WateringScheduleBase(SQLModel):
    frequency: Optional[Schedule] = None
    amount: Optional[float] = None
    time_of_day: Optional[str] = None
    rain_detected: Optional[bool] = False
    
    @classmethod
    def from_basemodel(cls, obj: WateringSchedule) -> "WateringScheduleBase":
        return cls(
            frequency = obj.frequency,
            amount = obj.amount,
            time_of_day = obj.time_of_day,
            rain_detected = obj.rain_detected
            )
    
    def to_basemodel(self) -> WateringSchedule:
        return WateringSchedule(
            frequency = self.frequency,
            amount = self.amount,
            time_of_day = self.time_of_day,
            rain_detected = self.rain_detected
        )


class HarvestBase(SQLModel):
    harvest_date: Optional[date] = None
    quantity: Optional[float] = None
    quality: Optional[str] = None
    notes: Optional[str] = None

    @classmethod
    def from_basemodel(cls, obj: Harvest) -> "HarvestBase":
        return cls(
            harvest_date = obj.harvest_date,
            quantity = obj.quantity,
            quality = obj.quality,
            notes = obj.notes
        )

    def to_basemodel(self) -> Harvest:
        return Harvest(
            harvest_date = self.harvest_date,
            quantity = self.quantity,
            quality = self.quality,
            notes = self.notes
        )
class GardenBase(SQLModel):
    name: Optional[str] = None
    list_of_plants: Optional[str] = None
    fertilizer: Optional[str] = None
    watering_schedule: Optional[str] = None
    harvests: Optional[str] = None
        
if __name__ == "__main__":
    
    
    object = Fertilizer(name="PermaBloom", type = "Liquid", NPK_ratio = NPKRatio(n=1.0, p=2.0, k=5.0), application_method = "Fertigation", application_frequency = "Twice a Month")
    object_base = FertilizerBase.from_basemodel(object)
    print(object_base)
    # transform back to BaseModel
    object_back = object_base.to_basemodel()
    print(object_back)
    print("Success")