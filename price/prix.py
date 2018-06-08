#!/usr/bin/env python
# encoding: utf-8
import difflib
import requests
import bs4
import csv
from datetime import date, datetime, timedelta
from time import gmtime, strftime, localtime
import os, re, sys
import unicodedata
from smtplib import SMTP_SSL as SMTP
from email.mime.text import MIMEText
from shutil import copyfile
from operator import itemgetter
# Variales autres
scriptpath=os.path.dirname(os.path.realpath(sys.argv[0]))+"/"
mail=[]
with open(scriptpath+"mail", "r") as f :
    for line in f.readlines():
        mail.append(line.strip(' \t\n\r'))

SMTPserver = mail[0]
sender = "'" + mail[1] + "'"
destination = [ mail[2] ]
USERNAME = mail[3]
PASSWORD = mail[4]
text_subtype = 'plain'
subject="Price evolution"
content=""

# Cleaners
def remove_all_whitespace(x):
    """
    Returns a string with any blank spaces removed.
    """
    try:
        x = x.replace(" ", "")
    except:
        pass
    return x

def trim_the_ends(x):
    """
    Returns a string with space on the left and right removed.
    """
    try:
        x = x.strip(' \t\n\r')
    except:
        pass
    return x

def remove_unneeded_chars(x):
    """
    Returns the string without the unneeded chars
    """
    try:
        x = x.replace("$", "").replace("RRP", "")
        x = x.replace("€", "").replace("RRP", "")
    except:
        pass
    return x

with open(scriptpath+"entre", "r") as f :
    for line in f.readlines():
        entre = trim_the_ends(line).split(' ')
        URL=entre[0]
        price_tag=entre[1]
        name_tag=entre[2]
        name_search=entre[3]
        print "URL=" + URL
# Grab the web page on the Packt website
# Use response to get the page
        response = requests.get(URL)
# Save the response to the soup so we can parse it
        soup = bs4.BeautifulSoup(response.text, "html.parser")
        name_tag = name_tag.split(',')
        price_tag = price_tag.split(',')
        price_box = soup.find_all(price_tag[0], attrs={price_tag[1]:price_tag[2]})
        name_box = soup.find_all(name_tag[0], attrs={name_tag[1]:name_tag[2]})
# Append the pricing data to the CSV file
        datalist = []
        file = scriptpath + (strftime("%Y-%m-%d %H:%M", localtime()) + " - " + name_search)
        with open(file, 'a') as fp:
            a = csv.writer(fp, delimiter=';')
            i = 0
            if not os.path.isfile(file) or os.stat(file).st_size == 0:
                while( i < len(name_box) ):
                    data = [[unicodedata.normalize('NFKD', trim_the_ends(name_box[i].text)).encode('ascii','ignore'),
                              unicodedata.normalize('NFKD', remove_all_whitespace(trim_the_ends(price_box[i].text))).encode('ascii','ignore') ]]
                    datalist.append(data)
                    i += 1
                datalist = sorted(datalist, key=itemgetter(0))
                a.writerows(datalist)

        try:
            with open(scriptpath + "previous - "+ name_search, 'r') as yesterday:
                with open(file, 'r') as today:
                    diff = difflib.unified_diff(
                        yesterday.readlines(),
                        today.readlines(),
                        fromfile='yesterday',
                        tofile='today',
                        n=0,
                     )
                    for line in diff:
                        content = content + URL + "\n"
                        break
                    for line in diff:
                         sys.stdout.write(line)
                         content = content + line
        except IOError as e:
              print("Previous file doesn't exist ?")

        copyfile(file, scriptpath + "previous - "+ name_search)

if not len(content) == 0:
    try:
        msg = MIMEText(content, text_subtype)
        msg['Subject']= subject
        msg['From']   = sender # some SMTP servers will do this automatically, not all

        conn = SMTP(SMTPserver)
        conn.set_debuglevel(False)
        conn.login(USERNAME, PASSWORD)
        try:
            conn.sendmail(sender, destination, msg.as_string())
        finally:
            conn.quit()

    except Exception, exc:
sys.exit( "mail failed; %s" % str(exc) ) # give a error message
