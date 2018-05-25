from flask import Flask
from flask import request
import requests
import xmltodict
import re

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
    return re.sub('[^ a-zA-Z0-9]', '', line).replace("\n", "")


@app.route('/title2dois', methods=['POST'])
def title_to_dois():
    n_total = 0
    n_crossref = 0
    n_mycore = 0
    n_scopus = 0
    filename = request.form['filename']
    file = open(location + filename, "r", encoding="utf8")
    file_output = open(location + filename + ".out", 'w')
    file_data = open(location + filename + ".data", 'w')
    file_output.write(
        "reference; DOI; Print ISSN; Online ISSN; title; score; cited-by (CrossRef); authors; title in reference?; MyCoRe-ID; PubMed ID; Scopus ID; EID; Link; cited-by (Scopus)\n")
    file_data.write("references; CrossRef Response; Scopus Response")
    for line in file:
        line = cleanup(line)
        n_total = n_total + 1
        print('reading entry ' + str(n_total))
        r = requests.get(crossref_url + line.replace(" ", "+"))
        if r.status_code == 200:
            crossref_data = r.json()
            status = crossref_data["status"]
            if status == "ok":
                print('hit in crossref')
                n_crossref += 1
                crossref_response = CrossrefResponse()
                crossref_response.reference = line
                data = crossref_data["message"]["items"][0]
                try:
                    crossref_response.title = data["title"][0]
                except KeyError:
                    print("no title given")
                authors = []
                try:
                    for author in data["author"]:
                        author_object = Author()
                        try:
                            author_object.surname = author["family"]
                        except KeyError:
                            print("no family name")
                        try:
                            author_object.firstname = author["given"]
                        except KeyError:
                            print("no given name")
                        try:
                            author_object.affiliation = author["affiliation"]
                        except IndexError:
                            print("no affiliation given")
                        authors.append(author_object)
                except KeyError:
                    print('no authors given')
                    authors.append(Author())
                try:
                    crossref_response.doi = data["DOI"]
                except KeyError:
                    print("no doi given")
                try:
                    crossref_response.cited_by = data["is-referenced-by-count"]
                except KeyError:
                    print("no cioted-by given")
                try:
                    crossref_response.score = data["score"]
                except KeyError:
                    print("no score given")
                try:
                    for issn in data["issn-type"]:
                        if issn["type"] == "print":
                            crossref_response.print_issn = issn["value"]
                        if issn["type"] == "electronic":
                            crossref_response.electronic_issn = issn["value"]
                except KeyError:
                    print("no ISSNs given")

                print('requesting DOI ' + crossref_response.doi + " in MyCoRe repository")
                url = mycore_url + "search?q=id_doi:" + crossref_response.doi
                r = requests.get(url)
                mycore_id = ""
                if r.status_code == 200:
                    mycore_data_response = r.text
                    mycore_xml = xmltodict.parse(mycore_data_response)
                    try:
                        mycore_id = mycore_xml['response']['result']['doc']['str']['#text']
                        n_mycore += 1
                    except KeyError:
                        print("not found in MyCoRe repository")
                print('requesting DOI ' + crossref_response.doi + " in Scopus")
                url = scopus_url + 'abstract/citation-count?doi=' + crossref_response.doi + '&apiKey=' + scopus_api_key
                r = requests.get(url)
                scopus_response = ScopusResponse()
                scopus_data = ""
                if r.status_code == 200:
                    scopus_data = r.json()
                    document = scopus_data['citation-count-response']['document']
                    if document['@status'] == "found":
                        n_scopus += 1
                        if document['pubmed_id'] is not None:
                            scopus_response.pubmed_id = document['pubmed_id']
                        else:
                            print("Scopus: no PubMed ID given")
                        if document['dc:identifier'] is not None:
                            scopus_response.scopus_id = document['dc:identifier']
                        else:
                            print("Scopus: no Scopus ID given")
                        if document['eid'] is not None:
                            scopus_response.eid = document['eid']
                        else:
                            print("Scopus: no EID given")
                        if document['prism:url'] is not None:
                            scopus_response.url = document['prism:url']
                        else:
                            print("Scopus: no URL given")
                        if document['citation-count'] is not None:
                            scopus_response.cited_by_scopus = document['citation-count']
                        else:
                            print("Scopus: no Cited-By given")
                delimiter = "; "
                result_line = crossref_response.to_output(delimiter) + delimiter + mycore_id + delimiter + scopus_response.to_output(delimiter)
                file_output.write("%s\n" % result_line.encode('UTF-8'))
                data_line = line + delimiter + str(crossref_data) + delimiter + str(scopus_data)
                file_data.write("%s\n" % data_line.encode('UTF-8'))
            else:
                file_output.write(line + ";;;;;;;;;;;;;;;")
                file_data.write(line + ";;")

    file_output.write('\nOut of ' + str(n_total) + ' references, ' + str(n_crossref) + ' DOIs were found.\n')
    file_output.write('\nOut of ' + str(n_total) + ' references, ' + str(n_mycore) + ' DOIs were found in the MyCoRe repository.\n')
    file_output.write('\nOut of ' + str(n_total) + ' references, ' + str(n_scopus) + ' Scopus entries were found.\n')
    file_output.close()
    return "finished"
