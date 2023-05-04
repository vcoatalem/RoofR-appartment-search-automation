
import itertools
import os

from domain.domain_types import Annonce

from secondary.inbox.gmail_adapter import GmailAdapter
from secondary.cache.csv_adapter import CSVAdapter


def handler(event, context):
    # Your code goes here!

    """
    email = os.getenv("FROM_EMAIL")
    name = os.getenv("NAME")
    phone = os.getenv("PHONE")

    print("found contact informations: ", email, name, phone)

    adds = AnnonceRepository.Basic()

    """

    gmailAdapter = GmailAdapter("victor.recherche.appartement@gmail.com")
    csvAdapter = CSVAdapter("annonces.csv")
    

    annonces = gmailAdapter.peekUnreadMails()
    print("annonces: ", annonces)

    """
    urls = set(list(itertools.chain(*[ get_urls(adds, content) for content in annonces ])))

    print("urls: ", urls)

    contact_agencies(urls, adds, email, name, phone)
    """
    return 0


if __name__ == '__main__':
    handler(None, None)