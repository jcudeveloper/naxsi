#Handling Whitelists involving free-text user inputs

## Hands On ##

Websites often support search features and more generally, textboxes where the user might have the freedom to use uncommon characters (forums, comments, forms etc.)

For example, on your search box, because you **know** your site is buggy and suffers from an XSS, you might decide not to allow any uncommon input. If you decide to do so, naxsi don't need to "learn" about this user input, and user will still be free to use all characters that are not tagged by naxsi.

On the other hand, you might want to allow your users to use the ' character in your search box (but not the " because of this damn xss). If you want to do so, type a string containing a ' in your search box (while in learning mode). This will tell naxsi you want to allow this, and you will see it appear in your whitelists.

And, in some case, because you have a blind trust in your code, you might want to let the user be free to type **anything** here and there. (Or because your site is about MySQL, and some false positives about SQL Injections might pop :p). When you want to do so, you can add a rule like
this to your naxsi\_core.rules (or /etc/nginx/yoursite.rules).

```

BasicRule id:0 "mz:ARGS|BODY" "str:123FREETEXT" "s:BLOCK";
```

Doing so will allow you, to perform one training for each possible user input. In our search box, we will now type "123FREETEXT". As the rule above states, any variable in ARG (GET) or BODY (POST/PUT) containing "123FREETEXT" will match. The rule has id 0 (which **usually** means all rules). We are here abusing naxsi simplicity, as we ask him to write whitelists for all rules. Doing so means that naxsi will never block a request because of the content of this variable.

In nx\_extract.py, you will indeed see your whitelist :

```

# means allow 'everything' on GET argument "s" for URL /
BasicRule wl:0 "mz:$URL:/|$ARGS_VAR:s";
```

wl:0 tells naxsi to ignore all rules on this var. Here the rule is quite restrictive, as it only allows search from '/', but doing multiple searches or playing with page\_hit (or doing yourself the simplification) will handle this.

For sure, don't let your :
BasicRule id:0 "mz:ARGS|BODY" "str:123FREETEXT" "s:BLOCK";
In production :)