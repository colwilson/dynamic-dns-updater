dynamic-dns-updater
===================

Script to check if your provider has changed you IP address and call a callback if it has.

This script is intended for the following use:

* You have a server in the shed which you want to be visible from as yourdomain.com
* Unfortunately you are on a broadband and your IP providers sometimes changes the IP without warning
* So you have yourdomain.com pointed at [FreeDNS](https://freedns.afraid.org) and use their dynamic service to point at your IP
* You need a script to run on a crontab to check if your IP changes and tell FreeDNS if it does
* You'd also like the change emailed to you

##Configuration

###Install the required modules

<pre>
pip install IPy mailer request
</pre>

###Crontab

Since the script is meant to run on a crontab you will need to define some variables in your crontab:

<pre>
MAILTO=my.email.address@yourdomain.com
IP_UPDATE_URL=http://freedns.afraid.org/dynamic/update.php?mycallback_oooo==
GMAIL_USER=mygmailuser
GMAIL_PASS=mygmailPass1

# synch the dynamic IP for freedns
*/5 * * * * /usr/bin/python ~/dynamic-ip.py >> /dev/null 2>&1

</pre>

##By the way...

As you can I'm using gmail to send myself emails, but you could configure
the mailer module in the script to use whatever you wish.

That callback could go anywhere you want, not just FreeDNS necessarily.

I'd be glad to see any improvements you might suggest.
