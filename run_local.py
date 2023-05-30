from src.domain.domain_types import Annonce, ContactInformation
from src.adapters.inbox.gmail_adapter import GmailAdapter
from src.adapters.cache.dynamodb_adapter import DynamodbAdapter
from src.adapters.cache.csv_adapter import CSVAdapter
from src.adapters.annonceApi.mock_adapter import MockAdapter
from src.adapters.annonceApi.seloger_adapter import SeLogerAdapter

from src.domain.domain import answer_all_annonces

if __name__ == '__main__':
    gmailAdapter = GmailAdapter.from_env()
    contact = ContactInformation.from_env()
    csvAdapter = CSVAdapter("annonces.csv")##DynamodbAdapter('find-a-roof')
    api = MockAdapter()

    csvAdapter.load()

    print("annonce mails: ", answer_all_annonces(
        inbox=gmailAdapter,
        cache=csvAdapter,
        api=api,
        contact=contact
    ))
