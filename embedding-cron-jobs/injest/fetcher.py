
import os
import requests
from requests.auth import HTTPBasicAuth



def fetch_confluence_pages():

    url = "https://advantalabs.atlassian.net/wiki/rest/api/content?type=page&expand=body.storage,version"

    confluence_user = os.getenv("CONFLUENCE_USER")
    confluence_token = os.getenv("CONFLUENCE_TOKEN")
    if not confluence_user or not confluence_token:
        raise ValueError("CONFLUENCE_USER and CONFLUENCE_TOKEN must be set in environment variables.")
    auth = HTTPBasicAuth(confluence_user, confluence_token)

    response = requests.get(url, auth=auth).json()

    transformed_response = response.get("results", [])


    return transformed_response
          