#Bench !

## Results ##

In this bench, I will present naxsi's raw performances.
As you will see, the nginx configuration for tested site only does a "return 200;". Meaning that nginx is in a condition where it can 'instantly' deliver any page (No network interaction, no Hard Drive interaction).

  * Without naxsi (nginx-1.0.14) : 12K RPS
  * With naxsi (nginx-1.0.14 + naxsi-0.44) : 8K RPS

I cannot stress this enough for people reading too fast : this is not a realistic case at all. It is well known that bottleneck will be webserver and pages generation.

So here we are benching naxsi itself :)

## Without naxsi ##

Nginx : 1.0.14 (current stable as of writing time)

Configure options :
```

./configure --conf-path=/etc/nginx/nginx.conf
--error-log-path=/var/log/nginx/error.log
--http-client-body-temp-path=/var/lib/nginx/body
--http-fastcgi-temp-path=/var/lib/nginx/fastcgi
--http-log-path=/var/log/nginx/access.log
--http-proxy-temp-path=/var/lib/nginx/proxy
--lock-path=/var/lock/nginx.lock
--pid-path=/var/run/nginx.pid
--with-http_ssl_module
--without-mail_pop3_module
--without-mail_smtp_module
--without-mail_imap_module
--without-http_uwsgi_module
--without-http_scgi_module
--with-ipv6  --prefix=/usr
```


nginx configuration :
```

user www-data;
worker_processes  10;
worker_rlimit_core  500M;
working_directory   /tmp/;

error_log  /var/log/nginx/error.log;
pid        /var/run/nginx.pid;


events {
worker_connections  10000;
use epoll;
}

http {
include       /etc/nginx/mime.types;
server_names_hash_bucket_size 128;
access_log  /var/log/nginx/access.log;

sendfile        on;
keepalive_timeout  65;
tcp_nodelay        on;

gzip  on;
gzip_disable "MSIE [1-6]\.(?!.*SV1)";
server {
proxy_set_header Proxy-Connection "";
listen       *:80;
access_log  /tmp/nginx_access.log;
error_log  /tmp/nginx_error.log;

location / {
return 200;
}


location /RequestDenied {
return 500;
}
}
}
```



AB results (10K requests, 1K concurrent connections).

```

Server Software:        nginx/1.0.14
Server Hostname:        xx.xx.xx.xx
Server Port:            80

Document Path:          /?foobar=AAAAAA&bar=BBBBBBBBBBBBB&xx=AAAAAAAAAAAAA&rere=ZZZZZZZZZZZZZZZZZZZ&jzrlk=AZJEJAJE12313123123131
Document Length:        0 bytes

Concurrency Level:      1000
Time taken for tests:   0.816 seconds
Complete requests:      10000
Failed requests:        0
Write errors:           0
Total transferred:      1420000 bytes
HTML transferred:       0 bytes
Requests per second:    12260.64 [#/sec] (mean)
Time per request:       81.562 [ms] (mean)
Time per request:       0.082 [ms] (mean, across all concurrent requests)
Transfer rate:          1700.21 [Kbytes/sec] received

Connection Times (ms)
min  mean[+/-sd] median   max
Connect:        0    5   6.5      3      27
Processing:     3   11  13.8      8     215
Waiting:        1   10  13.6      7     215
Total:          7   16  17.9     10     226

Percentage of the requests served within a certain time (ms)
50%     10
66%     11
75%     12
80%     13
90%     44
95%     55
98%     68
99%     72
100%    226 (longest request)

```


## With Naxsi ##

AB results (10K requests, 1K concurrent connections).

```

Server Software:        nginx/1.0.14
Server Hostname:        xx.xx.xx.xx
Server Port:            80

Document Path:          /?foobar=AAAAAA&bar=BBBBBBBBBBBBB&xx=AAAAAAAAAAAAA&rere=ZZZZZZZZZZZZZZZZZZZ&jzrlk=AZJEJAJE12313123123131
Document Length:        0 bytes

Concurrency Level:      1000
Time taken for tests:   1.224 seconds
Complete requests:      10000
Failed requests:        0
Write errors:           0
Total transferred:      1420000 bytes
HTML transferred:       0 bytes
Requests per second:    8170.70 [#/sec] (mean)
Time per request:       122.388 [ms] (mean)
Time per request:       0.122 [ms] (mean, across all concurrent requests)
Transfer rate:          1133.05 [Kbytes/sec] received

Connection Times (ms)
min  mean[+/-sd] median   max
Connect:        0    5   8.7      1      36
Processing:     1   20  21.8     15     637
Waiting:        1   19  21.8     14     637
Total:          3   24  27.5     15     638

Percentage of the requests served within a certain time (ms)
50%     13
66%     13
75%     14
80%     16
90%     41
95%     95
98%    122
99%    135
100%    228 (longest request)


```