#FAQ.

**I compiled naxsi from source, I enabled NAXSI, but it doesn't seem to filter requests ?**

Did you put NAXSI directives first in your location configuration and ./configure ?
You **MUST** put NAXSI's directives first your location configuration.

**How to limit learning mode to some specific IPs ?**

The easiest way to do so is to rely on nginx's HttpAllowModule.
http://wiki.nginx.org/HttpAccessModule
Using this module (default in nginx), you can simply put in your location specified by DeniedUrl :

```
        location /RequestDenied {
                 allow 127.0.0.1;
                 allow x.x.x.x;
                 deny all;
                 proxy_pass http://127.0.0.1:4242/;                                                                                                               
                 }

```

You can as well setup different vhosts (with associated locations). And define some vhost to have learningmode, and some others without learningmode.

**How to test that naxsi is working ?**

Setup your RequestDenied as follow :


```
        location /RequestDenied {
                return 500;                                                                                                           
        }
```

Check that LearningMode is disabled, and issue a request like :

```
http:/.../?a=<>
```


You should get a 500 from NGINX, and get an entry in your nginx error log, in the form :


```
NAXSI_FMT: ....
```


**I downloaded / installed debian package, but I cannot find learning daemon ?**


Naxsi learning daemons are into separate packages for most distributions. If you cannot find it, get it from the SVN, here :
http://code.google.com/p/naxsi/source/browse/#svn%2Ftrunk%2Fcontrib%2Fnaxsi-ui
or
```

svn checkout http://naxsi.googlecode.com/svn/trunk/contrib/naxsi-ui naxsi-ui
```

  * How can I get statistics over a long time 

nx\_intercept -l option allows multiple filenames.
Data will then be concatenated.


  * Naxsi interface is empty 

Remember that naxsi (nx\_extract) interface is only fed by nx\_intercept.
So, run nx\_intercept first. When it will catch some exceptions, you will see lines like this appear :
```

[+] drop and creating new tables
/tmp/naxsi-0.46-1/contrib/naxsi-ui/nx_parser.py:21: Warning: Unknown table 'rules'
self.cursor.execute("DROP TABLES IF EXISTS rules")
...
```

Once you see this, you can safely start nx\_extract.

If you cannot make it work, and naxsi is already in learning mode, you can as well generate whitelists / statistics from nginx error log, see LearningFromLogFiles.

**Which version of naxsi is suitable for which nginx version ?**

All naxsi version should work on **ALL** nginx version, except very very old version (< 0.8.54).

**nx\_intercept does not seem to receive exceptions, and database is empty**

Check that you ONLY have a proxy\_pass directive in your /RequestDenied. No return, no root etc. If you cannot make it work, please use LearningFromLogFiles.

**nx\_intercept says it got exceptions, but I cannot get any whitelists**

When this happens, check that you did not forgot to include your naxsi\_core.rules in nginx.conf (see Howto for details).