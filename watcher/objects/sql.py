from typing import Optional
from sqlmodel import SQLModel, Session, create_engine, Field


class SQLTrade(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    time: str
    buy_exchange: str
    buy_market: str
    buy_price: float
    buy_fee: float
    sell_exchange: str
    sell_market: str
    sell_price: float
    sell_fee: float
    profit: float

def write_hero_to_database(object: SQLTrade):
    engine = create_engine("sqlite:///database.db")
    SQLModel.metadata.create_all(engine)
    with Session(engine) as session:
        session.add(object)
        session.commit()