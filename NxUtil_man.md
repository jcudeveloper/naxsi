**Please always refer to your current manual (man nx\_util)**


NAME
> nx\_util - A tool to parse & analyze naxsi logs

SYNOPSIS
> nx\_util [-hoi] [-l FILE ] [-H FILE ] [-f filter ]

DESCRIPTION
> nx\_util processes nginx-naxsi log files to generate white-lists or html reports.  It stores NAXSI\_FMT/NAXSI\_EXLOG events to a sqlite database, and use it to
> generate both whitelists and reports.  The user can supply filters to reduce false positives or reduce the scope of the html reports.

OPTIONS
> nx\_util supports options for the three different functions :

> Importing filtered events (from logs, gzipped logs or stdin),
> generating naxsi whitelists from events,
> generating html reports representing activity over the specified period.

> nx\_util -d mysite -l /var/log/nginx/mysite.error.log

> This tells nx\_util to parse the nginx-naxsi error log /var/log/nginx/mysite.error.log , extract NAXSI\_FMT and NAXSI\_EXLOG events, and store  them  into  the
> sqlite database 'mysite'.

> nx\_util -d mysite -o

> This tells nx\_util to display to stdout generated whitelists from database mysite.

> nx\_util -d mysite -H mysite.html

> This tells nx\_util to generate a html report (mysite.html) of events from mysite


> nx\_util -l /var/log/nginx/`*`error`*`log`*` -f "country = FR"

> nx\_util will import events from all files matching the /var/log/nginx/`*`error`*`log`*` string,
> but will only import events for which originating country is France.

> You can find detailed notes about filters in the FILTERS section below.




> -l FILES
> > Process supplied nginx-naxsi log files.
> > Space-separated list of files and regular expressions as well.  If no file name is specified, stdin is used to read log lines.


> -i     If option is passed, nx\_util will work in incremental mode,
> > and will append data to sqlite database, rather than create a new one.



> -H FILE
> > Outputs a html static report to the FILE.
> > Python-geoip is required for the world-map section.



> -f FILTER
> > Specify one or multiple filters to apply to events.
> > The ip,uri,date,server,zone,var\_name,id,content,country keywords can be used,
> > along with the operators = != =~ (and >,>,<=, >= for dates)
> > Note that the python-geoip is required for country-filters.


> -o
> > Outputs generated whitelists to stdout.
> > If NAXSI\_EXLOG datas are present, they will be integrated to output.



> -d db\_name
> > Specify the name of the sqlite3 database to use.
> > By default, nx\_util will append data to the database called naxsi\_sig in the current directory.


> -c config-file
> > config-file  specifies directories for sqlite databases and static files used to generate reports. It provides path to naxsi rules as well, to embel‐
> > lish whitelists output.


FILTERS

> nx\_util's offers a very primtive language for filtering events that aims at
> Lower false-positive rate when doing learning (by restricting events on country, periods etc.)
> Provide focused reports whenever you whish to investigate a specific event.

> Filters need to be supplied with -f argument, are quoted, and support various keywords : ip, date, server, uri, zone, var\_name, id, content,  country  ,  as
> well as some simple operators : = != <= >= =~

> Supported keywords

> ip is a string representation of the client ip, and supports =, !=, =~ operators :
> > -f 'ip = 8.8.8.8'  : Only events from IP 8.8.8.8 will be analyzed.
> > -f 'ip =~ 8.`*`'       : Only events from IPs starting by a '8' will be analyzed.
> > -f 'ip != 1.1.1.1'   : Events from 1.1.1.1 will not be analyzed.


> date is a string representation of the date, in the format YYYY-MM-DD HH:MM:SS.
> Note that lastweek and lastmonth values can be used as shortcuts for now() - (60`*`60`*`24`*`7) and now() - (60`*`60`*`24`*`30).
> As well, date supports the > and < operators :
> > -f 'date > lastmonth and date < lastweek' will select events that are newer than 30 days and older than 7 days.


> When using a full date for comparisons, it needs to be quoted :
> -f 'date >= "2013-01-01 00:00:00"' will select events newer than 1st Jan of 2013.

> server corresponds to the "Host" http header.

> uri corresponds to the requested uri.
> > -f 'uri =~ ^/.`*`foo$' will select events whith an url starting with a '/' and ending with 'foo'.


> zone corresponds to the zone in which the event happened. It can be useful when troubleshooting specific events.
> > -f "zone = BODY" will only select events that happened in a POST/PUT body.


> id corresponds to the naxsi-rule ID that matched. It supports >, <, >= and <= operators.

> var\_name corresponds to the variable name in which the event occured.

> content can only be used when importing naxsi\_exlog events.  Content refers to offending data captured from the http request.

> country is the two-letter country code representation of the client's IP. It requires the GeoIP module to be used :
> > -f "country = FR" will only select events coming from France.


WHITELISTS

> Option -o is used to generate whitelists from events. Typical output looks like this :
    1. total\_count:1420 (10.66%), peer\_count:130 (35.62%) | mysql keyword (|)
> > BasicRule wl:1005 "mz:$HEADERS\_VAR:cookie";


> Each suggested whitelist has two line :

> The first one indicates the total number of times this event was triggered, its ratio amongst the total number of exceptions,
> > along with the number of unique peers that triggered the event, and the ratio amongst all unique peers that triggered events.
> > if your nx\_util.conf file contains a valid path to naxsi rules, you will as well get a human readable explenation of the event.


> The second line is the whitelist itself, in a format that naxsi can understand.

> Those whitelists should be included (either directly or via nginx's include directive) to your configuration,
> directly into the location where naxsi is activated.

> If you enable $naxsi\_extensive\_log in your location, nx\_util will include extra data in the whitelists, such as :
    1. total\_count:2 (0.27%), peer\_count:1 (5.0%) | , in stuff
    1. xemple (from exlog) : 'Korea, North'
> > BasicRule wl:1015 "mz:$URL:/user/register|$BODY\_VAR:field\_country[und](und.md)";


> After the original comment line, another one was added. The quoted string corresponds to the actual content
> of the variable that triggered the exception, helping you to distinguish false positives.


EXAMPLES
> cat foobar.log | nx\_util -l -o -H test1
> > nx\_util reads events from stdin, then generates whitelists to stdout (-o) and html report to  "test1" (-H)


> nx\_util -l /var/log/nginx/`*`error.log -H test1 -f "date > lastweek"
> > nx\_util will read all log files from /var/log/nginx directory
> > and create a html report of last week events to file "test1"


> nx\_util -d allsites -i -l /var/log/nginx/`*`error.log -H test1 -f "date > lastweek"
> > nx\_util will append last week events from all files in /var/log/nginx/`*`error.log to the database allsites.


BUGS

> The filters mechanism is extremely primitive and might be subject to bugs if you attempt to create some complex filters.