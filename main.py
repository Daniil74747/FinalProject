import requests
from bs4 import BeautifulSoup
import logging
import sqlite3

siteDate = requests.get('https://ua.sinoptik.ua/')
soup = BeautifulSoup(siteDate.text, features='html.parser')

date = soup.find_all(name='p', attrs={'class': 'date'})
temperature = soup.find_all(name='div', attrs={'class': 'temperature'})
for rate1 in date:
    print(rate1.text)
for rate2 in temperature:
    print(rate2.text)

conn = sqlite3.connect('weather.db')
c = conn.cursor()
c.execute('''CREATE TABLE IF NOT EXISTS weather(date, temperature, precipitation, wind_speed, wind_direction)''')

temperature = soup.find(name='tr', class_='temperature').text
date_time = soup.find(name='tr', class_='gray time').text

c.execute("INSERT INTO weather (date, temperature, precipitation, wind_speed, wind_direction)"
          " VALUES (3, '+21', 'No', '7', 'NW')")
weather = (4, '+21', 'No', '9', 'NW')
c.execute("INSERT INTO weather (date, temperature, precipitation, wind_speed, wind_direction) "
          "VALUES (?, ?, ?, ?, ?)", weather)

weathers = [(5, '+20', 'No', '9', 'SW'), (6, '+22', 'No', '9', 'SW')]
c.executemany("INSERT INTO weather (date, temperature, precipitation, wind_speed, wind_direction) VALUES "
              "(?, ?, ?, ?, ?)", weathers)


conn.commit()
conn.close()

def select_weather_data(condition):
    conn = sqlite3.connect('weather.db')
    c = conn.cursor()
    c.execute(condition)
    data = c.fetchall()
    conn.close()
    return data

data_by_date = select_weather_data("SELECT * FROM weather WHERE date = '03'")
print(data_by_date)

data_by_min_temp = select_weather_data("SELECT * FROM weather ORDER BY temperature ASC LIMIT 1")
print(data_by_min_temp)

data_by_max_temp = select_weather_data("SELECT * FROM weather ORDER BY temperature DESC LIMIT 1")
print(data_by_max_temp)

class DateWeather:
    def __init__(self, date, temperature, precipitation, wind_speed, wind_direction):
        self.date = date
        self.temperature = temperature
        self.precipitation = precipitation
        self.wind_speed = wind_speed
        self.wind_direction = wind_direction

data_by_date = select_weather_data("SELECT * FROM weather WHERE date = '03'")
if data_by_date:
    date_weather_obj = DateWeather(*data_by_date[0])
    print(date_weather_obj.date)
    print(date_weather_obj.temperature)
    print(date_weather_obj.precipitation)
    print(date_weather_obj.wind_speed)
    print(date_weather_obj.wind_direction)
else:
    print("There are no data for the specified date")

try:
    conn = sqlite3.connect('weather_data.db')
    logging.info("Connected to SQLite database")
except sqlite3.Error as error:
    logging.error(f"Error connecting to SQLite database: {error}")

try:
    logging.info("Weather table created successfully")
except sqlite3.Error as error:
    logging.error(f"Error creating weather table: {error}")

try:
    connection, data = 5, +20
    logging.info("Weather data inserted successfully")
except sqlite3.Error as error:
    logging.error(f"Error inserting weather data: {error}")

try:
    selected_data = conn, "date = '31'"
    logging.info("Weather data selected successfully")
except sqlite3.Error as error:
    logging.error(f"Error selecting weather data: {error}")

conn.close()
