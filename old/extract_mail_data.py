import email_listener
import os
import re
from bs4 import BeautifulSoup
from contact import contact
from urllib.parse import urlparse

from dotenv import load_dotenv
from old.annonceRepository import AnnonceRepository


def get_urls(adds: AnnonceRepository, content: str) -> set[str]:
    #print(content)
    pattern = r'https://www\.seloger\.com/annonces/[^ ]+'#/\d+\.htm'
    # Use the re.findall() function to extract all URLs that match the pattern
    links = set(re.findall(pattern, content))

    urls = [ urlparse(link) for link in links]

    return [ url.scheme + "://" + url.netloc + url.path for url in urls ]
