import pandas as pd 
from prophet import Prophet 
from database import engine

def compute_future_power_consumption(username: str):
    with engine.connect() as conn, conn.begin():
        data = pd.read_sql_table('data', conn)
        data = data[data.username == 'Saverio']
        prophet_df = data.loc[:, ['timestamp', 'power_consumption']]

    m = Prophet()
    m.fit(prophet_df.rename(columns={'timestamp': 'ds', 'power_consumption': 'y'}))

    future = m.make_future_dataframe(periods=365)

    forecast = m.predict(future)
    dict_keys = [data for data in (forecast[['ds', 'yhat']].to_dict())['ds'].values()]
    dict_values = [data for data in (forecast[['ds', 'yhat']].to_dict())['yhat'].values()]
    
    return {key: value for key, value in zip(dict_keys, dict_values)}