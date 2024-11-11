from flask import Flask, render_template
import pandas as pd
import numpy as np


app = Flask(__name__)


@app.route("/")
def home():
    return render_template("home.html")


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


if __name__ == "__main__":
    app.run(debug=True)