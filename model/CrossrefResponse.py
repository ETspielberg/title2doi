class CrossrefResponse:

    def __init__(self, reference, doi, title, authors, issn, score, cited_by):
        self.reference = reference
        self.doi = doi
        self.title = title
        self.authors = authors
        self.issn = issn
        self.score = score
        self.cited_by = cited_by

    def serialize(self):
        return {
            'reference': self.reference,
            'doi': self.doi,
            'title': self.title,
            'score': self.score,
            'cited-by': self.cited_by
        }
