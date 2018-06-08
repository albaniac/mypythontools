#!/usr/bin/env python
import datetime
import sys
import os
import socket
import subprocess
from os.path import basename
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.MIMEBase import MIMEBase
from email import encoders
from smtplib import SMTP_SSL as SMTP
################################### Initialisation des variables ################################### 
SMTPserver = "smtp.xxx.xxx"
sender = "xxxx@xxxx.xxx"
destination = "xxxx@xxxx.xxx"
USERNAME = "xxxxx"
PASSWORD = "xxxxxx"
text_subtype = 'html'
subject="Sauvegarde "+socket.gethostname()
content=""
#############"
date = str(datetime.date.today().year)+"-"+str('{:02d}'.format(datetime.date.today().month))+"-"+str('{:02d}'.format(datetime.date.today().day))
#date = "2018-05-13"
boxtoclone = socket.gethostname()
filename = date+"_"+boxtoclone+".img.gz"
file = "<path /xxx/xxx/xx/>"+filename
bashcommand="sudo dd if=/dev/mmcblk0 bs=4M | sudo gzip -1 -| sudo dd of="+file+" && sync"
################################### Lancement de la commande ###################################
output = subprocess.check_output(['bash','-c', bashcommand])
content = output
try:
    #msg = MIMEText(content, text_subtype)
    msg = MIMEMultipart()
    msg['Subject']= subject
    msg['From']   = sender # some SMTP servers will do this automatically, not all
    msg.attach(MIMEText(content))

    conn = SMTP(SMTPserver)
    conn.set_debuglevel(False)
    conn.login(USERNAME, PASSWORD)
    try:
        conn.sendmail(sender, destination, msg.as_string())
    finally:
        conn.quit()

except Exception, exc:
    sys.exit( "mail failed; %s" % str(exc) ) # give a error message
