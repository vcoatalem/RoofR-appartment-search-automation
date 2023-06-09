import re
from urllib.parse import urlparse

import requests

from domain.annonce_api_port import AnnonceAPIPort
from domain.domain_types import Annonce, ContactInformation, Mail


class SeLogerAdapter(AnnonceAPIPort):

    def __init__(self) -> None:
        super().__init__()

    def contact(self, annonce: Annonce, contact: ContactInformation) -> AnnonceAPIPort.Response:
        print("contact annonce: ", annonce)
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
            print(res.status_code)
            if res.status_code == 200:
                return AnnonceAPIPort.Response(
                    annonce=annonce,
                    wasSent=True,
                    wasAccepted=True
                    )
            elif res.status_code == 404:
                return AnnonceAPIPort.Response(
                    annonce=annonce,
                    wasSent=True,
                    isOutdated=True
                    )
            else:
                return AnnonceAPIPort.Response(
                    annonce=annonce,
                    wasSent=True,
                    error={ "msg": res.text }
                )
        except Exception as e:
            return AnnonceAPIPort.Response(
                annonce=annonce,
                error={ "msg":  f"{str(e)}  \n--\n  {str(e.with_traceback())}"}
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