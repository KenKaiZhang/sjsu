import requests
import pandas as pd
import json

BASE_URL = "https://et.water.ca.gov/api"
API_KEY = "7d73896c-7595-4529-ad7d-6edbe50ffd0b"
DATA_ITEMS = {
    "DayAirTmpAvg": "day-air-tmp-avg",
    "DayPrecip": "day-precip",
    "DayRelHumAvg": "day-rel-hum-avg",
    "DaySoilTmpAvg": "day-soil-tmp-avg",
    "DayWindSpdAvg": "day-wind-spd-avg"
}
def get_weather_data(zip_codes, start, end):
    try:
        params = {
            "appKey": API_KEY,
            "targets": zip_codes,
            "startDate": start,
            "endDate": end,
            "dataItems": ",".join(DATA_ITEMS.values()),
            "unitOfMeasure": "M"
        }

        url = BASE_URL + "/data"
        headers = {"Accept": "application/json"}
        response = requests.get(url, headers=headers, params=params)

        print(response.url)
        response.raise_for_status()

        return response.json()

    except Exception as e:
        print(e)

def process_row(row):
    date = row["incident_dateonly_created"]
    zip_codes = stations_zip_dict.get(row["incident_county"], "") 

    if not zip_codes:
        return {item: None for item in DATA_ITEMS.keys()}
    
    weather_record_json = get_weather_data(zip_codes, date, date)
    if weather_record_json is None:
        weather_record_json = {}
    records = weather_record_json.get("Data", {}).get("Providers", [{}])[0].get("Records", None)

    if records is not None:
        record = records[0]
        results = {}
        for item in DATA_ITEMS.keys():
            value = record.get(item, {}).get("Value", None)
            results[item] = float(value) if value is not None else None
        return results
    
    return {item: None for item in DATA_ITEMS.keys()}


def get_station_zip_dict():
    url = f"{BASE_URL}/station"
    res = requests.get(url, headers={"content-type": "application/json"})
    res.raise_for_status()

    station_zip = {}
    for station in res.json()["Stations"]:
        station_zip[station["City"]] = ",".join(station["ZipCodes"])
    return station_zip


stations_zip_dict = get_station_zip_dict()

df = pd.read_csv("mapdataall.csv")
df_subset = df.iloc[:100]
weather_data = df_subset.apply(process_row, axis=1, result_type="expand")
df_updated = pd.concat([df_subset, weather_data], axis=1)
print(df_updated.head())
df_updated.to_csv("mapdataall_with_weather.csv", index=False)