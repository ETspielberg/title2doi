import re

class CrossrefResponse:

    def __init__(self):
        self.reference = ""
        self.doi = ""
        self.title = ""
        self.authors = ""
        self.score = 0
        self.cited_by = ""
        self.print_issn = ""
        self.electronic_issn = ""

    def to_output(self, delimiter):
        string: str = "\"" + self.reference + "\""
        string += delimiter
        string += self.doi
        string += delimiter
        string += self.print_issn
        string += delimiter
        string += self.electronic_issn
        string += delimiter
        string += self.title
        string += delimiter
        string += str(self.score)
        string += delimiter
        string += str(self.cited_by)
        string += delimiter
        string += "\""
        for author in self.authors:
            string += author.to_output(delimiter)
        string += "\""
        string += delimiter
        string += str(self.reference.__contains__(re.sub('[^ a-zA-Z0-9]', '', self.title)))
        return string
