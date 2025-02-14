from sqlalchemy import *
from sqlalchemy.orm import *
import datetime
from sqlalchemy import select 
from operator import itemgetter

engine = create_engine("sqlite:///database.sqlite", echo=True)

Session = sessionmaker(engine)

class Base(DeclarativeBase):
    pass

class Data(Base):
    __tablename__ = 'data'

    timestamp: Mapped[datetime.datetime] = mapped_column(primary_key=True)
    username: Mapped[str]
    duration: Mapped[float]
    on_mode: Mapped[str]
    off_mode: Mapped[str]
    color: Mapped[str]
    light_intensity: Mapped[str]
    power_consumption: Mapped[float]

    def __init__(self, timestamp: str, username: str, duration: float, on_mode: str, off_mode: str, color: str, light_intensity: str, power_consumption: float):
        self.timestamp = datetime.datetime.strptime(timestamp, '%Y-%m-%d %H:%M:%S.%f')
        self.username = str(username)
        self.duration = float(duration)
        self.on_mode = str(on_mode)
        self.off_mode = str(off_mode)
        self.color = str(color)
        self.light_intensity = str(light_intensity)
        self.power_consumption = float(power_consumption)

class State(Base):
    __tablename__ = 'current state'

    timestamp: Mapped[datetime.datetime] = mapped_column(primary_key=True)
    room: Mapped[str]
    color: Mapped[str]
    light_intensity: Mapped[str]
    people_in_the_room: Mapped[int]

    def __init__(self, timestamp: str, room: str, color: str, light_intensity: str, people_in_the_room: int):
        self.timestamp = datetime.datetime.strptime(timestamp, '%Y-%m-%d %H:%M:%S.%f')
        self.room = str(room)
        self.color = str(color)
        self.light_intensity = str(light_intensity)
        self.people_in_the_room = int(people_in_the_room)



def create_db():
    Base.metadata.create_all(engine)


def compute_rankings(user: bool):
    with Session() as session:
        users_consumptions_tuples = session.execute(select(Data.username, func.sum(Data.power_consumption)).group_by(Data.username)).all()
        users_consumptions_dict = {data[0] : data[1] for data in users_consumptions_tuples}
        value = users_consumptions_dict['Saverio']
        users_consumptions_dict_list = [{'name': key, 'power_used':value} for key, value in users_consumptions_dict.items()]
        users_consumptions_dict_list_ordered = sorted(users_consumptions_dict_list, key=itemgetter('power_used'))
        index = users_consumptions_dict_list_ordered.index({'name': 'Saverio', 'power_used': value})
        return index + 1, users_consumptions_dict_list_ordered[index] if user is True else users_consumptions_dict_list_ordered

def add_row(db_row): #TODO
    if isinstance(db_row, Data):
        pass 
    else:
        pass

def compute_past_power_consumption(username: str):
    with Session() as session:
        past_power_consumption_tuples = session.execute(select(Data.timestamp, Data.power_consumption).filter(Data.username == username)).all()
        past_power_consumption_dict = {data[0] : data[1] for data in past_power_consumption_tuples}
        
        return past_power_consumption_dict

def compute_colors_usage(username: str):
    with Session() as session:
        colors_usage = {}
        colors_usage['White'] = session.scalar(select(func.count(Data.timestamp)).filter(Data.color == 'white').filter(Data.username == username))
        colors_usage['Red'] = session.scalar(select(func.count(Data.timestamp)).filter(Data.color == 'red').filter(Data.username == username))
        colors_usage['Green'] = session.scalar(select(func.count(Data.timestamp)).filter(Data.color == 'green').filter(Data.username == username))
        colors_usage['Blue'] = session.scalar(select(func.count(Data.timestamp)).filter(Data.color == 'blue').filter(Data.username == username))
        colors_usage['Yellow'] = session.scalar(select(func.count(Data.timestamp)).filter(Data.color == 'yellow').filter(Data.username == username))
        colors_usage['Pink'] = session.scalar(select(func.count(Data.timestamp)).filter(Data.color == 'pink').filter(Data.username == username))
        colors_usage['Purple'] = session.scalar(select(func.count(Data.timestamp)).filter(Data.color == 'purple').filter(Data.username == username))
        colors_usage['Orange'] = session.scalar(select(func.count(Data.timestamp)).filter(Data.color == 'orange').filter(Data.username == username))
        colors_usage = {key : value for key, value in colors_usage.items() if value > 0}
        return colors_usage

def compute_light_usage_methods(username: str):
    with Session() as session:
        light_usage_methods = {}
        light_usage_methods['Auto'] = session.scalar(select(func.count(Data.timestamp)).filter(Data.on_mode == 'auto').filter(Data.username == username))
        light_usage_methods['Switch'] = session.scalar(select(func.count(Data.timestamp)).filter(Data.on_mode == 'switch').filter(Data.username == username))
        light_usage_methods['Voice'] = session.scalar(select(func.count(Data.timestamp)).filter(Data.on_mode == 'voice').filter(Data.username == username))
        light_usage_methods['Mobile App'] = session.scalar(select(func.count(Data.timestamp)).filter(Data.on_mode == 'mobile app').filter(Data.username == username))
        light_usage_methods = {key : value for key, value in light_usage_methods.items() if value > 0}
        return light_usage_methods