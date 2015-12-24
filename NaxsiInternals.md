#Some stuff about how naxsi really works, no rocket-science inside !

**For now, I'll simply put some callgraphs, real stuff will come later**

Callgraph with apache-bench (5k requests), all request are blocked :


![http://naxsi.googlecode.com/svn/wiki/Cachegrind_callgraph_full_denied.png](http://naxsi.googlecode.com/svn/wiki/Cachegrind_callgraph_full_denied.png)


Callgraph with apache-bench (5k requests), only legitimate requests :

![http://naxsi.googlecode.com/svn/wiki/Cachegrind_callgraph_no_block.png](http://naxsi.googlecode.com/svn/wiki/Cachegrind_callgraph_no_block.png)

Callgraph with naxsi complied in nginx, but disabled :

![http://naxsi.googlecode.com/svn/wiki/Cachegrind_callgraph_naxsi_disabled.png](http://naxsi.googlecode.com/svn/wiki/Cachegrind_callgraph_naxsi_disabled.png)