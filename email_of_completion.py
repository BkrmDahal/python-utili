"""Send email using gmail API"""
import os
import base64
import traceback

import httplib2
import oauth2client
from oauth2client import client, tools
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from apiclient import errors, discovery

#path to access token not client secret json, use access_token.py to make token from client json
ACCESS_TOKEN_PATH = "M:\\gmail-python-email.json" ###change this###

def _get_credentials(access_token_path=ACCESS_TOKEN_PATH):
    """get the credentials from access token"""
    credential_path = access_token_path
    store = oauth2client.file.Storage(credential_path)
    credentials = store.get()
    return credentials

def send_email(subject: str, 
               msgHtml: "str or html str",
               to: list=['bkrm.dahal@gmail.com'],
               sender: str='Python scripts') -> "display message id or error":
    credentials = _get_credentials()
    http = credentials.authorize(httplib2.Http())
    service = discovery.build('gmail', 'v1', http=http)
    message1 = _create_message(sender, to, subject, msgHtml)
    _send_message_internal(service, "me", message1)

def _send_message_internal(service, user_id, message):
    try:
        message = (service.users().messages().send(userId=user_id, 
                                                   body=message).execute())
        print('Message Id: %s' % message['id'])
        return message
    except errors.HttpError as error:
        print('An error occurred: %s' % error)

def _create_message(sender, to,
                  subject, msgHtml):
    msg = MIMEMultipart('alternative')
    msg['Subject'] = subject
    msg['From'] = sender
    msg['To'] = ", ".join(to)
    msg.attach(MIMEText(msgHtml, 'plain'))

    raw = base64.urlsafe_b64encode(msg.as_bytes())
    raw = raw.decode()
    body = {'raw': raw}
    return body

def email_of_completion(subject:'subject of mail', 
                     to:list=['bkrm.dahal@gmail.com']):
    """Decorator for sending the mail"""
    def f(func):
        def wrapper(*args, **kwags):
            try:
                func(*args, **kwags)
                send_email('✔️ ' + subject +' SUCCESS', 
                           "You scripts has run sucessfully.", to=to)
            except Exception as e:
                send_email('❌   ' + subject + ' ERROR', 
                           "Error with your script \r\n \r\n ERROR \r\n {}.".format(
                               traceback.format_exc()), to=to)
        return wrapper
    return f

# test the decorators 
@email_of_completion(__file__)
def add(x, y):
    print(x+y)

def main():
    add(1, 2)
    add(1, "a")

if __name__ == "__main__":
    main()
