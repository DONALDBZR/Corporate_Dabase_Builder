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