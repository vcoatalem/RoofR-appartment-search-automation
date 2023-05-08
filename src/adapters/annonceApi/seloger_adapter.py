import re
from urllib.parse import urlparse

import requests

from src.domain.annonce_api_port import AnnonceAPIPort
from src.domain.domain_types import Annonce, ContactInformation, Mail


class SeLogerAdapter(AnnonceAPIPort):

    def __init__(self) -> None:
        super().__init__()

    def contact(self, annonce: Annonce, contact: ContactInformation) -> AnnonceAPIPort.Response:
        s = requests.Session()
        s.headers.update({
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36"
        })
        payload = {
            "email": contact.email,
            "listingId": annonce.id,
            "listingPublicationId": 1,
            "message": contact.message,
            "name": contact.name,
            "phone": contact.phone
        }
        try:
            res = s.post("https://www.seloger.com/annoncesbff/2/Contact", json=payload)
            if res.status_code == 200:
                return AnnonceAPIPort.Response(
                    annonce=annonce,
                    wasSent=True,
                    wasAccepted=True,
                    error=None
                    )
            else:
                return AnnonceAPIPort.Response(
                    annonce=annonce,
                    wasSent=True,
                    wasAccepted=False,
                    error={ "msg": res.text }
                )
        except Exception as e:
            return AnnonceAPIPort.Response(
                annonce=annonce,
                wasSent=False,
                wasAccepted=False,
                error={ "msg":  f"{str(e)}  \n--\n  {str(e.with_traceback())}"}
            )

    def find_urls_in_mail(self, mail: Mail) -> set[str]:
        pattern = r'https://www\.seloger\.com/annonces/[^ ]+'#/\d+\.htm'
        # Use the re.findall() function to extract all URLs that match the pattern
        links = set(re.findall(pattern, mail.content))

        urls = [ urlparse(link) for link in links]

        return [ url.scheme + "://" + url.netloc + url.path for url in urls ]