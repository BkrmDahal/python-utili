"""Send email using gmail API"""
import os
import base64
import traceback

import httplib2
import oauth2client
from oauth2client import client, tools
from apiclient import errors, discovery

import mimetypes
from email import encoders
from email.message import Message
from email.mime.audio import MIMEAudio
from email.mime.base import MIMEBase
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication

SCOPES = 'https://www.googleapis.com/auth/gmail.send' #Scopes of your auth, here you can only send the email
CLIENT_SECRET_FILE = "keys\\client_secret.json" #path to json downloded from api, this is only need first time you make auth
APPLICATION_NAME = 'gmail' #project name in google developer console

def _get_credentials():
    """get the credentials, if its already present than it will fetch that otherwise use above client secret file to make new credentails"""
    current_dir = os.getcwd()
    home_dir = os.path.expanduser(current_dir)
    credential_dir = os.path.join(home_dir, '.credentials') 
    if not os.path.exists(credential_dir):
        os.makedirs(credential_dir)
    credential_path = os.path.join(credential_dir, 'gmail-python-email-send.json') #change this to path of file if you already have json file
    store = oauth2client.file.Storage(credential_path)
    credentials = store.get()
    if not credentials or credentials.invalid:
        flow = client.flow_from_clientsecrets(CLIENT_SECRET_FILE, SCOPES)
        flow.user_agent = APPLICATION_NAME
        credentials = tools.run_flow(flow, store)
        print('Storing credentials to ' + credential_path)
    return credentials

def send_message(subject: str, msgHtml: "str or html str",
                to: list='',
                attached_file=None,
                sender: str='Python scripts') -> "display message id or error if any":
    credentials = _get_credentials()
    http = credentials.authorize(httplib2.Http())
    service = discovery.build('gmail', 'v1', http=http)
    message1 = _create_message(sender, to, subject, msgHtml, attached_file)
    _send_message_internal(service, "me", message1)

def _send_message_internal(service, user_id, message):
    try:
        message = (service.users().messages().send(userId=user_id, body=message).execute())
        print('Message Id: %s' % message['id'])
        return message
    except errors.HttpError as error:
        print('An error occurred: %s' % error)

def _create_message(sender, to,
                  subject, msgHtml, attached_file=None):
    msg = MIMEMultipart('alternative')
    msg['Subject'] = subject
    msg['From'] = sender
    msg['To'] = ", ".join(to)
    msg.attach(MIMEText(msgHtml, 'html'))

    ##added file if any
    if attached_file:
        my_mimetype, encoding = mimetypes.guess_type(attached_file)

        if my_mimetype is None or encoding is not None:
            my_mimetype = 'application/octet-stream' 

        main_type, sub_type = my_mimetype.split('/', 1)

        if main_type == 'text':
            print("text")
            temp = open(attached_file, 'r')  # 'rb' will send this error: 'bytes' object has no attribute 'encode'
            attachement = MIMEText(temp.read(), _subtype=sub_type)
            temp.close()

        elif main_type == 'image':
            print("image")
            temp = open(attached_file, 'rb')
            attachement = MIMEImage(temp.read(), _subtype=sub_type)
            temp.close()

        elif main_type == 'audio':
            print("audio")
            temp = open(attached_file, 'rb')
            attachement = MIMEAudio(temp.read(), _subtype=sub_type)
            temp.close()            

        elif main_type == 'application' and sub_type == 'pdf':   
            temp = open(attached_file, 'rb')
            attachement = MIMEApplication(temp.read(), _subtype=sub_type)
            temp.close()

        else:                              
            attachement = MIMEBase(main_type, sub_type)
            temp = open(attached_file, 'rb')
            attachement.set_payload(temp.read())
            temp.close()

        #-----3.3 encode the attachment, add a header and attach it to the message
        encoders.encode_base64(attachement)
        filename = attached_file.split('\\')[-1]
        attachement.add_header('Content-Disposition', 'attachment', filename=filename) # name preview in email
        msg.attach(attachement)

    raw = base64.urlsafe_b64encode(msg.as_bytes())
    raw = raw.decode()
    body = {'raw': raw}
    return body

def send_message_d(subject, body, to, attached_file ):
    """Decorator for sending the mail"""
    def f(func):
        def wrapper(*args, **kwags):
            try:
                func(*args, **kwags)
                send_message('✔️ ' + subject +' SUCESS', body, to=to, attached_file=attached_file)
            except Exception as e:
                send_message('❌   ' + subject + ' ERROR', "There is error with your script \r\n \r\n ERROR \r\n {}.".format(traceback.format_exc()), to=to, attached_file=attached_file)
        return wrapper
    return f
