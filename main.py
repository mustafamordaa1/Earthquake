from flask import Flask, render_template
import requests
import json
import xmltodict
import matplotlib.pyplot as plt

app = Flask(__name__)

@app.route('/')
def hello_world():
    URL = "https://www.seismicportal.eu/fdsnws/event/1/query?start=2023-2-18&end=2023-2-19&minlat=42.240172&maxlat=29.588440&minlon=28.533673&maxlon=49.348036"
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
        
    plt.plot(dec_time, mag)
    plt.savefig('static/Image/main.png')
    min_mag, max_mag, total = min(mag), max(mag), len(mag)
    data = {
        'min_mag':min_mag,
        'max_mag':max_mag,
        'total':total
    }
    return render_template('main.html', data=data)


if __name__ == '__main__':
    app.run()