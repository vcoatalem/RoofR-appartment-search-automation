from domain.domain_types import Annonce, ContactInformation
from adapters.inbox.gmail_adapter import GmailAdapter
from adapters.cache.dynamodb_adapter import DynamodbAdapter
from adapters.cache.csv_adapter import CSVAdapter
from adapters.annonceApi.mock_adapter import MockAdapter
from adapters.annonceApi.seloger_adapter import SeLogerAdapter

from domain.domain import answer_all_annonces

if __name__ == '__main__':

    contact = ContactInformation.from_env()

    if contact is None:
        print("Contact information not found")
        exit(1)

    print(contact)

    gmailAdapter = GmailAdapter.from_env()

    csvAdapter = CSVAdapter("annonces.csv")##DynamodbAdapter('find-a-roof')
    api = MockAdapter()

    csvAdapter.load()

    print("annonce mails: ", answer_all_annonces(
        inbox=gmailAdapter,
        cache=csvAdapter,
        api=api,
        contact=contact
    ))
