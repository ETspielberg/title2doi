from flask import Flask
from flask import request
from flask import jsonify
import requests

app = Flask(__name__)
# app.config.from_object('yourapplication.default_settings')
app.config.from_envvar("LIBINTEL_SETTINGS")
url = "https://api.crossref.org/works?mailto=Eike.Spielberg@uni-due.de&rows=1&query="
location = app.config.get("LIBINTEL_UPLOAD_DIR") + "\\title2doi\\"


def cleanup(line):
    return line.replace(".", " ").replace(";", " ").replace("\"", " ").replace("\'", " ").replace("/", "")\
        .replace(" ", "+").replace("\n", "")


@app.route('/title2dois', methods=['POST'])
def title_to_dois():
    mode = request.form['mode']
    if mode == "upload":
        file = request.form('file')
    else:
        filename = request.form['filename']
        file = open(location + filename, "r")
    results = []
    for line in file:
        search_term = cleanup(line)
        r = requests.get(url + search_term)
        if r.status_code == 200:
            json = r.json()
            results.append(json)
    return jsonify(results)
