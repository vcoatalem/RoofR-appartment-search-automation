
import itertools
import os

from domain.domain_types import Annonce, ContactInformation
from secondary.inbox.gmail_adapter import GmailAdapter
from secondary.cache.csv_adapter import CSVAdapter
from secondary.annonceApi.mock_adapter import MockAdapter
from secondary.annonceApi.seloger_adapter import SeLogerAdapter


from domain.domain import answer_annonces

def handler(event, context):

    gmailAdapter = GmailAdapter.from_env()
    contact = ContactInformation.from_env()
    csvAdapter = CSVAdapter("annonces.csv")
    api = MockAdapter()

    csvAdapter.load()

    print("annonce mails: ", answer_annonces(
        inbox=gmailAdapter,
        cache=csvAdapter,
        api=api,
        contact=contact
    ))
    return 0


if __name__ == '__main__':
    handler(None, None)