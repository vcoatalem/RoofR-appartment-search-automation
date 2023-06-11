import json
import os
import re
from dataclasses import dataclass

from dotenv import load_dotenv


@dataclass
class Annonce:
    def __init__(self, id: str, url: str) -> None:
        self.id = id
        self.url = url

    @staticmethod
    def __extract_id_from_url(url: str) -> str:
        extract_id_pattern = r"/(\d+)\.htm"
        match = re.search(pattern=extract_id_pattern, string=url)
        if match:
            number = match.group(1)
            return number
        return None

    @staticmethod
    def from_url(url: str):
        res = Annonce(
                id=Annonce.__extract_id_from_url(url),
                url=url
            )
        if not res.id:
            return None
        return res
    
    def __repr__(self):
        return "Annonce(" + self.url + ")"

    def __hash__(self):
        return hash(self.url)

@dataclass
class Mail():
    def __init__(self, sender: str, subject: str, content: str):
        self.sender = sender
        self.subject = subject
        self.content = content

    def is_annonce(self) -> bool:
        return "annonce" in self.subject \
            or "vous adresse ses dernières exclusivités" in self.subject
    
    def __repr__(self):
        return f"mail from sender: {self.sender} with subject: {self.subject}"
    
@dataclass
class ContactInformation:

    def __init__(self, email: str, name: str, phone: str, message: str):
        self.email = email
        self.name = name
        self.phone = phone
        self.message = message

    def __str__(self):
        return f"ContactInformation for: {self.email} \n" \
            + json.dumps({info: getattr(self, info) for info in { "email", "name", "phone", "message" }})


    @staticmethod
    def message_from_file(filename: str):
        with open(filename, mode="r") as f:
            txt = f.read()
            return txt

    @staticmethod
    def from_env():
        load_dotenv()
        email = os.getenv("FROM_EMAIL")
        name = os.getenv("FROM_NAME")
        phone = os.getenv("FROM_PHONE")
        message = os.getenv("FROM_MESSAGE")
        if any(s in [None, ""] for s in [email, name, phone, message]):
            return None
        return ContactInformation(
            email=email,
            name=name,
            phone=phone,
            message=message
        )

    