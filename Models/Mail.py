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
from smtplib import SMTP
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
    __message: str
    """
    Body of the mail
    """
    _Mailer: SMTP
    """
    It is the communication protocol for electronic mail
    transmission as the mail servers and other message transfer
    agents use it to send and receive mail messages.
    """
    ENV: Environment
    """
    The ENV file of the application which stores the important
    information which allows the application to operate
    smoothly.
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

    def getMessage(self) -> str:
        return self.__message

    def setMessage(self, message: str) -> None:
        self.__message = message