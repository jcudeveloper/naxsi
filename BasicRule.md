#BasicRule is used for whitelisting (or rule writting) inside a location.

# BasicRule #

BasicRule(s) are present at the location's configuration level. It is (most of the time) used to create whitelists. BasicRule syntax is :
```
BasicRule wl:ID [mz:[$URL:target_url]|[match_zone]|[$ARGS_VAR:varname]|[$BODY_VARS:varname]|[$HEADERS_VAR:varname]|[NAME]]
```

**wl:ID** (WhiteList): Which rule ID(s) are whitelisted. Possible syntaxes :
  * wl:0 : Whitelist all rules
  * wl:42 : Whitelist rule #42
  * wl:42,41,43 : Whitelist rules 42, 41 and 43

**mz:** (MatchZones): Specify the conditions to match for the rule to be whitelisted. A MatchZone must be specified in a nginx location                     context to enable a rule. MatchZone can contain one or several elements, separated by '|' :

  * **$URL:/bar** : Only apply the whitelist is the target URL is /bar.

> _**Beware**, $URL:/x must be considered as an "adjective" to
> a whitelist. It just tells naxsi that the WL will apply ONLY
> when URL is "/x". It does not indicate where the exception will
> happen (unlike the others)._


  * **match\_zone** : Apply the whitelist to one (or several zones). Valid zones are :
    * ARGS : GET args
    * HEADERS : HTTP Headers
    * BODY : POST args
    * URL : The URL (before '?')
    * NAME : It's a suffix, indicating that the target element is the NAME of the var, not its content. For example a whitelist targetting BODY|NAME means that the exception were triggered in the "name" of some POST (BODY) variables.

  * **$ARGS\_VAR:bar** : Only apply the whitelist to the GET argument called 'bar'
  * **$BODY\_VAR:bar** : Only apply the whitelist to the POST argument called 'bar'
  * **$HEADERS\_VAR:bar** : Only apply the whitelist to the HTTP header called 'bar'

Examples :


Totally disable rule #1000 for this location :
```
BasicRule wl:1000; 
```
Disable rule #1000 in GET argument named 'foo' :
```
BasicRule wl:1000 "mz:$ARGS_VAR:foo";
```
Disable rule #1000 in GET argument named 'foo' for url '/bar' :
```
BasicRule wl:1000 "mz:$ARGS_VAR:foo|$URL:/bar";
```
Disable rule #1000 in all GET arguments for url '/bar' :
```
BasicRule wl:1000 "mz:$URL:/bar|ARGS";
```
Disable rule #1000 in all GET argument NAMES (only name, not content) :
```
BasicRule wl:1000 "mz:ARGS|NAME";
```