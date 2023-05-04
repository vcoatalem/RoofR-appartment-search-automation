from dataclasses import dataclass

from abc import ABC, abstractmethod

from domain.domain_types import Mail

class InboxPort(ABC):
    def __init__(self, email_address: str):
        self.email_address = email_address

    @abstractmethod
    def peekUnreadMails(self) -> list[Mail]:
        pass

    @abstractmethod
    def readUnreadMails(self) -> list[Mail]:
        pass
