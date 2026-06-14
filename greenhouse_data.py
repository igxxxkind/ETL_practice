# .\greenhouse.venv\Scripts\Activate.ps1

from pydantic import BaseModel
from fastapi import FastAPI
from typing import Optional, List
from sqlmodel import Field, SQLModel, create_engine, Session, select

import pandas as pd
import numpy as np


# simple SQL table
class Fertilizer(SQLModel, table=True):
    id: int| None = Field(default=None, primary_key=True)
    name: str | None = None
    type: str | None = None
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
    
    print("Before interacting with DB")
    print(fert1)
    print(fert2)
    print(fert3) 
    
    # session = Session(engine)
    
    with Session(engine) as session:
        session.add(fert1)
        session.add(fert2)
        
        print("After adding to the DB")
        print("Fertilizer 1:",fert1)
        print("Fertilizer 2:",fert2)
        print("Fertilizer 3:",fert3) 

        session.commit()
        
        print("After commiting to the DB, show IDs")
        print("Fertilizer 1:",fert1.id)
        print("Fertilizer 2:",fert2.id)
        print("Fertilizer 3:",fert3.id)
        
        print("After commiting to the DB, show names")
        print("Fertilizer 1:",fert1.name)
        print("Fertilizer 2:",fert2.name)
        print("Fertilizer 3:",fert3.name) 
        
        session.refresh(fert1)
        session.refresh(fert2)
        # session.refresh(fert3)

        print("After refreshing the fertilizers")
        print("Fertilizer 1:", fert1)
        print("Fertilizer 2:", fert2)
        # print("Fertilizer 3:", fert3)
    print("After the session closes")
    print("Fertilizer 1:", fert1)
    print("Fertilizer 2:", fert2)
    print("Fertilizer 3:", fert3)
    # session.add(fert1) # git add fert1
    # session.add(fert2) # git add fert2
    # session.commit() # git commit
    # session.close() # git push

def select_fertilizers():
    with Session(engine) as session:
         fertilizers = session.exec(select(Fertilizer)).all()
         print(fertilizers)

def main():
    create_db_and_tables()
    create_fertilizers()
    select_fertilizers()

if __name__ == "__main__":
    
    main()
    
   
    