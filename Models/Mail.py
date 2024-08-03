"""
The module which will interact between the models of the
application and the mail server to be used for the
application.

Authors:
    Darkness4869
"""
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from Environment import Environment
import smtplib


class Mail:
    """
    The model which will communicate to the mail servers for the
    application for the sending of mail notifications.
    """
    __recipient: str
    """
    The recipient of the mail
    """
    __subject: str
    """
    Subject of the mail
    """

    def __init__(self) -> None:
        pass

    def getRecipient(self) -> str:
        return self.__recipient

    def setRecipient(self, recipient: str) -> None:
        self.__recipient = recipient

    def getSubject(self) -> str:
        return self.__subject

    def setSubject(self, subject: str) -> None:
        self.__subject = subject