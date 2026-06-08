# Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
# .\greenhouse.venv\Scripts\Activate.ps1

import pydantic
from fastapi import FastAPI
from typing import Optional, List
from sqlmodel import Field, SQLModel, create_engine, Session, select

import pandas as pd
import numpy as np


# simple SQL table
class Hero(SQLModel, table=True):
    id: int| None = Field(default=None, primary_key=True)
    name: str
    secret_name: str
    age: int | None = None
    
if __name__ == "__main__":

    hero_1 = Hero(name = 'DeadPull', secret_name='Wade Wilson')
    hero_2 = Hero(name = 'Batman', secret_name = "Bruce Wayne")
    hero_3 = Hero(name = 'Witcher', secret_name= 'Geralt of Rivia')

    engine = create_engine("sqlite:///database.db")

    SQLModel.metadata.create_all(engine)

    with Session(engine) as session:
        session.add(hero_1)
        session.add(hero_2)
        session.add(hero_3)
        session.commit()

    with Session(engine) as session:
        statement = select(Hero).where(Hero.name == "Witcher")
        hero = session.exec(statement).first()
        print(hero)

    ######################

    user_id = input("Type the user ID:")

    session.exec(
        select(Hero).where(Hero.id==user_id)
    ).all()

    session.exec(
        select(Hero).where(Hero.secret_name=='Bruce Wayne')
    ).all()
