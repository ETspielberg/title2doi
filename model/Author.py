class Author:
    def __init__(self):
        self.surname = ""
        self.firstname = ""
        self.affiliation = []

    def to_output(self, delimiter):
        string = self.surname + delimiter + self.firstname + "(\""
        for affil in self.affiliation:
            string += affil["name"] + delimiter
        string += "\")"
        return string
