import urlparse
import itertools
import datetime
import pprint
import gzip
import glob
import logging
import sys
from nx_lib.nx_filter import NxFilter
from select import select

class NxReader():
    """ Feeds the given injector from logfiles """
    def __init__(self, injector, stdin=False, lglob=[], step=50,
                 stdin_timeout=5, date_filters=[["", ""]]):
        self.injector = injector
        self.step = step
        self.files = []
        self.date_filters = date_filters
        self.timeout = stdin_timeout
        self.stdin = False
        if stdin is not False:
            print "Using stdin."
            self.stdin = True
            return
        if len(lglob) > 0:
            for regex in lglob:
                self.files.extend(glob.glob(regex))
        print "List of imported files :"+str(self.files)

    def read_stdin(self):
        rlist, _, _ = select([sys.stdin], [], [], self.timeout)
        if rlist:
            s = sys.stdin.readline()
            if s == '':
                return False
            self.injector.acquire_nxline(s)
            return True
        else:
            return False
    def read_files(self):
        if self.stdin is True:
            ret = ""
            while self.read_stdin() is True:
                pass
            self.injector.commit()
            print "Committing to db ..."
            self.injector.wrapper.StopInsert()
            return 0
        count = 0
        for lfile in self.files:
            success = fail = 0
            print "Importing file "+lfile
            try:
                if lfile.endswith(".gz"):
                    fd = gzip.open(lfile, "rb")
                else:
                    fd = open(lfile, "r")
            except:
                print "Unable to open file : "+lfile
                return 1
            for line in fd:
                if self.injector.acquire_nxline(line) == 0:
                    success += 1
                    count += 1
                else:
                    fail += 1
                if count == self.step:
                    self.injector.commit()
                    count = 0
            fd.close()
        self.injector.commit()
        print "Committing to db ..."
        self.injector.wrapper.StopInsert()
        print "Count (lines) success:"+str(success)+", fail:"+str(fail)
        print str(self.injector.total_objs)+" valid lines, "
        print str(self.injector.total_commits)+" injected objs in DB."
        return 0

class NxInject():
    """ Transforms naxsi error log into dicts """
    # din_fmt and fil_fmt are format of dates from logs and from user-supplied filters
    def __init__(self, wrapper, filters=[]):
        self.naxsi_keywords = [" NAXSI_FMT: ", " NAXSI_EXLOG: "]
        self.wrapper = wrapper
        self.dict_buf = []
        self.total_objs = 0
        self.total_commits = 0
        self.filters = filters

    def commit(self):
        """Process dicts of dict (yes) and push them to DB """
        self.total_objs += len(self.dict_buf)
        count = 0
        for entry in self.dict_buf:
            if not entry.has_key('uri'):
                entry['uri'] = ''
            if not entry.has_key('server'):
                entry['server'] = ''
            url_id = self.wrapper.insert(url = entry['uri'], table='urls')()
            if not entry.has_key('content'):
                entry['content'] = ''
            # NAXSI_EXLOG lines only have one triple (zone,id,var_name), but has non-empty content
            if 'zone' in entry.keys():
                count += 1
                if 'var_name' not in entry.keys():
                    entry['var_name'] = ''
                    #try:
                exception_id = self.wrapper.insert(zone=entry['zone'], var_name=entry['var_name'], rule_id=entry['id'], content=entry['content'], table='exceptions')
                self.wrapper.insert(peer_ip=entry['ip'], host = entry['server'], url_id=str(url_id), id_exception=str(exception_id),
                                    date=str(entry['date']), table = 'connections')()#[1].force_commit()
                # except:
                #     print "Unable to insert (EXLOG) entry (malformed ?)"
                #     pprint.pprint(entry)
                    
            # NAXSI_FMT can have many (zone,id,var_name), but does not have content
            # we iterate over triples.
            elif 'zone0' in entry.keys():
                count += 1
                for i in itertools.count():
                    zn = ''
                    vn = ''
                    rn = ''
                    if 'zone' + str(i) in entry.keys():
                        zn  = entry['zone' + str(i)]
                    else:
                        break
                    if 'var_name' + str(i) in entry.keys():
                        vn = entry['var_name' + str(i)]
                    if 'id' + str(i) in entry.keys():
                        rn = entry['id' + str(i)]
                    else:
                        print "Error: Invalid/truncated line. No id at pos:"+str(i)+". (see logs)"
                        break
                    exception_id = self.wrapper.insert(zone = zn, var_name = vn, rule_id = rn, content = '', table = 'exceptions')()
                self.wrapper.insert(peer_ip=entry['ip'], host = entry['server'], url_id=str(url_id), id_exception=str(exception_id),
                                    date=str(entry['date']), table = 'connections')()
        self.total_commits += count
        # Real clearing of dict.
        del self.dict_buf[0:len(self.dict_buf)]
    def exception_to_dict(self, line):
        """Parses a naxsi exception to a dict, 
        1 on error, 0 on success"""
        odict = urlparse.parse_qs(line)
        for x in odict.keys():
            odict[x][0] = odict[x][0].replace('\n', "\\n")
            odict[x][0] = odict[x][0].replace('\r', "\\r")
            odict[x] = odict[x][0]
        return odict
    # can return : 
    # 0 : ok
    # 1 : incomplete/malformed line 
    # 2 : not naxsi line
    def acquire_nxline(self, line, date_format='%Y/%m/%d %H:%M:%S',
                       sod_marker=[' [error] ', ' [debug] '], eod_marker=[', client: ', '']):
        line = line.rstrip('\n')
        for mark in sod_marker:
            date_end = line.find(mark)
            if date_end != -1:
                break
        for mark in eod_marker:
            if mark == '':
                data_end = len(line)
                break
            data_end = line.find(mark)
            if data_end != -1:
                break
        if date_end == -1 or data_end == 1:
            return 1
        try:
#datetime.datetime.strptime(line[:date_end], date_format)
            date = line[:date_end]
        except ValueError:
            return 1
        chunk = line[date_end:data_end]
        md = None
        for word in self.naxsi_keywords:
            idx = chunk.find(word)
            if (idx != -1):
                md = self.exception_to_dict(chunk[idx+len(word):])
                if md is not None:
                    md['date'] = date
                    break
        if md is None:
            return 1
        self.dict_buf.append(md)
        return 0
