from domain.domain_types import ContactInformation
from adapters.inbox.gmail_adapter import GmailAdapter
from adapters.cache.dynamodb_adapter import DynamodbAdapter
from adapters.annonceApi.seloger_adapter import SeLogerAdapter
from adapters.annonceApi.mock_adapter import MockAdapter

from domain.domain import answer_all_annonces

if __name__ == '__main__':
    contact = ContactInformation.from_env()
    if contact is None:
        print("Contact information not found")
        exit(1)

    inbox = GmailAdapter.from_env()
    cache = DynamodbAdapter.from_env()#CSVAdapter("annonces.csv")
    api = MockAdapter()#SeLogerAdapter()

    print(contact)

    cache.load()

    print("annonce mails: ", answer_all_annonces(
        inbox,
        cache,
        api,
        contact
    ))

