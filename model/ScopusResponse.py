class ScopusResponse:

    def __init__(self):
        self.pubmed_id = ""
        self.scopus_id = ""
        self.eid = ""
        self.url = ""
        self.cited_by_scopus = ""
        self.url_scopus_record = ""
        self.url_scopus_cited_by = ""

    def to_output(self, delimiter):
        string = self.pubmed_id
        string += delimiter
        string += self.scopus_id
        string += delimiter
        string += self.eid
        string += delimiter
        string += self.url
        string += delimiter
        string += str(self.cited_by_scopus)
        return string