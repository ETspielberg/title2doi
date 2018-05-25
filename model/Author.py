class Author:
    def __init__(self):
        self.surname = ""
        self.firstname = ""
        self.affiliation = []

    def to_output(self):
        string = self.surname + "," + self.firstname + " ("
        try:
            for affil in self.affiliation:
                string += affil["name"].replace(";", " ")
                string += ", "
        except:
            print("no affiliation given")
        string += "), "
        return string
