# Denied requests and white list generation #

When a user request is denied, he will be (internally) redirected to the page defined in the configuration :

`DeniedUrl "/RequestDenied";`

This page will receive detailed informations on the rules that matched (it's logued in log files too), as well as both the request and the user context, without giving information to the user (thanks to nginx internal redirects). Actually the page at /RequestDenied will be called with arguments, like :

`server=xxxx&uri=/vulnerable.php&ip=127.0.0.1&zone0=ARGS&id0=1010&var_name0=foo1&zone1=ARGS&id1=1011&...`

If you have a closer look at the above URL, you will understand that the following information will be transmitted to the forbidden page :

  * Which rule matched on which argument, in which part of the request (ARGS, BODY, URL, HEADERS ...)
  * Original URL and hostname
  * Client IP adress

This information is given for both statistics generation purpose, as well as white list generation purposes.

Yes, actually that's a very important aspect of Naxsi : as it is heavily relying on whitelist for configuration, the easiest the whitelist generation is, the easier the configuration is ! The thing being that the DeniedUrl page receives enough information to generate a set of whitelisting rules that will allow the request that was blocked to be allowed in the future.

To make it clear : you can generate the whole Naxsi configuration, only by navigating to the site, or even better, by using a clever crawler !
When you will do a navigation session on the website you want to create rules for, if you are in "LearningMode", some requests might be (and will be) tagged as blocked. They should be blocked, because, for example, the developers (damn!) decided to massively use '|' for URL rewritting, and Naxsi will dislike this if you don't tell it htat '|' is fine.

So, as you are in learning mode (but the idea is the same when LearningMode is disabled), Naxsi will log the fact that the request was blocked because of the presence of multiples '|' in the URL. Then, with a simple script (a python script, provided), you can parse the log files and generate the appropriate white rules to allow legitimate (false positive) requests.

The tricky part when talking about Naxsi and its whitelist, is when we come to sites that allows a LOT of wide user input : Comments, Registration forms and things like this. For this, either a carefull navigation, submitting real content is required (so that Naxsi will trigger every plausible rule on each kind of form field) or the usage of a clever crawler is required.
In the worst case, it will require to do a real navigation session to generate the appropriate white lists.