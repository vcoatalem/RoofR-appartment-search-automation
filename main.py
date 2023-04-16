import itertools
import os

from dotenv import load_dotenv
from annonceRepository import AnnonceRepository
from gmail_api import get_annonces
from extract_mail_data import get_urls
from contact import contact_agencies




def main():

    email = os.getenv("FROM_EMAIL")
    name = os.getenv("NAME")
    phone = os.getenv("PHONE")
    contact_message = os.getenv("MESSAGE")

    print("found contact informations: ", email, name, phone)

    adds = AnnonceRepository()

    print("adds: ", adds)

    annonces = get_annonces()

    print("annonces: ", annonces)

    urls = set(list(itertools.chain(*[ get_urls(adds, content) for content in annonces ])))

    print("urls: ", urls)

    contact_agencies(urls, adds, email, name, phone)
    
    #print(urls)


#print(get_unprocessed_urls(adds, "75014 Paris 14ème  (https://www.seloger.com/annonces/locations/appartement/paris-14eme-75/didot-porte-de-vanves/199502873.htm?utm_content=source_platform_alerting_legacy&cmp=AL-SLG-Classic-reco&utm_source=email_ali&utm_medium=B2CSLServiceEmailAlerteImmo_G&utm_campaign=169956089_20230411&utm_term=&pvd=SLG&utm_content=ville_recommandation_annonce)  75014 Paris 14ème  (https://www.seloger.com/annonces/locations/appartement/paris-14eme-75/didot-porte-de-vanves/199502873.htm?utm_content=source_platform_alerting_legacy&cmp=AL-SLG-Classic-reco&utm_source=email_ali&utm_medium=B2CSLServiceEmailAlerteImmo_G&utm_campaign=169956089_20230411&utm_term=&pvd=SLG&utm_content=ville_recommandation_annonce)"))