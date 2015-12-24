# Naxsi's learning mode #

Globally, you can "auto generate" your rules by two main methods :
  * Using a python script that will parse nginx's **log files**.
  * Using a standalone python HTTP daemon. (prefered method)


# Generating rules from nginx's log files (for versions < 0.44) #

naxsi write details about to-be-blocked requests in nginx's error log file. After doing a navigation session, you can use the **rules\_transformer.py** tool to parse you nginx's error log and generate naxsi's whitelists from this file. **rules\_transformer.py** will then write generated whitelists to **/tmp/RT\_naxsi.tmp**. If you include this file into your location's configuration, then exception raised while doing the initial browsing session will then be whitelisted.


LearningMode is enabled when `LearningMode;` is present in your location's configuration.


# Generating rules **on the fly** (for versions < 0.44) #

This is one of the great strengths of naxsi ! You can generate your whitelistes while browsing, without (nearly) touching a shell. As explained earlier, while in **LearningMode**, naxsi won't block any requests, but it will as well post them (using nginx's post\_action mechanism) to the **DeniedUrl** location. To take maximum profit from this mechanism, you have a standalone python HTTP daemon provided _http\_config.py_. This daemon will be pointed to by your **DeniedUrl** so that it will receive all the exception catched while in learning mode. You can as well access it with your browser, and it will display you how many whitelists have been generated and so on, even letting you "reload" nginx's configuration with the new generated whitelists.

To summarize the global process should be :
> - Start **http\_config.py**
_Listens, by default, on port 4242. Start it as root preferably, if you want it to have the availability to reload nginx._

Another option is to use some iptables DNAT/SNAT trick to make nginx run as 'low privilege' user, on a high port, and redirecting port 80/tcp to it with iptables.

> - Point your **DeniedUrl** location at it :
```
location /RequestDenied {
 proxy_pass http://127.0.0.1:4242;
} 
```
> - Put Naxsi in learning mode (simply add `LearningMode;` to your location's config.

> - Include your to-be-generated rules file (**/tmp/naxsi\_rules.tmp** by default) in your nginx's location config :
```
include "/tmp/naxsi_rules.tmp";
```
> - Restart nginx !

> - Start browsing

> - Open a browser to 127.0.0.1:4242, you should see exception and generated rules count growing.

> - Whenever you want, click on the **WRITE\_AND\_RELOAD** link. It will write the generated rules to a file and reload nginx.
_You can now have a look at your **/tmp/naxsi\_rules.tmp** (or wherever you set it) and you will see the generated rules, like :
```
BasicRule wl:1309 "mz:$HEADERS_VAR:cookie" ;
BasicRule wl:1313 "mz:$HEADERS_VAR:cookie" ;
BasicRule wl:1015 "mz:$URL:/skin/m/...
```_

> - Continue your browsing

> - When you see that exception / generated rules count stops to grow, and you think you did an exhaustive enough browsing session, it means that your NAXSI config is over !