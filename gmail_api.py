import os
import pickle
# Gmail API utils
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
# for encoding/decoding messages in base64
from base64 import urlsafe_b64decode, urlsafe_b64encode
# for dealing with attachement MIME types
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.image import MIMEImage
from email.mime.audio import MIMEAudio
from email.mime.base import MIMEBase
from mimetypes import guess_type as guess_mime_type
import base64

# Request all access (permission to read/send/receive emails, manage the inbox, and more)
SCOPES = ['https://mail.google.com/']
our_email = 'victor.recherche.appartement@gmail.com'

def gmail_authenticate():
    creds = None
    # the file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first time
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

def search_messages(service, query):
    result = service.users().messages().list(userId='me',q=query).execute()
    messages = [ ]
    if 'messages' in result:
        messages.extend(result['messages'])
    while 'nextPageToken' in result:
        page_token = result['nextPageToken']
        result = service.users().messages().list(userId='me',q=query, pageToken=page_token).execute()
        if 'messages' in result:
            messages.extend(result['messages'])
    return messages

def read_message(service, message_id):
    try:
        # Use the Gmail API to retrieve the message with the specified ID
        message = service.users().messages().get(userId='me', id=message_id).execute()
        #print(message)
        # Decode the message body from base64 URL encoding
        # print(message)

        if "parts" in message["payload"]:
            message_body = base64.urlsafe_b64decode(message['payload']['parts'][0]['body']['data']).decode('utf-8')
        else:
            message_body = base64.urlsafe_b64decode(message['payload']['body']['data']).decode('utf-8')
        return message["payload"]["headers"], message_body
    except:
        return None, None


def email_is_an_announce(email: str) -> bool:
    email = email.lower()
    return "annonce" in email


"""
def mark_email_as_read(service, message_id):
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
            'removeLabelIds': ['INBOX', 'UNREAD']
        }

        service.users().messages().modify(userId='me', id=message["id"], body=modify_request).execute()

    return res
