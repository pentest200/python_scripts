import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email import encoders

server=smtplib.SMTP('smtp.gmail.com', 587)     # ("server",port)
server.ehlo()         # identification
server.starttls()     # Upgrade connection to secure
server.ehlo()

#login
with open('password.txt','r') as f:
    password=f.read().strip()

server.login('your123@gmail.com',password) # if using gmail use app password(16 letter)

#creating message
message = MIMEMultipart()
message['From'] = 'your123@gmail.com'
message['To'] = 'xyzclient@gmail.com'
message['Subject'] = 'Regarding Scholarship query'

with open('message_body.txt','r') as f:
    msg=f.read()

message.attach(MIMEText(msg,'plain'))

#attaching files
file = 'attachment.jfif'
attachment = open(file,'rb')  #read binary 

payload = MIMEBase('application','octet-stream')    #create a MIME part for binary data
payload.set_payload(attachment.read()) 
encoders.encode_base64(payload)         #enconding the content
payload.add_header('content-Disposition', f'attachment; file={file}')      #tell email clients this is an attachment
message.attach(payload)

text = message.as_string()
server.sendmail('your123@gmail.com','xyzclient@gmail.com',text)
