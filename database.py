from sqlalchemy import *
from sqlalchemy.orm import *
import datetime
from sqlalchemy import select 

engine = create_engine("sqlite:///database.sqlite", echo=True)

Session = sessionmaker(engine)

class Base(DeclarativeBase):
    pass

class Data(Base):
    __tablename__ = 'data'

    timestamp: Mapped[datetime.datetime] = mapped_column(primary_key=True)
    duration: Mapped[float]
    on_mode: Mapped[str]
    off_mode: Mapped[str]
    color: Mapped[str]
    color_mode: Mapped[str]
    light_intensity: Mapped[int]
    power_consumption: Mapped[float]

def create_db():
    Base.metadata.create_all(engine)


def populate_db():
    pass 

def add_data():
    pass

def compute_past_power_consumption():
    with Session() as session:
        past_power_consumption_tuples = session.execute(select(Data.timestamp, Data.power_consumption)).all()
        past_power_consumption_dict = {data[0] : data[1] for data in past_power_consumption_tuples}
        return past_power_consumption_dict

def compute_colors_usage():
    with Session() as session:
        colors_usage = {}
        colors_usage['White'] = session.scalar(select(func.count(Data.timestamp)).filter(Data.color == 'white'))
        colors_usage['Red'] = session.scalar(select(func.count(Data.timestamp)).filter(Data.color == 'red'))
        colors_usage['Green'] = session.scalar(select(func.count(Data.timestamp)).filter(Data.color == 'green'))
        colors_usage['Blue'] = session.scalar(select(func.count(Data.timestamp)).filter(Data.color == 'blue'))
        colors_usage['Yellow'] = session.scalar(select(func.count(Data.timestamp)).filter(Data.color == 'yellow'))
        colors_usage['Pink'] = session.scalar(select(func.count(Data.timestamp)).filter(Data.color == 'pink'))
        colors_usage['Purple'] = session.scalar(select(func.count(Data.timestamp)).filter(Data.color == 'purple'))
        colors_usage['Orange'] = session.scalar(select(func.count(Data.timestamp)).filter(Data.color == 'orange'))
        colors_usage = {key : value for key, value in colors_usage.items() if value > 0}
        return colors_usage

def compute_light_usage_methods():
    with Session() as session:
        light_usage_methods = {}
        light_usage_methods['Auto'] = session.scalar(select(func.count(Data.timestamp)).filter(Data.on_mode == 'auto'))
        light_usage_methods['Switch'] = session.scalar(select(func.count(Data.timestamp)).filter(Data.on_mode == 'switch'))
        light_usage_methods['Voice'] = session.scalar(select(func.count(Data.timestamp)).filter(Data.on_mode == 'voice'))
        light_usage_methods['Mobile App'] = session.scalar(select(func.count(Data.timestamp)).filter(Data.on_mode == 'user'))
        light_usage_methods = {key : value for key, value in light_usage_methods.items() if value > 0}
        return light_usage_methods

        


def main():
    #create_db()
    #print(compute_past_power_consumption())
    print(compute_colors_usage())

main()