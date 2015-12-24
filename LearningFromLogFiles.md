#Performing learning from log files

# Why, and how does it work ? #

If you have some legitimate traffic on your website, or if you are not in a rush, you can perform passive learning from nginx's log files.

The idea behind passive learning is to setup your naxsi+nginx in LearningMode, and to put a simple "return 200;" in your RequestDenied.
In this way, your users won't be blocked (as naxsi is in learning mode), but the potential exceptions will be catched by naxsi (as it still inspects the HTTP traffic).

When doing passive learning, you don't need nx\_intercept to run as a daemon, as naxsi will write all the exceptions signatures into nginx's error\_log.

After a few hours or a few days (depending on how many users you have), you will be able to use this error\_log to generate whitelists. To do so, simply inject your error\_log into nx\_intercept database :
```

python nx_intercept.py -c naxsi-ui-learning.conf -l /var/log/nginx/mysite_error.log
```

Here, I decided to use SQLite type database, as we won't need concurrent access :

```

# Revelant part of the configuration file
[sql]
dbtype = sqlite
username = root
password =
hostname = 127.0.0.1
dbname = naxsi_sig
```

We can then fire nx\_extract to get the whitelists :

```

python nx_extract.py -c naxsi-ui-learning.conf
```

Then, if we connect on 127.0.0.1:8081 (default nx\_extract.py port), and go to the "Generate Whitelists" page, you should get your whitelists.

Alternatively, you can use :
```

python nx_extract.py -c naxsi-ui-learning.conf -o
```

To get whitelist printed on stdout.