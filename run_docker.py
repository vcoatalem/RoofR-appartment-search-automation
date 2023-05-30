from src.domain.domain_types import ContactInformation
from src.adapters.inbox.gmail_adapter import GmailAdapter
from src.adapters.cache.dynamodb_adapter import DynamodbAdapter
from src.adapters.annonceApi.seloger_adapter import SeLogerAdapter

from src.domain.domain import answer_all_annonces

if __name__ == '__main__':
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

