#!/usr/bin/env python
import sys
import os
import random
import pickle
import logging
import requests
import mailer
from IPy import IP as check_ip

fh = logging.FileHandler('external-ip.log')
fh.setLevel(logging.INFO)
fh.setFormatter(logging.Formatter('%(asctime)s - %(message)s'))

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
logger.addHandler(fh)


MY_EMAIL        = os.environ['MAILTO']
IP_UPDATE_URL   = os.environ['IP_UPDATE_URL']
GMAIL_USER      = os.environ['GMAIL_USER']
GMAIL_PASS      = os.environ['GMAIL_PASS']

PICKLE          = "/tmp/external-ip.pickle"
IP_SERVICE_URLS = [
                    'http://automation.whatismyip.com/n09230945.asp',
                    'http://bot.whatismyipaddress.com/'
                  ]

def email(subj, body):
    message = mailer.Message()
    message.From = message.To = MY_EMAIL
    message.Subject = subj
    message.Body = body
    sender = mailer.Mailer(
        host='smtp.gmail.com',
        port='587',
        use_tls=True,
        usr=GMAIL_USER,
        pwd=GMAIL_PASS
    )
    r = sender.send(message)

    
def main ():
    ip = None
    random.shuffle(IP_SERVICE_URLS)
    
    for url in IP_SERVICE_URLS:
        r = requests.get(url)
        if r.status_code == 200:
            try: # make sure we get a usable ip returned
                ip = r.text
                check_ip(ip)
            except:
                msg = "IP service response is weird"
                logging.info(msg)
                email(msg, r.text)
                continue
                
            try: # again, check for a usable ip
                last_ip = pickle.load(open(PICKLE, "rb" ))
                check_ip(last_ip)
            except:
                last_ip = '0.0.0.0'

            if last_ip != ip: # has the ip changed?
                msg = "IP has changed from %s to %s" % (last_ip, ip)
                logging.info(msg)
                pickle.dump(ip, open(PICKLE, "wb"))
                r = requests.get(IP_UPDATE_URL)
                logger.info(r.text)
                email(msg, r.text)
            else:
                logger.debug("IP is %s from %s" % (ip, url))
            break


if __name__ == '__main__':
    try:
        main()
        sys.exit(0)
    except KeyboardInterrupt, e: # Ctrl-C
        raise e


