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
from typing import Union, List
from Models.Logger import Corporate_Database_Builder_Logger
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
    __logger: Corporate_Database_Builder_Logger
    """
    The logger that will all the action of the application.
    """

    def __init__(self) -> None:
        """
        Initializing the model which will set the data needed for
        the model to communicate with the SMTP servers.
        """
        self.ENV = Environment()
        self.setLogger(Corporate_Database_Builder_Logger())
        self._Mailer = SMTP(
            host=self.ENV.getSmtpHost(),
            port=self.ENV.getSmtpPort()
        )
        self._Mailer.starttls()
        self._Mailer.login(self.ENV.getMailUsername(), self.ENV.getMailPassword())
        self.getLogger().inform("The mailer has been initialized and all of its dependencies are injected!")

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

    def getLogger(self) -> Corporate_Database_Builder_Logger:
        return self.__logger

    def setLogger(self, logger: Corporate_Database_Builder_Logger) -> None:
        self.__logger = logger

    def send(self, recipient: str, subject: str, message: str, carbon_copy: Union[str, None] = None) -> None:
        """
        Sending the mail after having configured model.

        Parameters:
            recipient: string: Receiver of the mail.
            subject: string: Subject of the mail.
            message: string: Body of the mail.
            carbon_copy: string: The list of mail addresses where the mail should be forwarded.

        Returns:
            void
        """
        destination: List[str]
        self.setRecipient(recipient)
        self.setSubject(subject)
        self.setMessage(message)
        data: MIMEMultipart = MIMEMultipart()
        data["From"] = self.ENV.getMailUsername()
        data["To"] = self.getRecipient()
        data["Subject"] = self.getSubject()
        if carbon_copy:
            data["Cc"] = carbon_copy
            destination = [self.getRecipient()] + carbon_copy.split(",")
        else:
            destination = [self.getRecipient()]
        data.attach(MIMEText(self.getMessage(), "plain"))
        message_data: str = data.as_string()
        self._Mailer.sendmail(self.ENV.getMailUsername(), destination, message_data)
        self._Mailer.quit()