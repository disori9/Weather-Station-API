from flask import Flask, render_template
import pandas as pd
import numpy as np


app = Flask(__name__)
stations_df = pd.read_csv('data_small/stations.txt', skiprows=17)

@app.route("/")
def home():
    stations_table_df = stations_df[['STAID', 'STANAME                                 ']]
    stations_table_html = stations_table_df.to_html()

    return render_template("home.html", stations=stations_table_html)


@app.route("/api/v1/<station>/<date>")
def temp(station, date):
    filename = f"data_small/TG_STAID{str(station).zfill(6)}.txt"
    temperature_df = pd.read_csv(filename, skiprows=20, parse_dates=["    DATE"])
    temperature_df["TG0"] = temperature_df['   TG'].mask(temperature_df['   TG'] == -9999, np.nan)
    temperature_df["TG"] = temperature_df["TG0"] / 10
    date_temp = temperature_df.loc[temperature_df['    DATE'] == date]['TG'].squeeze()
    return {"station": station,
            "date": date,
            "temperature": date_temp}

@app.route("/api/v1/<station>/")
def all_data(station):
    filename = f"data_small/TG_STAID{str(station).zfill(6)}.txt"
    temperature_df = pd.read_csv(filename, skiprows=20, parse_dates=["    DATE"])
    temperature_df["TG0"] = temperature_df['   TG'].mask(temperature_df['   TG'] == -9999, np.nan)
    temperature_df["TG"] = temperature_df["TG0"] / 10
    results = temperature_df.to_dict(orient="records")
    return results

@app.route("/api/v1/year_data/<station>/<year>")
def year_data(station, year):
    filename = f"data_small/TG_STAID{str(station).zfill(6)}.txt"
    str_yr = str(year)
    temperature_df = pd.read_csv(filename, skiprows=20)
    temperature_df["    DATE"] = temperature_df["    DATE"].astype(str)
    temperature_df["TG0"] = temperature_df['   TG'].mask(temperature_df['   TG'] == -9999, np.nan)
    temperature_df["TG"] = temperature_df["TG0"] / 10
    result = temperature_df[temperature_df["    DATE"].str.startswith(str_yr)]
    return result.to_dict(orient="records")

if __name__ == "__main__":
    app.run(debug=True)