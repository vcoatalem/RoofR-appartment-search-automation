import re
from urllib.parse import urlparse

import requests

from src.domain.annonce_api_port import AnnonceAPIPort
from src.domain.domain_types import Annonce, ContactInformation, Mail


class MockAdapter(AnnonceAPIPort):

    def __init__(self) -> None:
        super().__init__()

    def contact(self, annonce: Annonce, contact: ContactInformation) -> AnnonceAPIPort.Response:
        print(f"MOCK ADAPTER: mocking reply to annonce: {annonce}")
        return AnnonceAPIPort.Response(
            annonce=annonce,
            wasSent=True,
            wasAccepted=True,
            error=None
        )

    def find_urls_in_mail(self, mail: Mail) -> set[str]:
        pattern = r'https://a.seloger.com/[^ ]+'#/\d+\.htm'
        # Use the re.findall() function to extract all URLs that match the pattern
        links = set(re.findall(pattern, mail.content))

        def unshorten_url(longUrl: str) -> str:
            h = requests.head(longUrl)
            return h.headers["Location"] if "Location" in h.headers else None
        
        unshortened_urls = [ unshorten_url(url) for url in links ]

        urls = [ urlparse(url) for url in unshortened_urls if url is not None]

        return [ url.scheme + "://" + url.netloc + url.path for url in urls if "annonces/" in url.path]