import base64
import os
import pickle

from dotenv import load_dotenv
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
from google.oauth2 import service_account


# Gmail API utils
from googleapiclient.discovery import build

from domain.domain_types import Mail
from domain.inbox_port import InboxPort

# Request all access (permission to read/send/receive emails, manage the inbox, and more)
#our_email = 'victor.recherche.appartement@gmail.com'

class GmailAdapter(InboxPort):
    def __init__(self, email_address: str):
        super().__init__(email_address)
        self.service = self.__gmail_authenticate()
        results = self.service.users().labels().list(userId='me').execute()

    @staticmethod
    def from_env():
        load_dotenv()
        mail: str = os.getenv("FROM_EMAIL")
        return GmailAdapter(mail)

    def __gmail_authenticate(self):
        SCOPES = ['https://mail.google.com/']
        creds = None
        if os.path.exists("token.pickle"):
            with open("token.pickle", "rb") as token:
                creds = pickle.load(token)
        # if there are no (valid) credentials availablle, let the user log in.
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
                creds = flow.run_local_server(port=0)
            # save the credentials for the next run
            with open("token.pickle", "wb") as token:
                pickle.dump(creds, token)
        return build('gmail', 'v1', credentials=creds)
    
    def __class_email_as_read(self, emailId) -> bool:
        modify_request = {
            'addLabelIds': [],
            'removeLabelIds': ['UNREAD']
        }
        self.service.users().messages().modify(userId='me', id=emailId, body=modify_request).execute()

    def __get_unread_messages(self):
        query = 'is:unread'
        result = self.service.users().messages().list(userId='me',q=query).execute()
        messages = [ ]
        if 'messages' in result:
            messages.extend(result['messages'])
        while 'nextPageToken' in result:
            page_token = result['nextPageToken']
            result = self.service.users().messages().list(userId='me',q=query, pageToken=page_token).execute()
            if 'messages' in result:
                messages.extend(result['messages'])
        return messages

    def __read_message(self, message_id) -> Mail:
        try:
            # Use the Gmail API to retrieve the message with the specified ID
            message = self.service.users().messages().get(userId='me', id=message_id).execute()
            # Decode the message body from base64 URL encoding



            fromHeader = next(filter(lambda header: header['name'] == 'From', message['payload']['headers']), None)
            #print("from header:", fromHeader)
            subjectHeader = next(filter(lambda header: header['name'] == 'Subject', message['payload']['headers']), None)
            #print("subject header:", subjectHeader)

            def getMessageBody():
                if "parts" in message["payload"]:
                    return base64.urlsafe_b64decode(message['payload']['parts'][0]['body']['data']).decode('utf-8')
                else:
                    return base64.urlsafe_b64decode(message['payload']['body']['data']).decode('utf-8')
            
            return Mail(
                sender=fromHeader['value'],
                subject=subjectHeader['value'], #TODO: find proper attribute names
                content=getMessageBody()
            )
        except:
            return None


    def peekUnreadMails(self) -> list[Mail]:
        messages = self.__get_unread_messages()
        #print("message: ", messages[0])
        mails : list[Mail] = list(map(lambda message: self.__read_message(message["id"]), messages))
        return [ mail for mail in mails if mail is not None ]

    def readUnreadMails(self) -> list[Mail]:
        messages = self.__get_unread_messages()
        mails : list[Mail] = list(map(lambda message: self.__read_message(message["id"]), messages))
        for message in messages:
            self.__class_email_as_read(message)
        return [ mail for mail in mails if mail is not None ]

"""
def get_annonces() -> list[str]:
    # get the Gmail API service
    service = gmail_authenticate()

    messages = search_messages(service, query='is:unread')

    res = []
    for message in messages:
        headers, content = read_message(service, message["id"])
        
        if not headers:
            print(f"error reading message: {message['id']}")
            continue

        if any(map(lambda header: header["name"] == "Subject" and email_is_an_announce(header["value"]), headers)):
            print("Found an annonce: \n", content)
            res.append(content)

        modify_request = {
            'addLabelIds': [],
            'removeLabelIds': ['UNREAD']
        }

        service.users().messages().modify(userId='me', id=message["id"], body=modify_request).execute()

    return res
"""