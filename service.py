
import itertools
import os

from dotenv import load_dotenv
from annonceRepository import AnnonceRepository
from gmail_api import get_annonces
from extract_mail_data import get_urls
from contact import contact_agencies



def handler(event, context):
    # Your code goes here!

    email = os.getenv("FROM_EMAIL")
    name = os.getenv("NAME")
    phone = os.getenv("PHONE")

    print("found contact informations: ", email, name, phone)

    adds = AnnonceRepository.Basic()

    print("adds: ", adds)

    annonces = get_annonces()

    print("annonces: ", annonces)

    urls = set(list(itertools.chain(*[ get_urls(adds, content) for content in annonces ])))

    print("urls: ", urls)

    contact_agencies(urls, adds, email, name, phone)
    
    return 0
