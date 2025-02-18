from sqlalchemy import *
from sqlalchemy.orm import *
from sqlalchemy import select 
from operator import itemgetter
import random
from datetime import datetime, timedelta

engine = create_engine("sqlite:///database.sqlite", echo=True)

Session = sessionmaker(engine)

class Base(DeclarativeBase):
    pass

class Data(Base):
    __tablename__ = 'data'

    timestamp: Mapped[datetime] = mapped_column(primary_key=True)
    username: Mapped[str]
    room: Mapped[str]
    duration: Mapped[float]
    on_mode: Mapped[str]
    off_mode: Mapped[str]
    color: Mapped[str]
    light_intensity: Mapped[str]
    power_consumption: Mapped[float]

    def __init__(self, timestamp: str, username: str, room: str, duration: float, on_mode: str, off_mode: str, color: str, light_intensity: str, power_consumption: float):
        self.timestamp = datetime.strptime(timestamp, '%Y-%m-%d %H:%M:%S.%f')
        self.username = str(username)
        self.room = str(room)
        self.duration = float(duration)
        self.on_mode = str(on_mode)
        self.off_mode = str(off_mode)
        self.color = str(color)
        self.light_intensity = str(light_intensity)
        self.power_consumption = float(power_consumption)

class State(Base):
    __tablename__ = 'current_state'

    timestamp: Mapped[datetime] = mapped_column(primary_key=True)
    username: Mapped[str]
    room: Mapped[str]
    color: Mapped[str]
    light_intensity: Mapped[str]
    people_in_the_room: Mapped[int]
    auto_mode: Mapped[str]

    def __init__(self, timestamp: str, username: str, room: str, color: str, light_intensity: str, people_in_the_room: int, auto_mode: str):
        self.timestamp = datetime.strptime(timestamp, '%Y-%m-%d %H:%M:%S.%f')
        self.username = str(username)
        self.room = str(room)
        self.color = str(color)
        self.light_intensity = str(light_intensity)
        self.people_in_the_room = int(people_in_the_room)
        self.auto_mode = str(auto_mode)



def create_db():
    Base.metadata.create_all(engine)

def populate_db():
    with Session() as session:
        for i in range(1000):
            price = 0.15
            timestamp = str(gen_datetime())
            username = random.choice(['Cristina', 'Roberta', 'Matteo', 'Giada', 'Eleonora', 'Sabrina', 'Alice', 'Franco', 'Filippo', 'Silvio', 'Teresa', 'Saverio'])
            room = random.choice(['Living Room', 'Bathroom', 'Bedroom', 'Kitchen'])
            duration = random.randint(1, 100)
            on_mode = random.choice(['auto', 'switch', 'voice', 'mobile app'])
            off_mode = random.choice(['auto', 'switch', 'voice', 'mobile app'])
            color = random.choice(['white', 'red', 'green', 'blue', 'yellow', 'pink', 'purple', 'orange'])
            light_intensity = random.choice(['low', 'medium', 'high'])
            power_consumption = price * duration 

            data = Data(timestamp, username, room, duration, on_mode, off_mode, color, light_intensity, power_consumption)
            session.add(data)

        session.commit()



def compute_rankings(user: bool):
    with Session() as session:
        users_consumptions_tuples = session.execute(select(Data.username, func.sum(Data.power_consumption)).group_by(Data.username)).all()
        users_consumptions_dict = {data[0] : data[1] for data in users_consumptions_tuples}
        value = users_consumptions_dict['Saverio']
        users_consumptions_dict_list = [{'name': key, 'power_used':value} for key, value in users_consumptions_dict.items()]
        users_consumptions_dict_list_ordered = sorted(users_consumptions_dict_list, key=itemgetter('power_used'))
        index = users_consumptions_dict_list_ordered.index({'name': 'Saverio', 'power_used': value})
        return index + 1, users_consumptions_dict_list_ordered[index] if user is True else users_consumptions_dict_list_ordered

def add_row(db_row): 
    if isinstance(db_row, Data):
        with Session() as session:
            session.add(db_row)
            session.commit() 
    elif isinstance(db_row, State):
        with Session() as session:
            state = session.execute(select(State).filter_by(room='Living Room')).scalar_one()
            state.timestamp = db_row.timestamp
            state.color = db_row.color 
            state.light_intensity = db_row.light_intensity
            state.people_in_the_room = db_row.people_in_the_room
            state.auto_mode = db_row.auto_mode
            session.commit()


def compute_past_power_consumption(username: str):
    with Session() as session:
        past_power_consumption_tuples = session.execute(select(Data.timestamp, Data.power_consumption).filter(Data.username == username)).all()
        past_power_consumption_dict = {data[0] : data[1] for data in past_power_consumption_tuples}
        
        return dict(sorted(past_power_consumption_dict.items()))

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

def get_current_state():
    with Session() as session:
        state = {}
        current_state = session.execute(select(State)).scalar_one()
        state['timestamp'] = current_state.timestamp
        state['room'] = current_state.room
        state['color'] = current_state.color 
        state['light intensity'] = current_state.light_intensity
        state['people in the room'] = current_state.people_in_the_room 
        state['auto mode'] = current_state.auto_mode
        return state 


def gen_datetime(min_year=2015, max_year=datetime.now().year-1):
    # generate a datetime in format yyyy-mm-dd hh:mm:ss.000000
    start = datetime(min_year, 1, 1, 00, 00, 00)
    years = max_year - min_year + 1
    end = start + timedelta(days=365 * years)
    return start + (end - start) * random.random()

#create_db()

#populate_db()
