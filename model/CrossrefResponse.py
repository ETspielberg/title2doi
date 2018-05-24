import json


class CrossrefResponse:

    def __init__(self, reference: str, doi: str, title: str, authors: list, score: int, cited_by: int):
        self.reference = reference.replace("\n", "")
        self.doi = doi
        self.title = title
        self.authors = authors
        self.score = score
        self.cited_by = cited_by
        self.print_issn = ""
        self.electronic_issn = ""

    def set_print_issn(self, print_issn: str):
        self.print_issn = print_issn

    def set_electronic_issn(self, electronic_issn: str):
        self.electronic_issn = electronic_issn

    def to_json(self):
        return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True, indent=4)

    def to_csv_output(self, delimiter):
        string: str = "\"" + self.reference + "\"" + delimiter + self.doi + delimiter + self.print_issn + delimiter + \
                      self.electronic_issn + delimiter + self.title + delimiter + \
                      str(self.score) + delimiter + str(self.cited_by)
        string = string + delimiter
        # + \"\""
        # for author in self.authors:
        #     string = string + author.to_output(delimiter)
        # string = string + "\""
        string = string + delimiter + str(self.reference.replace("-", "").__contains__(self.title.replace("-", "")))
        return string
