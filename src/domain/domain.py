from dataclasses import dataclass

from dotenv import load_dotenv

from src.domain.annonce_api_port import AnnonceAPIPort
from src.domain.cache_port import CachePort
from src.domain.domain_types import Annonce, ContactInformation, Mail
from src.domain.inbox_port import InboxPort


def get_latest_agency_mails(inbox: InboxPort, read: bool = False) -> list[Mail]:
    mails : list[Mail] = inbox.peekUnreadMails() if not read else inbox.readUnreadMails()
    annonces = [ mail for mail in mails if mail.is_annonce() ]
    return annonces

def extract_annonces_from_one_mail(mail: Mail, api: AnnonceAPIPort) -> set[Annonce]:
    urls = api.find_urls_in_mail(mail)
    annonces = [ Annonce.from_url(url) for url in urls ]
    return set(annonces)

def extract_annonces_from_all_mails(mails: list[Mail], api: AnnonceAPIPort) -> set[Annonce]:
    set_list = [ extract_annonces_from_one_mail(mail, api) for mail in mails ]
    return set().union(*set_list)

def answer_annonce(annonce: Annonce, api: AnnonceAPIPort, cache: CachePort, contact: ContactInformation) -> AnnonceAPIPort.Response:
    response = api.contact(annonce, contact)
    if response.wasAccepted:
        cache.add(annonce)
    return response

def filter_annonces_in_cache(annonces: set[Annonce], cache: CachePort) -> set[Annonce]:
    return [ i for i in annonces if not cache.contains(i) ]


def answer_all_annonces(inbox: InboxPort, cache: CachePort, api: AnnonceAPIPort, contact: ContactInformation) -> list[AnnonceAPIPort.Response]:
    mails = get_latest_agency_mails(inbox, read=False)
    print(f"found {len(mails)} mails")
    annonces = extract_annonces_from_all_mails(mails, api)
    print(f"found {len(annonces)} annonces")
    annonces = filter_annonces_in_cache(annonces, cache)
    print(f"filtered annonces already processed. {len(annonces)} remaining")
    responses = [ response for response in map(lambda annonce: answer_annonce(annonce, api, cache, contact), annonces)]
    save = cache.save()
    print(f"Cache saving success: ", save)
    return responses


