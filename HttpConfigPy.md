#http\_config.py : Standalone python HTTP daemon for learning mode !

# http\_config.py #

http\_config.py is a standalone HTTP server, based on BaseHTTPServer. Its goal is to be used during the LearningMode phase, to receive the to-be-blocked requests and generate whitelists for those requests.
During the LearningMode phase, naxsi will let all requests pass, and will also forward them to the location configured by **DeniedUrl**. As you guess, you're expected to make this location point to http\_config.py daemon.

http\_config.py will then receive all the to-be-blocked requests (false positives) and will generate & store whitelist rules (using BasicRule syntax) into a SQLite3 database. If you fire your browser at http\_config.py daemon, you be able to follow the number of exceptions (false positives) and by a simple "click", dump those rules to a predefined file (that should be included into naxsi's configuration via nginx's include directive) and issue a /etc/init.d/nginx reload.

Your configuration will be over when you did an exhaustive enough browsing session of your website (that MUST include form-filling, as it's the main source of false positives).

current stable :
**Current stable version has no support for multi-sites, use dev version instead**
```
usage: http_config.py --rules /path/to/naxsi_core.rules [-h] [--dst DST] [--db DB] [--cmd CMD] [--port PORT]
                      [-n] [-v V]
--rules is mandatory

Naxsi's learning-mode HTTP server. Might have to be run as root (yes scarry), if you want it to be able to perform /etc/init.d/nginx reload.

optional arguments:
  -h, --help   show this help message and exit
  --dst DST    Full path to the temp rule file. This file should be included
               in your naxsi's location configuration file. (default:
               /tmp/naxsi_rules.tmp)
  --db DB      SQLite database file to use. (default: naxsi_tmp.db)
  --cmd CMD    Command that will be called to reload nginx's config file
               (default: /etc/init.d/nginx reload)
  --port PORT  The port the HTTP server will listen to (default: 4242)
  -n           Run the daemon as non-root, don't try to reload nginx.
               (default: False)
  -v V         Verbosity level 0-3 (default: 1)
```

dev:
**Allows per-site rules handling**

```
$ ./http_config.py -h
usage: http_config.py [-h] [--dst DST] [--db DB] [--rules RULES] [--cmd CMD]
                      [--port PORT] [-n] [-v V]

Naxsi's learning-mode HTTP server. Should be run as root (yes scarry), as it
will need to perform /etc/init.d/nginx reload. Runs fine as non-root, but
you'll have to manually restart nginx

optional arguments:
  -h, --help     show this help message and exit
  --dst DST      Full path to the temp rule file. This file should be included
                 in your naxsi's location configuration file. (default:
                 /tmp/naxsi_rules.tmp)
  --db DB        SQLite database file to use. (default: naxsi_tmp.db)
  --rules RULES  Path to your core rules file. (default:
                 /etc/nginx/naxsi_core.rules)
  --cmd CMD      Command that will be called to reload nginx's config file
                 (default: /etc/init.d/nginx reload)
  --port PORT    The port the HTTP server will listen to (default: 4242)
  -n             Run the daemon as non-root, don't try to reload nginx.
                 (default: False)
  -v V           Verbosity level 0-3 (default: 1)
```

see [Compatibility](Compatibility.md) for requirements.


Well, let's fire HttpConfigPy (for naxsi < 0.44)/nx\_intercept so that it'll listen there (127.0.0.1:4242)


**If you are using naxsi >= 0.44, refer to http://code.google.com/p/naxsi/wiki/LearningMode_0_44 from here**




**http\_config.py is old & dead, replaced by nx\_intercept/nx\_extract**
```
# python http_config.py -h
usage: http_config.py [-h] [--dst DST] [--db DB] [--rules RULES] [--cmd CMD]
                      [--port PORT] [-n] [-v V]

Naxsi's learning-mode HTTP server. Should be run as root (yes scarry), or use sudo in the "restart" command (better), as it
will need to perform /etc/init.d/nginx reload. Should run fine as non-root,
but you'll have to manually restart nginx

optional arguments:
  -h, --help     show this help message and exit
  --dst DST      Full path to the temp rule file. This file should be included
                 in your naxsi's location configuration file. (default:
                 /tmp/naxsi_rules.tmp)
  --db DB        SQLite database file to use. (default: naxsi_tmp.db)
  --rules RULES  Path to your core rules file. (default:
                 /etc/nginx/naxsi_core.rules)
  --cmd CMD      Command that will be called to reload nginx's config file
                 (default: /etc/init.d/nginx reload)
  --port PORT    The port the HTTP server will listen to (default: 4242)
  -n             Run the daemon as non-root, don't try to reload nginx.
                 (default: False)
  -v V           Verbosity level 0-3 (default: 1)

```

I'll just stick with the default settings, here we go :
```
#./http_config.py --cmd "/usr/sbin/nginx -s reload"  -v 3
Creating (new) database.
Finished DB creation.
Touched TMP rules file.
done.
Starting server, use <Ctrl-C> to stop
```

or :
```
$./http_config.py --cmd "sudo /usr/sbin/nginx -s reload"  -v 3
Creating (new) database.
Finished DB creation.
Touched TMP rules file.
done.
Starting server, use <Ctrl-C> to stop
```

Yes, you need to use sudo or launch it as root. Why ? Well, I want my configuration to be easy. By launching the daemon as root/using sudo, it has the capability to reload nginx by on its own. This is only a facility, and should be done with huge care (here, it'll only listen on 127.0.0.1 so it's kinda ok).

Now we are ready !

To make it clear, I configured nginx as a local reverse proxy for my company's website, and I modified my /etc/hosts file, so that www.nbs-system.com points to 127.0.0.1. In this way, I can configure and test NAXSI without any effect for the other users, I will be the only one impacted.


So I can now fire my browser at www.nbs-system.com, and it will actually hit 127.0.0.1:80, where my nginx+naxsi is waiting for me !

Whenever an exception (false positive) is catched, you see things appear into the HttpConfigPy console. If you want to be sure that your setup is correctly working, just add an attack pattern and see if something is printed in the HttpConfigPy console.

Ok, so I now load the main page of my company's website, browse a bit, and I see a lot of things being displayed in HttpConfigPy console's. This means that there are some false positives, but don't worry, that's ok, even normal !

To see how many, I will just open 127.0.0.1:4242 in my browser to access the HttpConfigPy interface :
```
You currently have 9.0 rules generated by naxsi.
You should reload nginx's config WRITE AND RELOAD
You have a total of 218.0 exceptions hit.
Authorizing :
rule 1005(|) authorized on url for argument 'cookie' of zone HEADERS
rule 1010(() authorized on url for argument 'cookie' of zone HEADERS
rule 1011()) authorized on url for argument 'cookie' of zone HEADERS
rule 1308(() authorized on url for argument 'cookie' of zone HEADERS
rule 1309()) authorized on url for argument 'cookie' of zone HEADERS
rule 1013(') authorized on url for argument 'cookie' of zone HEADERS
rule 1306(') authorized on url for argument 'cookie' of zone HEADERS
rule 1315() authorized on url for argument 'cookie' of zone HEADERS
rule 1000() authorized on url /wp-content/themes/nbswdp/images/bkg-selected-slider.png for zone URL
```

It means that a total of 218 request would have been blocked, and 9 rules were generated. Actually, that's (once again) perfectly normal. With no whitelists, I will just click the "WRITE and RELOAD" link. What it will do is :
  * Write the generated rule to /tmp/naxsi\_rules.tmp
  * Reload NGINX

After you click the link, the page will display this :
```
You currently have 0.0 rules generated by naxsi.
You have a total of 218.0 exceptions hit.
Authorizing :
```

Let's have a look at our generated rules :
```
root@zeroed:/tmp# cat naxsi_rules.tmp 
BasicRule wl:1005 "mz:$HEADERS_VAR:cookie" ;
BasicRule wl:1010 "mz:$HEADERS_VAR:cookie" ;
BasicRule wl:1011 "mz:$HEADERS_VAR:cookie" ;
BasicRule wl:1308 "mz:$HEADERS_VAR:cookie" ;
BasicRule wl:1309 "mz:$HEADERS_VAR:cookie" ;
BasicRule wl:1013 "mz:$HEADERS_VAR:cookie" ;
BasicRule wl:1306 "mz:$HEADERS_VAR:cookie" ;
BasicRule wl:1315 "mz:$HEADERS_VAR:cookie" ;
BasicRule wl:1000 "mz:$URL:/wp-content/themes/nbswdp/images/bkg-selected-slider.png|URL" ;
```

And now, if I reload the home page of my company's website, the number of exception won't grow anymore. It means that the whitelists that were generated are accurate enough.

I will continue browsing though the website to see wether there is other false positives. Generally, most of the false positives will be triggered in the first two pages, because they are caused by funky URL rewritting, and the way your cookies are created.