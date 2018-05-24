from flask import Flask
from flask import request
import requests
import xmltodict

from model.Author import Author
from model.ScopusResponse import ScopusResponse
from model.CrossrefResponse import CrossrefResponse

app = Flask(__name__)
# app.config.from_object('yourapplication.default_settings')
app.config.from_envvar("LIBINTEL_SETTINGS")

crossref_url = app.config.get("CROSSREF_URL")
mycore_url = app.config.get("MYCORE_URL")
scopus_url = app.config.get("SCOPUS_URL")
scopus_api_key = app.config.get("SCOPUS_API_KEY")

"https://api.crossref.org/works?mailto=Eike.Spielberg@uni-due.de&rows=1&query="
location = app.config.get("LIBINTEL_UPLOAD_DIR") + "\\title2doi\\"


def cleanup(line):
    return line.replace(".", " ").replace(";", " ").replace("\"", " ").replace("\'", " ").replace("/", "") \
        .replace(" ", "+").replace("\n", "")


@app.route('/title2dois', methods=['POST'])
def title_to_dois():
    mode = request.form['mode']
    if mode == "upload":
        file = request.form('file')
    else:
        filename = request.form['filename']
        file = open(location + filename, "r")
    f = open('results.txt', 'w')
    f.write(
        "reference; DOI; Print ISSN; Online ISSN; title; score; cited-by (CrossRef); authors; title in reference?; title in MyCoRe?; PubMed ID; Scopus ID; EID; Link; cited-by (Scopus)\n")
    for line in file:
        search_term = cleanup(line)
        r = requests.get(crossref_url + search_term)
        if r.status_code == 200:
            json_data = r.json()
            status = json_data["status"]
            if status == "ok":
                data = json_data["message"]["items"][0]
                title = data["title"][0]
                authors = []
                for author in data["author"]:
                    author_object = Author(author["family"], "", [])
                    try:
                        author_object.set_firstname(author["given"])
                    except KeyError:
                        print("no given name")
                    try:
                        author_object.set_affiliation(author["affiliation"])
                    except IndexError:
                        print("no affiliation given")
                    authors.append(author_object)
                doi = data["DOI"]
                cited_by = data["is-referenced-by-count"]
                score = data["score"]
                crossref_response = CrossrefResponse(line, doi, title, authors, score, cited_by)
                for issn in data["issn-type"]:
                    if issn["type"] == "print":
                        crossref_response.set_print_issn(issn["value"])
                    if issn["type"] == "electronic":
                        crossref_response.set_electronic_issn(issn["value"])
                url = mycore_url + "search?q=id_doi:" + doi
                r = requests.get(url)
                if r.status_code == 200:
                    mycore_data_response = r.text
                    mycore_xml = xmltodict.parse(mycore_data_response)
                    try:
                        found = mycore_xml['response']['result']['doc']['str']
                        in_mycore = True
                    except:
                        in_mycore = False
                else:
                    in_mycore = 'MyCoRe not reachable'
                url = scopus_url + 'abstract/citation-count?doi=' + doi + '&apiKey=' + scopus_api_key
                print('requesting url: ' + url)
                r = requests.get(url)
                if r.status_code == 200:
                    scopus_data = r.json()
                    document = scopus_data['citation-count-response']['document']
                    if document['pubmed_id'] is not None:
                        pubmed_id = document['pubmed_id']
                    else:
                        pubmed_id = ""
                    if document['dc:identifier'] is not None:
                        scopus_id = document['dc:identifier']
                    else:
                        scopus_id = ""
                    if document['eid'] is not None:
                        eid = document['eid']
                    else:
                        eid = ""
                    if document['prism:url'] is not None:
                        url = document['prism:url']
                    else:
                        url = ""
                    if document['citation-count'] is not None:
                        cited_by_scopus = document['citation-count']
                    else:
                        cited_by_scopus = 0
                    scopus_response = ScopusResponse(pubmed_id, scopus_id, eid, url, cited_by_scopus)
                else:
                    scopus_response = ScopusResponse("", "", "", "", 0)
                delimiter = "; "
                result_line = crossref_response.to_csv_output(delimiter)

                result_line = result_line + delimiter + str(in_mycore)
                result_line = result_line + delimiter + scopus_response.to_output(delimiter)
                f.write("%s\n" % result_line)
    f.close()
    return "finished"
