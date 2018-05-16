"""test email"""

import base64
import smtplib
import mimetypes
from email import encoders
from email.message import Message
from email.mime.audio import MIMEAudio
from email.mime.base import MIMEBase
from email.mime.image import MIMEImage
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def send_email(emailFrom,  emailTo, subject, 
                body , fileAttachment , password, html):
    """Input 
       ----------
            emailFrom: 'string'
                    Email of sender 

            emailTo: 'string or list of full email id'
                    Email of Reciever

            subject: 'string'
                    subject of email

            message: 'plain string or html string'
                    body of message

            fileAttachment: 'string'
                    absolute or relative path of fileAttachment

            html: Bool
                  True is message string is html

        Output:
            Send the mail"""

    #set parameters
    emailFrom = emailFrom
    emailTo = emailTo 
    fileAttachment = fileAttachment
    username = emailFrom
    password = password

    #start the mime object
    msg = MIMEMultipart()
    msg["From"] = emailFrom
    msg["To"] = emailTo
    msg["Subject"] = subject
    msg.preamble = subject

    #Add body to email
    if html:
        part = MIMEText(body, 'html')
    else:
        part = MIMEText(body, 'plain')

    msg.attach(part)

    ##if fileAttachment is present
    if fileAttachment !='' :
        # Guess the content type based on the file's extension. 
        ctype, encoding = mimetypes.guess_type(fileAttachment)
        if ctype is None or encoding is not None:
            ctype = "application/octet-stream"

        maintype, subtype = ctype.split("/", 1)

        # No guess could be made, or the file is encoded (compressed), so
        # use a generic bag-of-bits type.
        if maintype == "text":
            fp = open(fileAttachment)
            attachment = MIMEText(fp.read(), _subtype=subtype)
            fp.close()
        elif maintype == "image":
            fp = open(fileAttachment, "rb")
            attachment = MIMEImage(fp.read(), _subtype=subtype)
            fp.close()
        elif maintype == "audio":
            fp = open(fileAttachment, "rb")
            attachment = MIMEAudio(fp.read(), _subtype=subtype)
            fp.close()
        else:
            fp = open(fileAttachment, "rb")
            attachment = MIMEBase(maintype, subtype)
            attachment.set_payload(fp.read())
            fp.close()
            encoders.encode_base64(attachment)

        attachment.add_header("Content-Disposition", "attachment", filename=fileAttachment.split('\\')[-1])
        msg.attach(attachment)

    #send the mail 
    server = smtplib.SMTP("smtp.gmail.com:587")
    server.starttls()
    server.login(username, password)
    server.sendmail(emailFrom, emailTo.split(','), msg.as_string())
    print("Email sent successfully")
    server.quit()
