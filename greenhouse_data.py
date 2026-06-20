# .\greenhouse.venv\Scripts\Activate.ps1

from pydantic import BaseModel
from fastapi import FastAPI
from typing import Optional, List
from sqlmodel import Field, SQLModel, create_engine, Session, select

import pandas as pd
import numpy as np


# simple SQL data table Model for Fertilizer
class Fertilizer(SQLModel, table=True):
    id: int| None = Field(default=None, primary_key=True)
    name: str | None = Field(index=True)
    type: str | None = Field(default=None, index=True)
    NPK_ratio: str | None = None
    application_method: str | None = None
    application_frequency: str | None = None


sqlite_filename = "database.db"
sqlite_url = f'sqlite:///{sqlite_filename}'
engine = create_engine(sqlite_url, echo=True)

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

def  create_fertilizers():
    fert1 = Fertilizer(name="Azofoska", type = "Liquid", NPK_ratio = "10-5.5-8", application_method = "Fertigation", application_frequency = "Twice a month")
    fert2 = Fertilizer(name="PermaBloom", type = "Liquid", NPK_ratio = "1-2-5", application_method = "Fertigation", application_frequency = "Twice a month")
    fert3 = Fertilizer(name="GreenGro", type = "Granular", NPK_ratio = "5-10-5", application_method = "Top dressing", application_frequency = "Once a month")
    fert4 = Fertilizer(name="SuperGrow", type = "Granular", NPK_ratio = "20-10-10", application_method = "Top dressing", application_frequency = "Once a month")
    fert5 = Fertilizer(name="OrganicManure", type = "Solid", NPK_ratio = "2-3-2", application_method = "Broadcasting", application_frequency = "Once a month")
    fert6 = Fertilizer(name="HydroponicNutrient", type = "Liquid", NPK_ratio = "20-10-20", application_method = "Drip Irrigation", application_frequency = "Daily")

    # session = Session(engine)
    
    with Session(engine) as session:
        session.add(fert1)
        session.add(fert2)
        session.add(fert3)
        session.add(fert4)
        session.add(fert5)
        session.add(fert6)

        session.commit()
        
        session.refresh(fert1)
        session.refresh(fert2)
        session.refresh(fert3)
        session.refresh(fert4)
        session.refresh(fert5)
        session.refresh(fert6)


def select_fertilizers():
    with Session(engine) as session:
        #  statement = select(Fertilizer).where(Fertilizer.type=='Liquid')
        statement = select(Fertilizer).where(Fertilizer.type!='Liquid').offset(2).limit(2)
        fertilizers = session.exec(statement) #SELECT * from fertilizers # and execute it
        object = fertilizers.all()
        print(object)

def main():
    create_db_and_tables()
    # create_fertilizers()
    select_fertilizers()

if __name__ == "__main__":
    
    main()
    
   
    