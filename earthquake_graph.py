import json
import matplotlib.pyplot as plt

f = open("data.json", "r")
rawdata = f	
data = json.load(rawdata)
time = [i["origin"]["time"]["value"][11:16] for i in data["q:quakeml"]["eventParameters"]["event"]]
mag = [float(i["magnitude"]["mag"]["value"]) for i in data["q:quakeml"]["eventParameters"]["event"]]
dec_time =[]
for i in time:
	t = int(i[3:6]) / 60
	t = int(i[0:2]) + t
	dec_time.append("{:.1f}".format(t))
	
dec_time.reverse()
mag.reverse()
plt.plot(dec_time, mag)
plt.show()