
import itertools
import os

from src.domain.domain_types import Annonce, ContactInformation
from src.adapters.inbox.gmail_adapter import GmailAdapter
from src.adapters.cache.csv_adapter import CSVAdapter
from src.adapters.annonceApi.mock_adapter import MockAdapter
from src.adapters.annonceApi.seloger_adapter import SeLogerAdapter


from src.domain.domain import answer_all_annonces

def handler(event, context):

    gmailAdapter = GmailAdapter.from_env()
    contact = ContactInformation.from_env()
    csvAdapter = CSVAdapter("annonces.csv")
    api = MockAdapter()

    csvAdapter.load()

    print("annonce mails: ", answer_all_annonces(
        inbox=gmailAdapter,
        cache=csvAdapter,
        api=api,
        contact=contact
    ))
    return 0


if __name__ == '__main__':
    handler(None, None)