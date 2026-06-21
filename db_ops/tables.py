
from sqlmodel import Field, SQLModel, create_engine, Session, select


import pandas as pd
import numpy as np

from greenhouse import FertilizerBase, NPKRatioBase, SoilBase, PlantBase, WateringScheduleBase, HarvestBase, GardenBase

# simple SQL data table Model for Fertilizer
class Fertilizer(FertilizerBase, table=True):
    id: int| None = Field(default=None, primary_key=True)
    npk_id: int| None = Field(default=None, foreign_key='npk_ratio.id')

class NPKRatio(NPKRatioBase, table=True):
    id: int| None = Field(default=None, primary_key=True)

class Soil(SoilBase, table=True):
    id: int| None = Field(default=None, primary_key=True)
    fertilizer_id: int| None = Field(default=None, foreign_key='fertilizer.id')

class Plant(greenhouse.PlantBase, table=True):
    id: int| None = Field(default=None, primary_key=True)
    soil_id: int| None = Field(default=None, foreign_key='soil.id')
    water_schedule_id: int| None = Field(default=None, foreign_key='watering_schedule.id')
    
class WateringSchedule(greenhouse.WateringScheduleBase, table=True):
    id: int| None = Field(default=None, primary_key=True)
    
class Harvest(greenhouse.HarvestBase, table=True):
    id: int| None = Field(default=None, primary_key=True)
    plant_id: int| None = Field(default=None, foreign_key='plant.id')

class Garden(greenhouse.GardenBase, table=True):
    id: int| None = Field(default=None, primary_key=True)
    plant_id: int| None = Field(default=None, foreign_key='plant.id')
    

sqlite_filename = "database.db"
sqlite_url = f'sqlite:///{sqlite_filename}'
engine = create_engine(sqlite_url, echo=True)

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

def main():
    create_db_and_tables()


if __name__ == "__main__":
    main()
