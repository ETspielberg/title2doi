class Author:
    def __init__(self):
        self.surname = ""
        self.firstname = ""
        self.affiliation = []

    def to_output(self, delimiter):
        string = self.surname
        string += delimiter + self.firstname
        string += "(\""
        for affil in self.affiliation:
            string += affil["name"] + delimiter
        string += "\")"
        return string
