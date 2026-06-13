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
# 
    # session = Session(engine)
    
    with Session(engine) as session:
        session.add(fert1)
        session.add(fert2)
        session.commit()
    
    # session.add(fert1) # git add fert1
    # session.add(fert2) # git add fert2
    # session.commit() # git commit
    # session.close() # git push

def main():
    create_db_and_tables()
    create_fertilizers()

if __name__ == "__main__":
    
    main()