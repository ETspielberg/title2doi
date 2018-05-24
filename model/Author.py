class Author:
    def __init__(self, surname: str, firstname: str, affiliation: list):
        self.surname = surname
        self.firstname = firstname
        self.affiliation = affiliation

    def to_output(self, delimiter):
        string = self.surname + delimiter + self.firstname + "(\""
        for affil in self.affiliation:
            string = string + affil["name"] + delimiter
        string = string + "\")"
        return string

    def set_firstname(self, firstname: str):
        self.firstname = firstname

    def set_affiliation(self, affiliation: str):
        self.affiliation = affiliation
