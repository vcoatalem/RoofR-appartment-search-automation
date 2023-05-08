import re
from urllib.parse import urlparse

from domain.annonce_api_port import AnnonceAPIPort
from domain.domain_types import Annonce, ContactInformation, Mail


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
        pattern = r'https://www\.seloger\.com/annonces/[^ ]+'#/\d+\.htm'
        # Use the re.findall() function to extract all URLs that match the pattern
        links = set(re.findall(pattern, mail.content))
        #print(links)


        urls = [ urlparse(link) for link in links]



        return [ url.scheme + "://" + url.netloc + url.path for url in urls ]