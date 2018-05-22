from flask import Flask
from flask import request
from flask import jsonify
import requests

from model.CrossrefResponse import CrossrefResponse

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
            json_data = r.json()
            status = json_data["status"]
            if status == "ok":
                data = json_data["message"]["items"][0]
                title = data["title"][0]
                authors = jsonify(data["author"])
                doi = data["DOI"]
                issns = jsonify(data["ISSN"])
                cited_by = data["is-referenced-by-count"]
                score = data["score"]
                crossref_response = CrossrefResponse(line, doi, title, authors, issns, score, cited_by)
                results.append(crossref_response)
    return jsonify(results)
