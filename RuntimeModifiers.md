naxsi dynamic configuration (aka nginx vars)

Since 0.49, naxsi supports a limited set of variables that can override or modify its behavior.

  * naxsi\_flag\_learning : If present, this variable will override naxsi learning flag ("0" to disable learning, "1" to enable it).
  * naxsi\_flag\_post\_action : If present and set to "0" this variable may be used to disable post\_action in learning mode.
  * naxsi\_flag\_enable : if present, this variable will override naxsi "SecRulesEnabled" ("0" to disable naxsi, "1" to enable).
  * naxsi\_extensive\_log : If present (and set to "1"), this variable will force naxsi to log the CONTENT of variable matching rules (see notes at bottom).

## Gentle reminder ##

It is important to know that naxsi operates at the REWRITE phase of nginx. Thus, setting those variables directly in the location where naxsi is present is ineffective (as naxsi will be called before variable set is effective).

This is correct:

```
set $naxsi_flag_enable 0;
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

With that said, you can use the power of nginx, lua, **to change naxsi's behavior. The presence of these variables will enable/disable learning mode, naxsi itself or force extensive logging.**

You can thus do things naxsi is usually not able to, like modifying its behavior according to (nginx) variables set at run-time :

```
# Disable naxsi if client ip is 127.0.0.1
if ($remote_addr = "127.0.0.1") {
 set $naxsi_flag_enable 0;
}
```

Those variables can as well be set from lua scripts (see nginx's mod\_lua).

## naxsi\_flag\_learning ##

If naxsi\_flag\_learning variable is present, this value will override naxsi's current static configuration regarding learning mode.

```
if ($remote_addr = "1.2.3.4") {
set $naxsi_flag_learning 1;
}

location / {
...
}
```

## naxsi\_flag\_post\_action ##

This option may be used if you don't intend to use live learning at all and only perform logs learning. Or, if you intend to run a learning daemon for live learning on a public site (oh my) and you want to pre filter your learning sources.

You can then disable the post\_action that naxsi usually does while in learning mode. Trying to set it to "1" is useless and/or dangerous in all situations.

## naxsi\_flag\_enable ##

If naxsi\_flag\_enable variable is present and set to 0, naxsi will be disabled in this request. This allows you to partially disable naxsi in specific conditions.

To completely disable naxsi for "trusted" users :

```
set $naxsi_flag_enable 0;

location / {
...
}
```

## naxsi\_extensive\_log ##

If present (and set to “1”), this variable will force naxsi to log the CONTENT of variable matching rules.

Because of potential performances impacts of naxsi\_extensive log, use it with caution. Naxsi will log those to nginx’s error\_log, ie:

NAXSI\_EXLOG: ip=%V&server=%V&uri=%V&id=%d&zone=%s&var\_name=%V&content=%V