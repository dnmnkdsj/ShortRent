from flask_mail import Message
from . import mailServer

def send_email(destinations:[str], title:str, body, html):
    msg = Message(
        title,
        # sender="hydroxyapatite@126.com", # use default sender.
        recipients=destinations,
        body=body,
        html=html
    )
    mailServer.send(msg)

