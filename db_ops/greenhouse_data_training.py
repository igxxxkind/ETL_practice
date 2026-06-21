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
        
def update_fertilizers():
    with Session(engine) as session:
        statement = select(Fertilizer).where(Fertilizer.name == 'PermaBloom')
        fertilizer = session.exec(statement)
        object = fertilizer.one()
        print("Initial:", object)
        object.application_frequency = 'Once a month'
        session.add(object)
        session.commit()
        session.refresh(object)
        print("Updated:", object)

def delete_fertilizers():
    with Session(engine) as session:
        statement = select(Fertilizer).where(Fertilizer.name=='HydroponicNutrient')
        fertilizer = session.exec(statement)
        object = fertilizer.first()
        
        session.delete(object)
        session.commit()
        # check the record is deleted
        statement = select(Fertilizer).where(Fertilizer.name=='HydroponicNutrient')
        fertilizer = session.exec(statement)
        object = fertilizer.first()
        print(object)
        
        if object is None:
            print("There's no Hydroponic Nutritient")
            

    

def main():
    create_db_and_tables()
    # create_fertilizers()
    select_fertilizers()
    update_fertilizers()
    delete_fertilizers()

if __name__ == "__main__":
 # 1. SQLModel and BaseModel are essentially the same until the table initialized.
 # 2. When SQLModel object is initiated with a table flag, it is not a safe BaseModel object anymore
 # 3. A BaseModel class can be turned to SQLModel and create a corresponding table.
 # 4. for any table the changes need to be added, commited and refreshed.
 # 5. A table we get with SQLModel object should not contain any complex/custom-made classes as it is impossible to put them into the relational database. It should contain only basic datatypes and link to a differnt table. That is how we ensure a link between BaseModel classes.
 # 6. So it is impossible to create a business logic using SQLModel table objects. We need to create a separate BaseModel class for business logic and use the SQLModel table objects only for database operations.
    
    main()
    
   
    