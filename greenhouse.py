from pydantic import BaseModel, Field, field_validator, model_validator, computed_field
from datetime import date, timedelta
from typing import Optional, Dict, List, Union
from enum import Enum


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
    PERLITE = "Perlite"
    OTHER = "Other"
    
class Schedule(str, Enum):
    DAILY = "Daily"
    TWICE = "Twice a Week"
    WEEKLY = "Weekly"
    MONTHLY = "Monthly"
    
class TimeOfDay(str, Enum):
    MORNING = "Morning"
    AFTERNOON = "Afternoon"
    EVENING = "Evening"

class NPKRatio(BaseModel):
    n: Optional[float] = None
    p: Optional[float] = None
    k: Optional[float] = None
    
    @field_validator("n", "p", "k")
    @classmethod
    def validate_npk(cls, value):
        if value is None:
            return value
        elif value < 0:
            raise ValueError("NPK values must be non-negative")
        return value

class Fertilizer(BaseModel):
    name: Optional[str] = None
    type: Optional[str] = None
    NPK_ratio: Optional[NPKRatio] = None
    application_method: Optional[str] = None
    application_frequency: Optional[Schedule] = None
    
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
    plant_type: PlantType
    min_temperature: float
    max_temperature: float
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
        if self.min_temperature >= self.max_temperature:
            raise ValueError("Minimum temperature must be less than maximum temperature")
        if self.planting_date is None:
            return self
        if self.re_planting_date is None:
            return self      
        if self.re_planting_date < self.planting_date:
            raise ValueError("Re-planting date cannot be before planting date") 
        return self

    @field_validator("min_temperature", "max_temperature")
    @classmethod
    def positive_temperature(cls, value):
        if value < -5:
            raise ValueError("Temperature must be positive")
        return value
    
    @computed_field
    @property
    def days_since_watered(self) -> Optional[int]:
        if self.last_watered is not None:
            delta = date.today() - self.last_watered
            return delta.days
        else:
            return None
    
    @computed_field
    @property
    def days_since_planted(self) -> Optional[int]:
        if self.planting_date is None:
            return None
        if self.re_planting_date is None:
            return (date.today() - self.planting_date).days
        return (date.today() - self.re_planting_date).days
    
    @computed_field
    @property
    def days_since_fertilized(self) -> Optional[int]:
        if self.last_fertilized is None:
            return None
        return (date.today() - self.last_fertilized).days
    
    
    
class WateringSchedule(BaseModel):
    plant: Union[Plant, List[Plant]]
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
    
    @computed_field
    @property
    def next_watering_date(self) -> Optional[date]:
        
        watering = [item.last_watered for item in self.plant] if isinstance(self.plant, list) else [self.plant.last_watered]
        watering = [w for w in watering if w is not None]
        watering = min(watering) if watering else None
        if watering is None:
            return date.today()
        if self.frequency == Schedule.DAILY:
            return watering + timedelta(days=1)
        if self.frequency == Schedule.TWICE:
            return watering + timedelta(days=3)
        if self.frequency == Schedule.WEEKLY:
            return watering + timedelta(days=7)
        if self.frequency == Schedule.MONTHLY:
            return watering + timedelta(days=30)
        
    
class Harvest(BaseModel):
    plant: Plant
    harvest_date: Optional[date] = None
    quantity: Optional[float] = None
    quality: Optional[HarvestQuality] = None
    notes: Optional[str] = None
    

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
    
    