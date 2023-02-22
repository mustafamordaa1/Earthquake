from flask import Flask, render_template, request
import requests
import json
import xmltodict
from matplotlib.figure import Figure
from datetime import datetime
from datetime import date
from datetime import timedelta

app = Flask(__name__)

@app.route('/',methods = ['POST', 'GET'])
def mainView():
    if request.method == 'GET':
        t = datetime.now()
        today = date.today()
        yesterday = today - timedelta(days = 1)
        URL = f"https://www.seismicportal.eu/fdsnws/event/1/query?start={yesterday}T{t.hour -2 }:{t.minute}&end={today}T{t.hour -3 }:{t.minute}&minlat=42.240172&maxlat=29.588440&minlon=28.533673&maxlon=49.348036"
    elif request.method == 'POST':
        t1 = request.form["d1"]
        t2 = request.form["d2"]
        URL = f"https://www.seismicportal.eu/fdsnws/event/1/query?start={t1}&end={t2}&minlat=42.240172&maxlat=29.588440&minlon=28.533673&maxlon=49.348036"

    r = requests.get(URL)
    data = r.content
    data_dict = xmltodict.parse(data)
    json_data = json.dumps(data_dict)
    data = json.loads(json_data)

    time = [i["origin"]["time"]["value"][11:16] for i in data["q:quakeml"]["eventParameters"]["event"]]
    mag = [float(i["magnitude"]["mag"]["value"]) for i in data["q:quakeml"]["eventParameters"]["event"]]
    dec_time =[]
    for i in time:
        t = int(i[3:6]) / 60
        t = int(i[0:2]) + t
        dec_time.append("{:.1f}".format(t))

    fig = Figure()
    ax = fig.subplots()
    ax.plot(dec_time, mag)
    fig.savefig('static/Image/main.png')    
    min_mag, max_mag, total, last = min(mag), max(mag), len(mag), mag[:10]
    data = {
        'min_mag':min_mag,
        'max_mag':max_mag,
        'total':total,
        'last':last
    }
    return render_template('main.html', data=data)


if __name__ == '__main__':
    app.run()