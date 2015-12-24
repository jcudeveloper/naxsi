#Location where denied requests will be redirected. While in LearningMode, to-be-blocked requests will also be sent here, as well as to the original target.

# DeniedUrl #

DeniedUrl is part of naxsi's configuration. It **must** point to an existing nginx's location :
```
DeniedUrl "/RequestDenied";
```


```
 location /RequestDenied {
     proxy_pass http://127.0.0.1:4242;
   }
```

Blocked requests will be sent there, so feel free to put whatever you want here, from a simple
```
return 403;
```

to a proxy\_pass to your own software for NIDS / reporting features :
```
proxy_pass http://xx.xx.xx.xx:zz;
```

The request will contain the full original request, as well as some complementary information, such as details about which rule(s) matched on which part(s) of the request.

You might as well want to use a php page with a captcha to help cathing false positives. You will find an example here :

https://code.google.com/p/naxsi/source/browse/tags/0.41/contrib/fp-reporter/fp-reporter.php


You might as well want to allow only a restricted set of users to perform Learning onto naxsi : http://blog.memze.ro/?p=81