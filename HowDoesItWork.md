# How does Naxsi work? #

Naxsi relies on two separate configuration parts:

  * Core Rules: Located at HTTP server level configuration.
  * White Lists & Specific Rules: Located at the HTTP location level configuration.

The first one is what we called 'core rules'.
It's a set of rules that will contain all characters or regular expression
that will increase the score of the request, for example :

`MainRule "str:<" "msg:html open tag" "mz:ARGS|URL|BODY|$HEADERS_VAR:Cookie" "s:$XSS:8" id:1302;`

This rule, will match on `<` character (`str:<`), and will increase
the score associated to the XSS threat (`s:$XSS:8`). This pattern will be matched
against various zones of the request: ARGS (GET arguments), URL (the full URI),
> BODY (POST arguments), as well as Cookie http header. Each rule is associated to unique ID (here, 1302),
that is used for white listing.
There is not "many" core rules (34 at the time of writing), and this set
should not evolve significantly.

On the other hand, we have a "local" configuration, which is to be defined
"per site" (as Naxsi main goal is to work with NGINX as a reverse proxy), and
which will define "how strict" the security policy of the site will be, as well
as putting exceptions (white lists) according the site specificities :


```
# Define to which Nginx "location" the user will be redirected when a request is denied
DeniedUrl "/RequestDenied";

# Whitelist '|', as it's used on the /report/ page, in argument 'd'
BasicRule wl:1005 "mz:$URL:/report/|$ARGS_VAR:d";

# Whitelist ',' on URL zone as it's massively used for URL rewritting !
BasicRule wl:1008 "mz:URL";

# Check rules
CheckRule "$SQL >= 8" BLOCK;
CheckRule "$RFI >= 8" BLOCK;
CheckRule "$TRAVERSAL >= 4" BLOCK;
CheckRule "$XSS >= 8" BLOCK;
```

Let's see this configuration again to clarify things :

  * 'BasicRule' : This directive is used here to white list some rules.
As you can see (and expect !) you can be more or less slacky.
For example, there is a directive (BasicRule wl:1008 ...) that will totally disable the rule 1008 checking against URL. This rule is normally matching the ',' character.

On the other hand, you can make extremely precise rules, as this one :

`BasicRule wl:1005 "mz:$URL:/report/|$ARGS_VAR:d";`

In this last example, we are white listing a rule, but only on one specific argument of one specific web page (the argument named 'd' of the page'/report/'). Don't be frighten by the rules syntax, in most cases, you won't have to write it, Naxsi will generate them during your 'learning phase' (see: LearningMode) !

As stated earlier, "local" configuration is also used to decide how
"strict" one site (or one part of one site) will be, that is, what is
the maximal tolerated page score before a request is denied :

`CheckRule "$SQL >= 8" BLOCK;`

This directive tells Naxsi that every request having a 'SQL' score superior
or equal to 8 will be denied.