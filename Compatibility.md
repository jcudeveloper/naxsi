#Naxsi compatibility.

## Nginx compatibility ##
naxsi is proven to work with nginx >= 0.8.X

(known compilation error on 1.1.12 : nginx PCRE API updated, but not version #define)

## Naxsi "core" dependencies ##
  * lib pcre (naxsi sometimes on regex for pattern matching)
  * lib ssl (if you want SSL, but this is required by nginx as well)

## nx\_intercept/nx\_extract dependencies ##
  * python >= 2.5 or 3
  * twisted
  * mysql

## nx\_util ##
  * python >= 2.6

## Naxsi is compiling/working on ##
  * debian linux : yes
  * netbsd : yes
  * freebsd : yes
  * openbsd : newly packaged, should be working, waiting for further tests for confirmation.

If you try naxsi on other systems / distributions, feel free to drop us a word !

## Testing if naxsi is working on your system ##

naxsi, as many other softwares, comes with test units.
This allow you to perform tests onto nginx+naxsi to confirm it's working
with your distribution/libraries versions/whatever.

These test units rely on nginx::test and prove. You will find more details if needed on this awesome blog :

http://www.nginx-discovery.com/2011/03/day-32-moving-to-testnginx.html