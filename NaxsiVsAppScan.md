#Showing and explaining Naxsi results Vs Appscan

# Classical benchmark : Web Vuln Scanner vs WAF #


Here we will present the results of (IBM) AppScan vs NAXSI.

Why AppScan ? Because, it's not a bad "commercial" scanner, because they offer a target/demo (read : highly vulnerable) website, and, unlike Acunetix, you can run full tests on the target website.

I apologize for the french AppScan GUI ;)

# Overall Results #

As you will see bellow, AppScan is not able to find any vulnerabilities that it can exploit. The only vulnerabilities detected are probed with extremely simple patterns (read : nearly full ascii) that are not (and will not) be blocked by naxsi (to avoid false positives).

## Raw results ##
When running AppScan against demo.testfire.net with naxsi (set-up as forward proxy for this purpose), the following vulnerabilities will appear :
![http://naxsi.googlecode.com/svn/wiki/appscanfull.png](http://naxsi.googlecode.com/svn/wiki/appscanfull.png)

I won't make an exhaustive diff list between naxsi and raw results since, as you can expect, original scan results have a LOT of vulnerabilities, as this website is designed to show all the vulnerabilities AppScan can detect/exploit.

Let's go through all the "remaining" bugs :

## Blind SQL Injections ##
The scan result shows at least 2 Blind SQL Injection remaining. Actually, the attack pattern used by AppScan is the following :

![http://naxsi.googlecode.com/svn/wiki/appscandetails1.png](http://naxsi.googlecode.com/svn/wiki/appscandetails1.png)
![http://naxsi.googlecode.com/svn/wiki/appscandetails2.png](http://naxsi.googlecode.com/svn/wiki/appscandetails2.png)


_First test pattern :_

`listAccounts=0%2B0%2B0%2B1001160141`

decoded to :

`listAccounts=0+0+0+1001160141`

_Second test pattern:_

`before=1234+and+7659%3D7659`

decoded to :

`before=1234 and 7659=7659`


**Conclusion :** Appscan is able to detect the vulnerability, but will not be able to exploit it. It was detected because a very benign pattern is enough to make the code run into an unexpected behavior.

**How can you pretend it cannot be exploited ?!**
Here, AppScan was able to detect the vulnerabilities, because most of the used characters are not tagged by naxsi (or with very low score), for obvious reasons :

  * '+' : Is widely used, to encode space character for example
  * '=' : Is widely used too
  * 'and' : Even though it's a SQL keyword, we do not tagg it, because it may produce many false positives


## Database Error Pattern ##
During the scan, AppScan was able to detect several "Database Error Pattern" (read : MSSQL/MySQL/... error messages in webpage)

![http://naxsi.googlecode.com/svn/wiki/appscandetails3.png](http://naxsi.googlecode.com/svn/wiki/appscandetails3.png)

_Test pattern:_
`100116014WFXSSProbe` (The 100116014 part is random and is used by AppScan to 'find back' the injected data in the webpage)

**Conclusion :** Here, AppScan is able to trigger the bug by entering a non-numeric value in a numeric field, making the page yield a SQL error message. Obviously, you cannot do anything here except blocking the scanner's pattern, which would be dumb and inefficient. Obviously, the injected characters won't allow any kind of exploitation of the vulnerability, only a probe.

## Other vulnerabilities ##

The other vulnerabilities reported by AppScan :
  * Weak credentials : Because it's possible to login with admin/admin. No comment, Out of scope for a WAF.
  * Session Reuse : When logging / logging off and logging in again, AppScan notices that the Cookie (session) doesn't change. (Out of scope for a WAF)
  * Weak Cookies : Sensitive information is stored in the user's cookie, enabling cookie theft if someone can access the user's workstation. (Out of scope for a WAF)
  * No account lock : An attacker can brute-force passwords. (Out of scope for a WAF, but nginx with req\_limit might help you solving that !)
  * CSRF : This is more touchy, because it can be blocked by NAXSI, by adding a rule like :
`BasicRule "rx:http://demo.testfire.net/*" "mz:$HEADERS:Referer";`

I didn't add it, because I wanted this scan to be really "out of the box" with no customization.