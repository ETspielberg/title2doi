import re


class CrossrefResponse:

    def __init__(self):
        self.reference = ""
        self.doi = ""
        self.title = ""
        self.authors = []
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
        string += ("\"" + self.title.replace("\n", "") + "\"")
        string += delimiter
        string += str(self.score)
        string += delimiter
        string += str(self.cited_by)
        string += delimiter
        string += "\""
        for author in self.authors:
            string += author.to_output().replace("\n", "")
        string += "\""
        string += delimiter

        if self.reference.lower().__contains__("comment"):
            has_title = self.title.__contains__("comment")
        elif self.reference.lower().__contains__("erratum"):
            has_title = self.title.__contains__("erratum")
        else:
            has_title = reference_has(self.reference, self.title)
        string += str(has_title)
        return string


def reference_has(reference: str, item: str) -> bool:
    return reference.lower().__contains__(re.sub("[^ a-zA-Z0-9]", "", item.lower()))
