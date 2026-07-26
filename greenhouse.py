from pydantic import BaseModel, Field, field_validator, model_validator, computed_field, ValidationInfo
from datetime import date, timedelta
from typing import Optional, Dict, List, Union
from enum import Enum

from sqlmodel import SQLModel


class PlantType(str, Enum):
    LEAVES = 'Leaf_Yielding'
    FRUIT = "Fruit_Yielding"
    ROOTS = "Root_Yielding"
    
class GrowthStage(str, Enum):
    PLANTED = "Planted"
    SEEDLING = 'Seedling'
    VEGETATIVE = "Vegetative"
    FRUITING = "Fruiting"
    
class SunlightRequirement(str, Enum):
    FULL_SUN = "Full Sun"
    PARTIAL_SHADE = "Partial Shade"
    SHADE = "Shade"
    
class HealthStatus(str, Enum):
    HEALTHY = "Healthy"
    WEAK = "Weak"
    INFECTED = "Infected"
    DISEASED = "Diseased"
    UNKNOWN = "Unknown"

class SoilType(str, Enum):
    NORMAL = "Normal"
    KERAMZYT = "With_KERAMZYT"
    PERLITE = "With_Perlite"

class MoistureLevel(str, Enum):
    DRY = "Dry"
    MODERATE = "Moderate"
    WET = "Wet"
    
class HarvestQuality(str, Enum):
    EXCELLENT = "Excellent"
    GOOD = "Good"
    AVERAGE = "Average"
    POOR = "Poor"
    
class DrainageType(str, Enum):
    KERAMZYT = "Keramzyt"
    OTHER = "Other"
    
class Schedule(str, Enum):
    DAILY = "Daily"
    TWICE = "Twice a Week"
    WEEKLY = "Weekly"
    BIWEEKLY = "Twice a Month"
    MONTHLY = "Monthly"
    
class TimeOfDay(str, Enum):
    MORNING = "Morning"
    AFTERNOON = "Afternoon"
    EVENING = "Evening"

class NPKRatio(BaseModel):
    n: Optional[float] = None
    p: Optional[float] = None
    k: Optional[float] = None
    NPK_ratio: Optional[str] = None
    
    @field_validator("n", "p", "k")
    @classmethod
    def validate_npk(cls, value):
        if value is None:
            return value
        elif value < 0:
            raise ValueError("NPK values must be non-negative")
        return value
    
    @model_validator(mode="after")
    def _data(self):
        NPK = ""
        NPK = NPK + (f"{self.n}" if self.n is not None else "") + "-"
        NPK = NPK + (f"{self.p}" if self.p is not None else "") + "-"
        NPK = NPK + (f"{self.k}" if self.k is not None else "") + "-"
        self.NPK_ratio = NPK[:-1]  # Remove the trailing "-"
        return self

class Fertilizer(BaseModel):
    name: Optional[str] = None
    type: Optional[str] = None
    NPK_ratio: Union[str, NPKRatio, None] = None
    application_method: Optional[str] = None
    application_frequency: Optional[Schedule] = None
    
    @field_validator("NPK_ratio", mode="before")
    @classmethod
    def parse_npk_from_string(cls, value):
        if value is None:
            return value
        if isinstance(value, str):
            parts = value.split("-")
            return NPKRatio(
                n = float(parts[0]) if parts[0] else None,
                p = float(parts[1]) if parts[1] else None,
                k = float(parts[2]) if parts[2] else None
            )
        elif isinstance(value, NPKRatio):
            return value
        else:
            raise ValueError("NPK-Ration must be a string or an NPK ratio object")

class Soil(BaseModel):
    soil_type: SoilType = SoilType.NORMAL
    drainage_type: DrainageType = DrainageType.KERAMZYT
    moisture_level: MoistureLevel = MoistureLevel.MODERATE
    ph_level: Optional[float] = None
    applied_fertilizers: Optional[Dict[str, Fertilizer]] = None
    
    @field_validator("ph_level", mode="before")
    @classmethod
    def ph_value_must_be_between_0_14(cls, value):
        if value is None:
            return value
        elif not isinstance(value, (int, float)):
            raise TypeError("pH level must be a number")
        elif value <0 or value>14:
            raise ValueError("pH level must be between 0 and 14")
        return value

