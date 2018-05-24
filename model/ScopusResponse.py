class ScopusResponse:

    def __init__(self, pubmed_id: str, scopus_id: str, eid: str, url: str, cited_by_scopus: int):
        self.pubmed_id = pubmed_id
        self.scopus_id = scopus_id
        self.eid = eid
        self.url = url
        self.cited_by_scopus = cited_by_scopus
        self.url_scopus_record = ""
        self.url_scopus_cited_by = ""

    def to_output(self, delimiter):
        string = self.pubmed_id + delimiter + self.scopus_id + delimiter + self.eid + delimiter + self.url + delimiter + str(self.cited_by_scopus)
        return string

    def set_url_scopus_record(self, url_scopus_record: str):
        self.url_scopus_record = url_scopus_record

    def set_url_scopus_cited_by(self, url_scopus_cited_by: str):
        self.url_scopus_cited_by = url_scopus_cited_by