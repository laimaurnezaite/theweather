import json
import sqlite3


db = sqlite3.connect("theweather/db.sqlite3")

with open("city.list.json", "r") as json_file:
    data = json.load(json_file)
    for p in data:
        db.execute("INSERT INTO weather_city (name, geoname_id, state, country, lon, lat) VALUES (:name, :geoname_id, :state, :country, :lon, :lat);",
            {"name":p["name"], "geoname_id":p["id"], "state":p["state"], "country":p["country"], "lon":p["coord"]["lon"], "lat":p["coord"]["lat"]})
        db.commit()
    



