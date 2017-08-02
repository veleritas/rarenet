import requests
from lxml.html import fromstring

class UMLSAPI:
    url = "https://utslogin.nlm.nih.gov"
    auth_endpoint = "/cas/v1/api-key"

    def __init__(self, api_key):
        self.api_key = api_key
        self.tgt = self.get_tgt()

    def get_tgt(self):
        """Get a ticket granting ticket. Needed once every 8 hours."""
        params = {"apikey": self.api_key}
        header = {
            "Content-type": "application/x-www-form-urlencoded",
            "Accept": "text/plain",
            "User-Agent": "python"
        }

        resp = requests.post(
            self.url + self.auth_endpoint,
            data=params, headers=header
        )

        return fromstring(resp.text).xpath("//form/@action")[0]

    def get_st(self):
        """Get a service ticket. Needed for every API call."""
        params = {"service": "http://umlsks.nlm.nih.gov"}
        header = {
            "Content-type": "application/x-www-form-urlencoded",
            "Accept": "text/plain",
            "User-Agent": "python"
        }

        return requests.post(self.tgt, data=params, headers=header).text

    def query(self, url, extra_params=None):
        """Query the API with the given url."""

        params = {"ticket": self.get_st()}
        if extra_params is not None:
            params = {**params, **extra_params}

        resp = requests.get(url, params=params)

        if resp.status_code == requests.codes.ok:
            return resp.json()

        return None
