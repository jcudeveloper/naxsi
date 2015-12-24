naxsi dynamic configuration (aka nginx vars)

Since 0.49, naxsi supports a limited set of variables that can override or modify its behavior.

  * naxsi\_flag\_learning : If present, this variable will override naxsi learning flag ("0" to disable learning, "1" to enable it).
  * naxsi\_flag\_post\_action : If present and set to "0" this variable may be used to disable post\_action in learning mode.
  * naxsi\_flag\_enable : if present, this variable will override naxsi "SecRulesEnabled" ("0" to disable naxsi, "1" to enable).
  * naxsi\_extensive\_log : If present (and set to "1"), this variable will force naxsi to log the CONTENT of variable matching rules (see notes at bottom).


It is important to remind that naxsi operates at the REWRITE phase of nginx. Thus, setting those variables directly in the location where naxsi is present is ineffective (as naxsi will be called before variable set is effective).

This is correct:

```
set $naxsi_flag_enable 0;
location / {
...
}
```


This is correct as well:
```
if ($remote_addr = "127.0.0.42") {
 set $naxsi_flag_learning 1;
}
location / {
...
}
```

```
if ($uri = "/foobar") {
 set $naxsi_extensive_log 1;
}
location / {
...
}
```



But this is wrong:
```
location / {
         set $naxsi_flag_learning 1;
 ...
}
```


## special note on naxsi\_extensive\_log ##

If present (and set to “1”), this variable will force naxsi to log the CONTENT of variable matching rules.

Because of potential performances impacts of naxsi\_extensive log, use it with caution. Naxsi will log those to nginx’s error\_log, ie:

NAXSI\_EXLOG: ip=%V&server=%V&uri=%V&id=%d&zone=%s&var\_name=%V&content=%V