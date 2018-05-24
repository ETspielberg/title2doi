# Title2DOI

A small FLASK web service, taking a filename from the POST request, loads the corresponding file from the 
`LIBINTEL_:UPLOAD_DIR` directory containing an unformatted list of references.
 
each reference (= each line) is queried at the CrossRef-API to retrieve the corresponding DOI.
If a DOI is found, the MyCoRe repository is queried, whether it contains the entry. In addition,
Scopus is queried to retrieve the Scopus ID and actual citation counts. Results are written to the results.txt as spread sheet ascii (delimited by `;`).

## Configuration

Basic configuration data (CrossRef URL, Scopus URL, Scopus API key and MyCoRe repository API URL are set under ~/.libintel/config/title2dois.cfg:
```
LIBINTEL_UPLOAD_DIR = "<home directory>\\.libintel\\uploads"
CROSSREF_URL = "https://api.crossref.org/works?mailto=<E-Mail-Address>&rows=1&query="
MYCORE_URL = "address of MyCoRe repository"
SCOPUS_URL = "https://api.elsevier.com/content/"
SCOPUS_API_KEY = "<Scopus API Key>"
```

##setup
Create a virtual environment, install the packages from the `requirements.txt` and run the flask application
 (in Windows: `python -m flask run`)