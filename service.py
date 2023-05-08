import itertools
import os

from src.domain.domain_types import Annonce, ContactInformation
from src.adapters.inbox.gmail_adapter import GmailAdapter
from src.adapters.cache.dynamodb_adapter import DynamodbAdapter
from src.adapters.annonceApi.seloger_adapter import SeLogerAdapter

from src.domain.domain import answer_all_annonces

def handler(event, context):

    inbox = GmailAdapter.from_env()
    contact = ContactInformation.from_env()
    cache = DynamodbAdapter('find-a-roof')#CSVAdapter("annonces.csv")
    api = SeLogerAdapter()

    cache.load()

    print("annonce mails: ", answer_all_annonces(
        inbox,
        cache,
        api,
        contact
    ))
    return 0


if __name__ == '__main__':
    handler(None, None)