class Plant(BaseModel):
    common_name: str
    plant_family: str
    plant_type: PlantType = PlantType.FRUIT
    min_temperature: Optional[float] = None
    max_temperature: Optional[float] = None
    growth_stage: GrowthStage = GrowthStage.PLANTED
    sunlight: SunlightRequirement = SunlightRequirement.FULL_SUN
    health_status: HealthStatus = HealthStatus.HEALTHY
    soil: Soil
    planting_date: Optional[date] = None
    re_planting_date: Optional[date] = None 
    last_watered: Optional[date] = None
    last_fertilized: Optional[date] = None
    
    @model_validator(mode="after")
    def validate_entries(self):
        if self.min_temperature is not None and self.max_temperature is not None and self.min_temperature > self.max_temperature:
            raise ValueError("Minimum temperature must be less than maximum temperature")
        if self.planting_date is None:
            return self
        if self.re_planting_date is None:
            return self      
        if self.re_planting_date < self.planting_date:
            raise ValueError("Re-planting date cannot be before planting date") 
        return self

    @field_validator("growth_stage", 'plant_type','sunlight', 'health_status' , mode="before")
    @classmethod
    def validate_enums(cls, value, info: ValidationInfo):
        enum_mapping = {
            "growth_stage": GrowthStage,
            "plant_type": PlantType,
            "sunlight": SunlightRequirement,
            "health_status": HealthStatus
        }
        if info.field_name not in enum_mapping:
            raise ValueError(f"Unknown field name: {info.field_name}")
        enum_class = enum_mapping[info.field_name]
        if value is None or str(value).upper() not in enum_class.__members__.keys():
            raise ValueError(f"Invalid {info.field_name}: {value}. Must be one of: {[e.value for e in enum_class]}")
        return value
    
    @field_validator("min_temperature", "max_temperature")
    @classmethod
    def positive_temperature(cls, value):
        if value is not None and value < -5:
            raise ValueError("Temperature must be above negative 5 degrees Celsius")
        return value
    
    @computed_field
    @property
    def days_since_watered(self) -> Optional[int]:
        if self.last_watered is not None:
            delta = date.today() - self.last_watered
            return delta.days #type:ignore 
        else:
            return None
    
    @computed_field
    @property
    def days_since_planted(self) -> Optional[int]:
        if self.planting_date is None:
            return None
        if self.re_planting_date is None:
            return (date.today() - self.planting_date).days #type:ignore 
        return (date.today() - self.re_planting_date).days #type:ignore 
    
    @computed_field
    @property
    def days_since_fertilized(self) -> Optional[int]:
        if self.last_fertilized is None:
            return None
        return (date.today() - self.last_fertilized).days #type:ignore 
    
    
    
class WateringSchedule(BaseModel):
    plant: Plant
    frequency: Schedule = Schedule.DAILY
    amount: Optional[float] = None
    time_of_day: TimeOfDay = TimeOfDay.MORNING
    rain_detected: bool = False
    
    @field_validator("amount")
    @classmethod
    def validate_amount(cls, value):
        if value is None:
            return value
        elif value < 0:
            raise ValueError("Watering amount must be non-negative")
        return value
    
    @field_validator("frequency", 'time_of_day', mode="before")
    @classmethod
    def validate_enums(cls, value, info: ValidationInfo):
        enum_mapping = {
            "frequency": Schedule,
            "time_of_day": TimeOfDay,
        }
        if info.field_name not in enum_mapping:
            raise ValueError(f"Unknown field name: {info.field_name}")
        enum_class = enum_mapping[info.field_name]
        if value is None or str(value).upper() not in enum_class.__members__.keys():
            raise ValueError(f"Invalid {info.field_name}: {value}. Must be one of: {[e.value for e in enum_class]}")
        return value
    
    @computed_field
    @property
    def next_watering_date(self) -> Optional[date]:
        watering = self.plant.last_watered
        if watering is None:
            return date.today()
        if self.frequency == Schedule.DAILY:
            return watering + timedelta(days=1)
        if self.frequency == Schedule.TWICE:
            return watering + timedelta(days=3)
        if self.frequency == Schedule.WEEKLY:
            return watering + timedelta(days=7)
        if self.frequency == Schedule.BIWEEKLY:
            return watering + timedelta(days=14)
        if self.frequency == Schedule.MONTHLY:
            return watering + timedelta(days=30)
        
    
class Harvest(BaseModel):
    plant: Plant
    harvest_date: Optional[date] = None
    quantity: Optional[float] = None
    quality: Optional[HarvestQuality] = None
    notes: Optional[str] = None
    
    @field_validator("quality", mode="before")
    @classmethod
    def validate_enums(cls, value, info: ValidationInfo):
        enum_mapping = {
            "quality": HarvestQuality
        }
        if info.field_name not in enum_mapping:
            raise ValueError(f"Unknown field name: {info.field_name}")
        enum_class = enum_mapping[info.field_name]
        if value is None:
            return value
        if str(value).upper() not in enum_class.__members__.keys():
            raise ValueError(f"Invalid {info.field_name}: {value}. Must be one of: {[e.value for e in enum_class]}")
        return value
    

