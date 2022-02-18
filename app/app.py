import time
import random
import json
from sqlalchemy import create_engine
import pandas as pd
from haversine import haversine, Unit
from flask import Flask
from datetime import datetime
from ast import literal_eval


# Waiting for SQL database to spool up before trying to interact with it
time.sleep(5)
app = Flask(__name__)
app.config["DEBUG"] = False

db_name = 'starlink'
db_user = 'pguser'
db_pass = 'postgres1234'
db_host = 'db'
db_port = '5432'

# Connecto to the database
db_string = 'postgresql://{}:{}@{}:{}/{}'.format(
    db_user, db_pass, db_host, db_port, db_name)
db = create_engine(db_string)
conn = db.connect()


def flatten_json(y):
    out = {}

    def flatten(x, name=''):
        if type(x) is dict:

            for a in x:
                flatten(x[a], name + a + '_')
        elif type(x) is list:

            i = 0

            for a in x:
                flatten(a, name + str(i) + '_')
                i += 1
        else:
            out[name[:-1]] = x

    flatten(y)
    return out


def read_json():
    with open('./data/starlink_historical_data.json', 'r') as f:
        starlink_data = json.load(f)
    flattened_data = []
    for i in starlink_data:
        flattened_data.append(flatten_json(i))
    return flattened_data


def load_data(data):
    col_list = ['spaceTrack_CREATION_DATE', 'longitude', 'latitude', 'id']
    df = pd.DataFrame(data)
    df = df[col_list].sort_values(col_list[0])
    df = df.rename(columns={f"{col_list[0]}": "creation_date"})
    df['creation_date'] = df['creation_date'].str.replace('T', ' ')

    return df


@app.route('/')
def test():
    df = pd.read_sql_query('select * from satellites;', con=db)
    return df.columns.values


@app.route('/satellite/<id>')
def get_position(id, dt=str(datetime.now())):
    """
    Get position of satellite at specific time
    """
    df = pd.read_sql_query('select * from satellites;', con=db)
    df = df[df["creation_date"] < dt]
    df = df.dropna(how='any', axis=0)
    if len(df.values) != 0:
        df = df[df["id"] == f"{id}"]
        df = df[df["creation_date"] == max(df["creation_date"])]
        return({"ID": df.values[0][3], "POSITION": {"LAT": df.values[0][2], "LON": df.values[0][1]}})
    else:
        return("No satellites found\n")


@app.route('/satellite/<id>/<dt>')
def get_rel_position(id, dt):
    return get_position(id, str(dt))


@app.route('/position/<location>')
def get_closest_sat(location, dt=str(datetime.now())):
    """
    Get closest satellite to specific location (lat,lon) at specific time
    """
    df = pd.read_sql_query('select * from satellites;', con=db)
    df = df[df["creation_date"] < dt]
    df = df.dropna(how='any', axis=0)
    if len(df.values) != 0:
        location = literal_eval(location)
        df['haversine'] = 'NaN'
        df['haversine'] = df.apply(lambda x: haversine(
            location, (x['latitude'], x['longitude'])), axis=1)
        df = df[df['haversine'] == min(df['haversine'])]
        return({"ID": df.values[0][3], "POSITION": {"LAT": df.values[0][2], "LON": df.values[0][1]}})
    else:
        return("No satellites found\n")


@ app.route('/position/<location>/<dt>')
def get_rel_closest_sat(location, dt):
    return get_closest_sat(location, dt)


if __name__ == '__main__':
    print('Application started')
    flat_json = read_json()
    df = load_data(flat_json)
    df.to_sql('satellites', conn, if_exists='replace', index=False)
    app.run(debug=True, host="0.0.0.0", port=3333)
