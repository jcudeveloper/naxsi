#Known bugs, we're hunting them down.

So far, naxsi is quite simple :
  * Parses GET/POST/PUT requests
  * For POST and PUT requests, ony `application/x-www-form-urlencoded` and `multipart/form-data` types are supported, no JSON / XML parsing.
  * Naxsi doesn't parse FILES in POST requests. It may be the case someday, but I feel like it's more an anti-virus job, as it would be extremly easy to bypass (within naxsi's design).

We're working on it:

  * (Expected commit apr 2012) Naxsi doesn't parse files buffered to disk by nginx. Code is being tested before integration in next release.
