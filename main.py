import os, webbrowser,  http.client, json, time
from flask import Flask, render_template, send_from_directory

print("---")
print("---")
print("the application is running, please wait while it collects the required information")

with open("s_data_ru.json", "r") as read_file:
    data_ru = json.load(read_file)

with open("s_data_global.json", "r") as read_file:
    data_g = json.load(read_file)

app = Flask(__name__)

while True:
        try:
            conn = http.client.HTTPSConnection("eapi.stalcraft.net")
            break
        except:
            print("no connection...")

token = os.environ["TOKEN"]
headers = {
        'Content-Typ': "application/json",
        'Authorization': f"Bearer {token}"
        }

for i in range(1, 3):
        print("---")
        print(i)
        print("---")
        new_data=[]
        if i == 1:
            data = data_ru
            region = "ru"
        else:
            data = data_g
            region = "eu"
        for a in range(len(data)):
            print(a/len(data)*100)
            while True:
                try:
                    conn.request("GET", f"/{region}/auction/{data[a]['id']}/lots", headers=headers)
                    res = conn.getresponse()
                    break
                except:
                    print("no connection...")
            d = json.loads(res.read().decode("utf-8"))
            try:
                if d["total"] > 0:
                    new_data.append([data[a]["name_ru"], data[a]["name_en"], d, data[a]["icon"], data[a]["category"]])
            except KeyError:
                print("---")
                print("wait")
                time.sleep(60)
                print("wait is over")
                print("---")
        if i == 1:
            new_data_ru = new_data
        else:
            new_data_g = new_data

@app.route('/smonitoring')
def index():
        return render_template("index.html", data=[new_data_g, new_data_ru])

@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'),
                               'favicon.ico', mimetype='image/vnd.microsoft.icon')

if __name__ == "__main__":
    print("---")
    print("---")
    print("Ready. Additional information can be found in the browser console on the page.")
    webbrowser.open_new_tab("http://127.0.0.1:5000/smonitoring") 
    app.run(host="0.0.0.0")