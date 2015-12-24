#Only trust what you can test.

# Test naxsi, trust naxsi #

As a security enthusiastic, I only trust software I can test, I don't believe a wiki, and I don't think you do either.

That's why we propose you proof by example : test naxsi !

We have setup a dedicated box that acts as a reverse proxy (with OOB naxsi installation) to the following sites :
  * demo.testfire.net (Appscan demo site)
  * testphp.vulnweb.com (Acunetix demo site)
  * testasp.vulnweb.com (Acunetix demo site)


## Ok, how to play ? ##

We are no longer providing a test server for Naxsi but you can easily set up you own and point it the the URLs above.

## What's the goal, what can I win ? ##

Those sites present numerous "on purpose" vulnerabilities, your goal is fairly simple : exploit one of those vulnerabilities, find a way to bypass naxsi ! Help the project !

What can you win ? We'd like to offer you helicopters, trips to vegas & Disneyland, but we unfortunately cannot. If you're lucky enough to be in France/Paris, and find a bypass, I will be more than happy to offer you a beer and share results ! We will also add your name to the wall of fame (for people helping the project by finding bypasses/vulnerabilities) !

## How to report ? I found over 9000 vulnerabilities ##

Either report an issue to the project (via googlecode's interface), or send me an email directly !

You can also find me on irc, freenode, nickname bui.

## Limits ##

Please, do not report SQLi patterns like 1 OR 1=1 and 1 AND 1=1.
Even this is "technically speaking" an SQLi exploitation, we do not aim at blocking detection of vulnerabilities, but blocking their exploitation.

Have fun ! Thanks !