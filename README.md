# Title2DOI

A small FLASK web service, taking a filename from the POST request, loads the corresponding file from the 
`LIBINTEL_:UPLOAD_DIR` directory containing an unformatted list of references.
 
each reference (= each line) is queried at the CrossRef-API to retrieve the corresponding DOI.
If a DOI is found, the MyCoRe repository is queried, whether it contains the entry. In addition,
Scopus is queried to retrieve the Scopus ID and actual citation counts. Results are written to the results.txt as spread sheet ascii (delimited by `;`).

## Configuration

You could store the basic configuration data (CrossRef URL, Scopus URL, Scopus API key and MyCoRe repository API URL  in the file: `~/.libintel/config/title2dois.cfg`, by filling it with the following content (add your own Scopus API key):
```
LIBINTEL_UPLOAD_DIR = "<home directory>\\.libintel\\uploads"
CROSSREF_URL = "https://api.crossref.org/works?mailto=<E-Mail-Address>&rows=1&query="
MYCORE_URL = "address of MyCoRe repository"
SCOPUS_URL = "https://api.elsevier.com/content/"
SCOPUS_API_KEY = "<Scopus API Key>"
```

## Setup

Create a virtual environment, install the packages from the `requirements.txt` and run the flask application
 (in Windows: `python -m flask run`)

Or using conda:
```
conda env create --file environment.yml
conda activate title2doi
export LIBINTEL_SETTINGS=~/.libintel/config/title2dois.cfg
```
then you can run the code with:
```
python start.py
```
