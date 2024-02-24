from sqlite3 import connect
from pathlib import Path

def setup() -> None:
    connection = connect("./air.db")
    cursor = connection.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS station(
            id INTEGER PRIMARY KEY,
            ip TEXT,
            position INTEGER
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS measurement(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            date TIMESTAMP,
            station INTEGER,
            temperature FLOAT,
            humidity FLOAT,
            location INTEGER
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS location(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT
        )
    ''')
    locations = ["Flur unten", "Flur oben", "Flur Gäste", "Bad unten", "Bad oben", "Bad Gäste", "Schlafzimmer Gäste", "Schlafzimmer Tim", "Schlafzimmer Niklas", "Schlafzimmer Mama / Papa", "Küche", "Wohnzimmer", "Treppenzimmer", "Arbeitszimmer"]
    for i in locations:
        add_location(i)
    stations = [(0, 4, "http://192.168.178.53")]
    for i in stations:
        add_station(i[0], i[1], i[2])

def add_station(id: int, position: int, ip: str) -> None:
    connection = connect("./air.db")
    cursor = connection.cursor()
    cursor.execute('''
        INSERT INTO station
        (id, position, ip)
        VALUES(?, ?, ?)
    ''',
    (id, position, ip)
    )
    connection.commit()

def update_position(old: str, new: str) -> None:
    connection = connect("./air.db")
    cursor = connection.cursor()
    cursor.execute('''
        UPDATE station
        SET position = ?
        WHERE id = ?
    ''',
    (get_location_id(new), get_station_from_position(old),))
    connection.commit()

def update_position(station: int, position: str)-> None:
    connection = connect("./air.db")
    cursor = connection.cursor()
    cursor.execute('''
        UPDATE station
        SET position = ?
        WHERE id = ?
    ''',
    (get_location_id(position), station,))
    connection.commit()

def get_location_id(name: str) -> int:
    connection = connect("./air.db")
    cursor = connection.cursor()
    cursor.execute('''
        SELECT id
        FROM location
        WHERE name = ?
    ''',
    (name,))
    return cursor.fetchone()[0]

def get_all_stations():
    connection = connect("./air.db")
    cursor = connection.cursor()
    cursor.execute('''
        SELECT id, ip
        FROM station
    ''')
    res = cursor.fetchall()
    out = []
    for i in res:
        out.append((i[0], i[1]))
    return out

def add_value(station: int, temperature: float, humidity: float) -> None:
    connection = connect("./air.db")
    cursor = connection.cursor()
    cursor.execute('''
        INSERT INTO measurement
        (station, location, temperature, humidity, date)
        VALUES(?, ?, ?, ?, datetime("now", "localtime"))
    ''',
    (station, get_location_from_station(station), temperature, humidity,))
    connection.commit()

def get_station_from_position(position: str) -> int:
    connection = connect("./air.db")
    cursor = connection.cursor()
    cursor.execute('''
        SELECT s.id
        FROM station s
        INNER JOIN location l ON l.id = s.position
        WHERE l.name = ?
    ''',
    (position,))
    return cursor.fetchone()[0]

def get_location_from_station(station: int) -> int:
    connection = connect("./air.db")
    cursor = connection.cursor()
    cursor.execute('''
        SELECT L.id
        FROM station S
        INNER JOIN location L ON L.id = s.position
        WHERE s.id = ?
    ''',
    (station,))
    return cursor.fetchone()[0]

def get_all_locations():
    connection = connect("./air.db")
    cursor = connection.cursor()
    cursor.execute('''
        SELECT DISTINCT id, name
        FROM location
    '''
    )
    out = cursor.fetchall()
    for i in range(len(out)):
        out[i] = (out[i][0], out[i][1])
    return out

def add_location(name: str) -> None:
    connection = connect("./air.db")
    cursor = connection.cursor()
    cursor.execute('''
        INSERT INTO location
        (name)
        VALUES(?)
    ''',
    (name,))
    connection.commit()

def get_values_from_position(position: int) -> list:
    connection = connect("./air.db")
    cursor = connection.cursor()
    cursor.execute('''
        SELECT m.temperature, m.humidity, m.date, m.station
        FROM measurement m
        WHERE location = ?
        ORDER BY date ASC
    ''',
    (position,)
    )
    res = list(cursor.fetchall())
    
    temps = {}
    hums = {}
    for i in res:
        temps[i[2]] = i[0]
        hums[i[2]] = i[1]
    data = [
        {'name': 'Temperature', 'data': temps, "color": "red", "suffix": "°C"},
        {'name': 'Humidity', 'data': hums, "color": "blue", "suffix": "%"},

    ]
    return data

if not Path("./air.db").is_file():
    print("database does not exist")
    print("starting to build db...")
    setup()
    print("db build finished")