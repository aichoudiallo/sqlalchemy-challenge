import numpy as np
import pandas as pd
import datetime as dt

# Python SQL toolkit and Object Relational Mapper
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify

# create engine to hawaii.sqlite
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()

# reflect the tables
Base.prepare(engine, reflect=True)


# Save references to each table
Measurement = Base.classes.measurement
Station = Base.classes.station


# Create our session (link) from Python to the DB
session = Session(engine)


app= Flask(__name__)
@app.route("/")

def welcome():
    return(f"Welcome to the Hawaii Climate Analysis API!<br/>"
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/temp/start<br/>"
        f"/api/v1.0/temp/start/end<br/>"
        f"<p>'start' and 'end' date should be in the format MMDDYYYY.</p>"
)

@app.route("/api/v1.0/precipitation")

@app.route("/api/v1.0/stations")
def stations():
    result=session.query(Station.station).all()
    session.close()

    stations = list(np.ravel(result))
    return jsonify(stations=stations)





@app.route("/api/v1.0/temp/<start>")
@app.route("/api/v1.0/temp/<start>/<end>")
def statistics(start=None,end=None):
    sel=[func.min(Measurement.tobs),func.avg(Measurement.tobs), func.max(Measurement.tobs)]

    if not end:
        result=session.query(*sel).filter(Measurement.date>=start).all()

        session.close()

        temps = list(np.ravel(result))
        return jsonify(temps)

    result=session.query(*sel).filter(Measurement.date>=start).filter(Measurement.date<=end).all()

    session.close()

    temps = list(np.ravel(result))
    return jsonify(temps)












if __name__=="__main__":
    app.run()