class Garden(BaseModel):
    name: str
    list_of_plants: List[Plant] = []
    fertilizer: Optional[Fertilizer] = None   
    watering_schedule: Optional[WateringSchedule] = None
    harvests: Optional[List[Harvest]] = None
    
    @computed_field
    @property
    def total_plants(self) -> int:
        return len(self.list_of_plants)
    


    
if __name__ == "__main__":
    
    garden_soil = Soil(soil_type=SoilType.KERAMZYT, drainage_type=DrainageType.KERAMZYT, moisture_level=MoistureLevel.MODERATE, ph_level=6.5)
    Betalux = Plant(common_name="Betalux", plant_family="Solanaceae", plant_type=PlantType.FRUIT, min_temperature=15, max_temperature=30, soil=garden_soil, planting_date=date(2026, 4, 23), growth_stage=GrowthStage.SEEDLING, last_watered=date(2026, 5, 30))
    Des_Andes = Plant(common_name="Des_Andes", plant_family="Solanaceae", plant_type=PlantType.FRUIT, min_temperature=15, max_temperature=30, soil=garden_soil, planting_date=date(2026, 4, 23), growth_stage=GrowthStage.SEEDLING, last_watered=date(2026, 5, 30))
    CaliforniaWonder= Plant(common_name="California Wonder", plant_family="Solanaceae", plant_type=PlantType.FRUIT, min_temperature=15, max_temperature=30, soil=garden_soil, planting_date=date(2026, 4, 23), growth_stage=GrowthStage.PLANTED, health_status=HealthStatus.UNKNOWN, last_watered=date(2026, 5, 30))
    CaliforniaWonder2= Plant(common_name="California Wonder", plant_family="Solanaceae", plant_type=PlantType.FRUIT, min_temperature=15, max_temperature=30, soil=garden_soil, planting_date=date(2026, 5, 30), growth_stage=GrowthStage.PLANTED, last_watered=date(2026, 5, 30))
    Basil_Black = Plant(common_name="Basil Black", plant_family="Lamiaceae", plant_type=PlantType.LEAVES, min_temperature=10, max_temperature=30, soil=garden_soil, planting_date=date(2026, 4, 23), growth_stage=GrowthStage.SEEDLING, last_watered=date(2026, 5, 30))
    Basil = Plant(common_name="Basil", plant_family="Lamiaceae", plant_type=PlantType.LEAVES, min_temperature=10, max_temperature=30, soil=garden_soil, planting_date=date(2026, 4, 23), growth_stage=GrowthStage.SEEDLING, last_watered=date(2026, 5, 30))
    Coriander = Plant(common_name='Coriander', plant_family="Apiaceae", plant_type=PlantType.LEAVES, min_temperature=10, max_temperature=30, soil=garden_soil, planting_date=date(2026, 5, 10), growth_stage=GrowthStage.SEEDLING, last_watered=date(2026, 5, 30))
    Mint = Plant(common_name='Mint', plant_family="Lamiaceae", plant_type=PlantType.LEAVES, min_temperature=10, max_temperature=30, soil=garden_soil, planting_date=date(2026, 4, 23), growth_stage=GrowthStage.SEEDLING, last_watered=date(2026, 5, 30))
    
    watering_fruits = WateringSchedule(plant=[Betalux, Des_Andes, CaliforniaWonder, CaliforniaWonder2], frequency=Schedule.TWICE, amount=0.05, time_of_day=TimeOfDay.MORNING)
    watering_leaves = WateringSchedule(plant=[Basil_Black, Basil, Coriander, Mint], frequency=Schedule.TWICE, amount=0.1, time_of_day=TimeOfDay.MORNING)
    
    
    garden_fruits = Garden(name = "My fruits", list_of_plants=[Betalux, Des_Andes, CaliforniaWonder, CaliforniaWonder2], watering_schedule=watering_fruits)
    garden_leaves = Garden(name = "My greens", list_of_plants=[Basil_Black, Basil, Coriander, Mint], watering_schedule=watering_leaves)
    
    print(Betalux.days_since_planted)
    print(Coriander.days_since_planted)
    
    print(watering_fruits.next_watering_date)
    print(watering_leaves.next_watering_date)
    
    for p in garden_fruits.list_of_plants + garden_leaves.list_of_plants:
        p.last_fertilized = date.today()
        p.last_watered = date.today()
    
    garden_json = garden_fruits.model_dump_json()
    
    garden_fruits_backup = Garden.model_validate_json(garden_json)
    
    