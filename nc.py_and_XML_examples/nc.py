#!/usr/bin/env python

__author__  = 'robert puskajler'
__email__   = 'rpuskajl@cisco.com'
__version__ = '1.0.19'


def usage():
    print \
"""
NetConf Commander - CLI version %s - tool for sending file requests to netconf device and getting responses back

By design it doesn't allocate any big structures in memory so it is suitable to handle huge requests and responses.
Requests are parsed and sent to netconf device line-by-line. Responses are processed line-by-line and stored to files.
It requires 'sshpass' utility (see the note bellow for details how to get sshpass).

NetConf Commander - CLI version supports:
- HELLO handshake
- built in CLOSE  session operation
- built in COMMIT changes operation
- built in SLEEP command
- set custom variables (token replacement) for request templates
- executing single request/response
- sequencing of requests/responses
- looping (repeating defined sequence of requests/responses)
- configurable prefixes for storing response files
- supression of storing responses
- optional timestamping

usage: nc.py [ -time] -connect user:password@host[:port][ -hrf][ -hello][ -hellofile hello.xml[ -loop n][ -rs prefix][ -nors]
             [ -file request.xml][ -file request2.xml][ -var name=val][ -get name][ -commit][ -close]

    -time             ... print timestamps at the beginning of each output line to stdout (recommended)
    -connect url      ... connect to url (format is user:password@host:port)
    -hrf              ... human readable format for numbers (like du or df utility on unix)
    -hello            ... perform HELLO handshake and show session_id (send and receive hello message)
    -hellofile h.xml  ... use HELLO from file h.xml instead of default hardcoded one, this will also store HELLO response
    -loop count       ... start looping with count (will repeat everything till end-of-line after loop command cnt times)
    -rs prefix        ... use prefix for responses (default is 'rs-' so 'request.xml' will create 'rs-request.xml' file)
                          existing file is overwritten without any warnings, exisitng token '${i}' is replaced by loop counter
    -nors             ... do not store responses (feeds responses to /dev/null)
    -file request.xml ... send reqest from file 'request.xml', can be used multiple times to send sequence of various requests
                          token '${TIMESTAMP}' is replaced by current unix timestamp (recommended for message-id attribute)
    -sleep seconds    ... sleep seconds before continuing (can be also float number like 1.25)
    -commit           ... perform built-in COMMIT-CHANGES operation
    -close            ... perform built-in CLOSE-SESSION  operation
    -var name=value   ... set NAME to value used for token replacement in request templates (default TIMESTAMP value is unix time())
    -get name         ... prints text value of the first xml tag with name, requires response file (also memory hungry for big responses)
    -debug f1,f2      ... activate debug mode for method f1, or comma separated list of names (* act as a wildcard to match all)
    -help             ... shows this help
    -examples         ... usage examples

NOTE: the order of command line parameters is important. Parameters are processed exactly in the order they are entered,
therefore the sequence should follow this pattern: -connect -hello -file optional multiple -file and optional -close.

Here are short versions for frequently used parameters, each line represents equivalent parameter:
  '-h' '-help' '-?'
  '-t' '-time' '-timestamp'
  '-l' '-loop' '-repeat'
  '-c' '-con' '-connect' '-url'
  '-f' '-file' '-rq'
  '-o' '-hellofile' '-hellorq'
  '-s' '-sleep'
  '-v' '-dbg' '-debug'
  '-hrf' '-hformat'
  '-var' '-set'
  '-get' '-tag'

UUT CONFIG: To congifure netconf to listen on standard tcp port 830 use following statements in the config menu:
  ssh server netconf port 830
  netconf agent ssh

SSHPASS: It is well know standard utility for automated ssh login used in cron jobs and batch scripts.
Use either system installed one or the one included in the package compiled on aurora 5.5 (ver 1.05).
There is also version 1.00 available here: /auto/catch/Published/tools/sshpass/bin/sshpass,
so just copy it to the directory where nc.py is located or setup your PATH variable.
To verify sshpass setup use the command 'sshpass -V' to print copyright and version information.

""" % __version__


def usage_examples():
    print \
"""
NetConf Commander - CLI version %s - tool for sending requests from files to netconf device and getting responses to files

usage: nc.py [ -time] -connect user:password@host[:port][ -hrf][ -hello][ -hellofile hello.xml[ -loop n][ -rs prefix][ -nors]
             [ -file request.xml][ -file request2.xml][ -var name=val][ -get name][ -commit][ -close]

usage examples:


1 - verify connectivity to netconf device and user authentication:

$ nc.py -con root:toor@localhost:8830
   CONNECT:                 root:toor@localhost:8830 ... OK


2 - perform HELLO handshake (shows session id) and show timestamps:

$ nc.py -time -con root:toor@localhost:8830 -hello
[2014-10-22 00:11:56]    CONNECT:                 root:toor@localhost:8830 ... OK
[2014-10-22 00:11:56]      HELLO:                          session_id=3832 sent:    657 [Bytes], recv:  18042 [Bytes], rq.time:    0.0 [ms], rs.time:  456.2 [ms]


3 - perform get-config operation, response will be stored in 'rs-get-config.xml' file:

$ nc.py -con root:toor@localhost:8830 -hello -file get-config.xml
   CONNECT:                 root:toor@localhost:8830 ... OK
     HELLO:                         session_id=29632 sent:    657 [Bytes], recv:  18043 [Bytes], rq.time:    0.0 [ms], rs.time:  432.0 [ms]
      FILE:      get-config.xml -> rs-get-config.xml sent:    254 [Bytes], recv:   2956 [Bytes], rq.time:    0.1 [ms], rs.time:  642.0 [ms]


4 - repeat 3 times get-config operation, do not store responses:

$ nc.py -con root:toor@localhost:8830 -hello -nors -loop 3 -file rq/get-config.xml
   CONNECT:                 root:toor@localhost:8830 ... OK
     HELLO:                         session_id=32077 sent:     657 Bytes, recv:   18043 Bytes, rq:     0.0 ms, rs:    54.5 ms
      LOOP:                              REPEAT 3 x  ... START
   1. FILE:           rq/get-config.xml -> /dev/null sent:     252 Bytes, recv:    2954 Bytes, rq:     9.2 ms, rs:   712.1 ms
   2. FILE:           rq/get-config.xml -> /dev/null sent:     252 Bytes, recv:    2954 Bytes, rq:     0.4 ms, rs:   712.1 ms
   3. FILE:           rq/get-config.xml -> /dev/null sent:     252 Bytes, recv:    2954 Bytes, rq:     0.4 ms, rs:   710.8 ms
      LOOP:                    === SUMMARY.STATS === sent:     756 Bytes, recv:    8862 Bytes, rq:    10.0 ms, rs:  2134.9 ms


5 - repeat 3 times get-config, read requests from subdir rq and store responses to subdir rs with loop counter as prefix:

$ nc.py -time -con root:toor@localhost:8830 -hello -rs 'rs/${i}-' -loop 3 -file rq/get-config.xml
[2014-10-24 23:58:39]    CONNECT:                 root:toor@localhost:8830 ... OK
[2014-10-24 23:58:39]      HELLO:                         session_id=13541 sent:     657 Bytes, recv:   18043 Bytes, rq:     0.0 ms, rs:    52.8 ms
[2014-10-24 23:58:39]       LOOP:                              REPEAT 3 x  ... START
[2014-10-24 23:58:40]    1. FILE: rq/get-config.xml -> rs/001-get-config.xml sent:     252 Bytes, recv:    2954 Bytes, rq:     0.1 ms, rs:   738.4 ms
[2014-10-24 23:58:40]    2. FILE: rq/get-config.xml -> rs/002-get-config.xml sent:     252 Bytes, recv:    2954 Bytes, rq:     0.1 ms, rs:   709.6 ms
[2014-10-24 23:58:41]    3. FILE: rq/get-config.xml -> rs/003-get-config.xml sent:     252 Bytes, recv:    2954 Bytes, rq:     0.1 ms, rs:   709.2 ms
[2014-10-24 23:58:41]       LOOP:                    === SUMMARY.STATS === sent:     756 Bytes, recv:    8862 Bytes, rq:     0.3 ms, rs:  2157.2 ms


6 - lock candidate, wait 5.1 seconds then unlock candidate, do not store responses:

$ nc.py -time -con root:toor@localhost:8830 -hello -nors -file rq/lock-candidate.xml -sleep 5.1 -file rq/unlock-candidate.xml
[2014-10-24 23:59:42]    CONNECT:                 root:toor@localhost:8830 ... OK
[2014-10-24 23:59:42]      HELLO:                         session_id=11243 sent:     657 Bytes, recv:   18043 Bytes, rq:     0.0 ms, rs:    55.8 ms
[2014-10-24 23:59:42]       FILE:       rq/lock-candidate.xml -> /dev/null sent:     242 Bytes, recv:     153 Bytes, rq:    17.8 ms, rs:   100.8 ms
[2014-10-24 23:59:42]      SLEEP:                             for 5.10 sec ... 5.10 s
[2014-10-24 23:59:47]       FILE:     rq/unlock-candidate.xml -> /dev/null sent:     246 Bytes, recv:     153 Bytes, rq:     0.1 ms, rs:   100.8 ms


7 - get hostname

$ nc.py -time -con root:toor@localhost:8830 -hello -rq rq/host-name/get-hostname.xml -get host-name
[2014-11-14 00:34:19] NC.CONNECT:                 root:toor@localhost:8830.......... OK
[2014-11-14 00:34:26]      HELLO:                         session_id=11380 sent:     657 Bytes, recv:   18043 Bytes, rq:     0.0 ms, rs:    60.6 ms
[2014-11-14 00:34:26]       FILE: rq/host-name/get-hostname.xml -> rs-get-hostname.xml sent:     385 Bytes, recv:     324 Bytes, rq:     0.1 ms, rs:   101.7 ms
[2014-11-14 00:34:26]        TAG:                  host-name = host.domain ... GET


8 - change hostname

$ nc.py -time -con root:toor@localhost:8830 -hello -var HOSTNAME=host.domain -rq rq/host-name/set-hostname.xml -commit
[2014-11-14 00:36:13] NC.CONNECT:                 root:toor@localhost:8830.......... OK
[2014-11-14 00:36:20]      HELLO:                         session_id=11940 sent:     657 Bytes, recv:   18043 Bytes, rq:     0.0 ms, rs:    61.4 ms
[2014-11-14 00:36:20]        VAR:                ${HOSTNAME} = host.domain ... SET
[2014-11-14 00:36:20]       FILE: rq/host-name/set-hostname.xml -> rs-set-hostname.xml sent:     415 Bytes, recv:     217 Bytes, rq:     0.1 ms, rs:   101.5 ms
[2014-11-14 00:36:20]     COMMIT:                                       OK sent:     415 Bytes, recv:     217 Bytes, rq:     0.1 ms, rs:   101.5 ms

""" % __version__


import subprocess
import sys
import time
import re
import os
import fcntl
import xml.etree.ElementTree as ET
import datetime
import inspect


class NetConf:
    """
    Netconf class
    """

    sshpass = 'sshpass'
    subsystem = 'netconf'
    xmlns = 'urn:ietf:params:xml:ns:netconf:base:1.0'
    ssh_timeout  = 7
    rdln_timeout = 60
    last_error = ''
    # debug (* = debug_all)
    dbg_active = None

    # framing sequences
    EOM_10 = ']]>]]>'
    EOM_11 = "##\n"
    CHUNK  = re.compile('^#(\d+)$')

    # variable token
    VARS = {}

    def __init__(self, url=None, user=None, pswd=None, host=None, port=None):
        """

        :param url:
        :param user:
        :param pswd:
        :param host:
        :param port:
        """
        if  url is not None: self.parse_url(url)
        if user is not None: self.user = user
        if pswd is not None: self.pswd = pswd
        if host is not None: self.host = host
        if port is not None: self.port = port
        return


    def parse_url(self, url):
        """
        :param url: user:password@host:port
        :return:
        """
        if '@' not in url or ':' not in url:
            self.print_err('Invalid url(%s) - required format is user:pass@host[:port]' % url)
            sys.exit(-2)
        userpswd,hostport = url.rsplit('@', 1)
        self.user, self.pswd = userpswd.split(':', 1)
        if ':' in hostport:
          self.host, self.port = hostport.split(':', 1)
        else:
          self.host = hostport
          self.port = '830'
        # debug splitting
        NetConf.dbg('url(%s) -> user(%s) pswd(%s) host(%s) port(%s)' % (url, self.user, self.pswd, self.host, self.port))
        return


    def print_err(self, msg):
        """

        :return:
        """
        self.last_error = msg
        print >>sys.stderr, msg
        return


    def connect(self):
        """

        :return:
        """
        err = None
        args = [ self.sshpass, '-p', self.pswd,
                'ssh',
                '-o', 'PubkeyAuthentication=no',
                '-o', 'StrictHostKeyChecking=no',
                '-o'  'UserKnownHostsFile=/dev/null',
                '-o', 'ConnectTimeout=%d' % self.ssh_timeout,
                '-p', self.port,
                '%s@%s' % (self.user, self.host),
                '-s', self.subsystem ]
        try:
            self.ssh = subprocess.Popen(args,
                               bufsize=1,
                               stdin=subprocess.PIPE,
                               stdout=subprocess.PIPE,
                               stderr=subprocess.PIPE,
                               shell=False,
                               env={'PATH': '.:'+os.environ['PATH']} )
                               
            # http://eyalarubas.com/python-subproc-nonblock.html
            flags = fcntl.fcntl(self.ssh.stdout, fcntl.F_GETFL)
            fcntl.fcntl(self.ssh.stdout, fcntl.F_SETFL, flags | os.O_NONBLOCK)

            #flags = fcntl.fcntl(self.ssh.stderr, fcntl.F_GETFL)
            #fcntl.fcntl(self.ssh.stderr, fcntl.F_SETFL, flags | os.O_NONBLOCK)

            err = self.connection_error()

        except (OSError, IOError) as e:
            # file not found
            desc = 'sshpass ' if e.errno == 2 else ''
            err = 'Connect to host %s failed - %s%s' % (self.host, desc, e)
            self.print_err(err)

        #stdout, stderr = x.communicate()
        return err


    def terminate(self):
        """
        close ssh connection
        :return:
        """
        if self.is_ssh_running(): self.ssh.terminate()
        return


    def is_ssh_running(self):
        """
        check if child process is still running
        :return:
        """
        return self.ssh.poll() is None


    def connection_error(self):
        """
        :return: try to return as descriptive error as possible
        """
        # wait till ssh negotiations takes place so we really know if connection was successfull
        for i in range(self.ssh_timeout):
            time.sleep(1)
            if not self.is_ssh_running(): break
            self.print_progress()
        #
        if self.is_ssh_running(): return
        #
        for line in self.ssh.stderr:
            # dbg
            NetConf.dbg('stderr line(%s)' % line)
            if 'refused' in line:
                return 'Invalid host:port - %s' % line
            if 'denied' in line:
                return 'Invalid password - %s'  % line
            if 'disconnect' in line:
                return 'Invalid username - %s'  % line
        return


    def readln(self, stream, eom='', timeout=None):
        """
        This is a dirty hack due to Python bug - readline() doesn't work in non-blocking mode
        :param fd:
        :param eom:
        :return:
        """
        line = ''
        fd = stream.fileno()
        if timeout is None: timeout = self.rdln_timeout
        stoptime = time.time() + timeout
        while True:
            # if ssh diconnected
            if not self.is_ssh_running():
                raise IOError('Netconf server disconnected - ssh return code %s' % self.ssh.returncode)
            try:
                c = os.read(fd, 1)
            except:
                #print self.ssh.stderr.readline()
                if time.time() >  stoptime:
                    raise IOError('readln() timeout - %d sec no data' % timeout)
                time.sleep(0.1)
                continue
            line += c
            if c == "\n":
                break
            if line == eom:
                break
            # move timeout as we got char
            stoptime = time.time() + timeout
        # dbg
        NetConf.dbg("line(%s) eom(%s)" % (line,eom))
        return line


    def chunk_str(self, str):
        """
        chunkize string
        :param line:
        :return:
        """
        str = str.rstrip()
        return "\n#%d\n%s" % (len(str), str)


    def replace_tokens(self, line):
        """
        replace tokens in line requests before sending to device
        :param line:
        :return:
        """
        self.VARS.setdefault('${TIMESTAMP}', '%d' % time.time())
        #if len(line) < 10:   return line
        for token,value in self.VARS.iteritems():
            line = line.replace(token, value)
        return line


    def send_rq10_str(self, str):
        """
        send netconf 1.0 request from string
        :param str:
        :return:
        """
        cnt = 0
        self.last_error = ''
        start = time.time()
        try:
            self.ssh.stdin.write(str)
            cnt += len(str)
            self.ssh.stdin.write("\n"+self.EOM_10)
            cnt += len("\n"+self.EOM_10)
        except (OSError, IOError) as e:
            self.print_err('Sending Rq.10 failed - %s' % e)

        return cnt, time.time()-start


    def send_rq10_file(self, fname):
        """
        send netconf 1.0 request from file
        :param str:
        :return:
        """
        cnt = 0
        self.last_error = ''
        start = time.time()
        try:
            with open(fname) as f:
                for line in f:
                    # dbg
                    NetConf.dbg("line(%s)" % line)
                    self.ssh.stdin.write(line)
                    cnt += len(line)
            line = "\n"+self.EOM_10
            self.ssh.stdin.write(line)
            self.ssh.stdin.flush()
            cnt += len(line)
        except (OSError, IOError) as e:
            self.print_err('Sending Rq.10 %s failed - %s' % (fname, e))

        return cnt, time.time()-start


    def send_rq11_str(self, str):
        """
        send netconf 1.1 request from string
        :param fd:
        :return:
        """
        cnt = 0
        self.last_error = ''
        start = time.time()
        try:
            cline = self.replace_tokens(str)
            cline = self.chunk_str(cline)
            self.ssh.stdin.write(cline)
            cnt += len(cline)

            cline = "\n"+self.EOM_11
            self.ssh.stdin.write(cline)
            cnt += len(cline)
        except (OSError, IOError) as e:
            self.print_err('Sending Rq.11 failed - %s' % e)

        return cnt, time.time()-start


    def send_rq11_file(self, fname):
        """
        send netconf 1.1 request from file
        :param fd:
        :return:
        """
        cnt = 0
        self.last_error = ''
        start = time.time()
        try:
            with open(fname) as f:
                for line in f:
                    # skip empty lines
                    if not line.strip(): continue
                    # dbg
                    NetConf.dbg("line(%s)" % line)
                    cline = self.replace_tokens(line)
                    cline = self.chunk_str(cline)
                    self.ssh.stdin.write(cline)
                    cnt += len(cline)
                    #print 'rq11:%s' % cline,
            cline = "\n"+self.EOM_11
            self.ssh.stdin.write(cline)
            cnt += len(cline)
            #print 'rq11:%s' % cline,
        except (OSError, IOError) as e:
            self.print_err('Sending Rq.11 %s failed - %s' % (fname, e))

        return cnt, time.time()-start



    def recv_rs10_xml(self):
        """
        receive netconf 1.0 response and parse response to xml
        :return:
        """
        cnt = 0
        self.last_error = ''
        start = time.time()
        res = []
        xml = None
        try:
            while True:
                line = self.readln(self.ssh.stdout, self.EOM_10)
                # dbg
                NetConf.dbg("line(%s)" % line)
                cnt += len(line)
                if line == self.EOM_10:
                    break
                res.append(line)
            xml = ET.fromstringlist(res)
        except (OSError, IOError) as e:
            self.print_err('Receiving Rq.10 failed - %s' % e)

        return cnt, time.time()-start, xml


    def recv_rs10_file(self, fname):
        """
        receive netconf 1.0 response and store it to file
        :return:
        """
        cnt = 0
        self.last_error = ''
        start = time.time()
        try:
            with open(fname,'w') as f:
                while True:
                    line = self.readln(self.ssh.stdout, self.EOM_10)
                    # dbg
                    NetConf.dbg("line(%s)" % line)
                    cnt += len(line)
                    if line == self.EOM_10:
                        break
                    f.write(line)
        except (OSError, IOError) as e:
            self.print_err('Receiving Rq.10 %s failed - %s' % (fname, cnt))

        return cnt, time.time()-start


    def recv_rs11_file(self, fname):
        """
        receive netconf 1.1 response and store it to file
        :param fname:
        :return:
        """
        cnt = clen = size = 0
        self.last_error = ''
        start = time.time()
        try:
            with open(fname,'w') as f:
                while True:
                    line = self.readln(self.ssh.stdout, self.EOM_11)
                    NetConf.dbg("line(%s)" % line)
                    cnt  += len(line)
                    size += len(line)
                    # chunk expected
                    if cnt >= clen:
                        # end of message
                        if line == self.EOM_11:
                            break
                        # lenght chunk
                        match = self.CHUNK.match(line)
                        if match:
                            clen = int(match.group(1))
                            cnt = 0
                            NetConf.dbg("chunk found with len(%d)" % clen)
                            continue
                        if cnt > clen+1:
                            self.print_err('Received chunking error cnt(%d) > length(%d) line:%s' % (cnt, clen, line))
                    # write only lines inside chunk
                    if clen > 0:
                        f.write(line)
        except (OSError, IOError) as e:
            self.print_err('Receiving Rq.11 %s failed - %s' % (fname, e))

        return size, time.time()-start

    def recv_rs11_xml(self):
        """
        receive netconf 1.1 response and parse it to xml
        :param fname:
        :return:
        """
        cnt = clen = size = 0
        self.last_error = ''
        res = []
        xml = None
        start = time.time()
        try:
            while True:
                line = self.readln(self.ssh.stdout, self.EOM_11)
                NetConf.dbg("line(%s)" % line)
                cnt  += len(line)
                size += len(line)
                # chunk expected
                if cnt >= clen:
                    # end of message
                    if line == self.EOM_11:
                        xml = ET.fromstringlist(res)
                        break
                    # lenght chunk
                    match = self.CHUNK.match(line)
                    if match:
                        clen = int(match.group(1))
                        cnt = 0
                        NetConf.dbg("chunk found with len(%d)" % clen)
                        continue
                    if cnt > clen+1:
                        self.print_err('Received chunking error cnt(%d) > length(%d) line:%s' % (cnt, clen, line))
                # write only lines inside chunk
                if clen > 0:
                    res.append(line)
        except (OSError, IOError) as e:
            self.print_err('Receiving Rq.11 failed - %s' % e)

        return size, time.time()-start, xml


    def send_recv_hello(self):
        """
        HELLO handshake sequence
        :return:
        """
        hello_rq = """<?xml version="1.0" encoding="utf-8"?>
        <hello xmlns="%s">
        <capabilities><capability>urn:ietf:params:netconf:base:1.1</capability>
        <capability>urn:ietf:params:xml:ns:yang:ietf-netconf-monitoring</capability>
        <capability>urn:ietf:params:netconf:capability:candidate:1.0</capability>
        <capability>urn:ietf:params:netconf:capability:rollback-on-error:1.0</capability>
        <capability>urn:ietf:params:netconf:capability:validate:1.1</capability>
        <capability>urn:ietf:params:netconf:capability:confirmed-commit:1.1</capability>
        </capabilities>
        </hello>"""
        sent, time_sent = self.send_rq10_str(hello_rq % self.xmlns)
        recv, time_recv, hello_rs = self.recv_rs10_xml()
        sessionid = hello_rs.findtext('{%s}session-id' % self.xmlns) if hello_rs is not None else '-'
        return sessionid, (sent,recv), (time_sent,time_recv)


    def sessionid_fromfile(self, fname):
        """
        get sessionid from hello file
        :param fname:
        :return:
        """
        return self.find_in_xmlfile(fname, 'session-id')
        
        
    def find_in_xmlfile(self, fname, match):
        """

        :param fname:
        :param match:
        :return:
        """
        res = None
        try:
            tree = ET.parse(fname)
            root = tree.getroot()
            #res = root.find(match, namespaces={'ns':self.xmlns})
            for elm in root.getiterator():
                if elm.tag.endswith("}%s" % match):
                    return elm.text
        except OSError as e:
            self.print_err('XML parsing Rs %s failed - %s' % (fname, e))
        return
        

    def send_cmd(self, cmd='close-session'):
        """
        COMMIT changes
        :return:
        """
        close_rq = """<?xml version="1.0" encoding="utf-8"?>
        <rpc message-id="${TIMESTAMP}" xmlns="%s">
        <%s/>
        </rpc>"""
        sent, time_sent = self.send_rq11_str(close_rq % (self.xmlns, cmd))
        recv, time_recv, xml = self.recv_rs11_xml()
        return (sent,recv), (time_sent,time_recv), self.rs_status(xml)


    def rs_status(self, xml):
        """
        get netconf response status OK or error details
        :param xml:
        :return:
        """
        #print "XML:\n", ET.tostring(xml), "\n"
        # no xml no status
        if xml is None: return ''
        # ok ?
        ok = xml.find('./ns:ok', namespaces={'ns':self.xmlns})
        if ok is not None: return 'OK'
        # error ?
        err = xml.find('./ns:rpc-error', namespaces={'ns':self.xmlns})
        if err is None: return '?'
        # error deails
        err_type = err.find('./ns:error-type', namespaces={'ns':self.xmlns}).text
        err_tag  = err.find('./ns:error-tag',  namespaces={'ns':self.xmlns}).text
        err_sev  = err.find('./ns:error-severity', namespaces={'ns':self.xmlns}).text
        err_path = err.find('./ns:error-path', namespaces={'ns':self.xmlns}).text
        err_msg  = err.find('./ns:error-message', namespaces={'ns':self.xmlns}).text
        return "%s: %s" % (err_sev.upper(), err_tag)


    def send_commit(self):
        """
        COMMIT changes
        :return:
        """
        return self.send_cmd('commit')


    def send_close_session(self):
        """
        CLOSE SESSION
        :return:
        """
        return self.send_cmd('close-session')


    def kMGT(self, val, k=1000):
        """
        human readable format
        :param val:
        :return:
        """
        if val < k: return "%d " % val
        for j in ['k', 'M', 'G', 'T']:
            val = float(val) / k
            if val < k: break
        return "%.3f %s" % (val, j)


    def sec(self, sec):
        """
        human readable format for second
        :param val:
        :return:
        """
        if sec < 1: return "%.3f ms " % (1000*sec)
        min = sec // 60
        sec = sec - 60*min
        if min==0:
            return  "%.2f s" % sec
        if min < 60:
            return "%dm %ds" % (min, sec)
        hod = min // 60
        min = min - 60*hod
        return "%dh %dm %ds" % (hod, min, sec)


    def print_flush(self):
        sys.stdout.flush()
        return
    
    def print_progress(self, char='.'):
        """
        """
        sys.stdout.write(char)
        sys.stdout.flush()
        return


    def print_line(self, hrf=None, tstamp=None, oper=None, par=None, res=None, bytes=(), times=()):
        """
        """
        # timestamp
        if tstamp:              print("[%s]" % datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')),
        # operation
        if oper is not None:    print("%10s:" % oper),
        # parameters
        if par is not None:     print("%40s" % par),
        # result
        if res is not None:     print("... %s" % res),
        # metrics
        if bytes != ():
            # last rq/rs error
            err = " - %s" % self.last_error if self.last_error else ''
            if hrf:
                print("sent:%10sBytes, recv:%10sBytes, rq:%10s, rs:%10s%s" %
                    (self.kMGT(bytes[0]), self.kMGT(bytes[1]), self.sec(times[0]), self.sec(times[1]), err))
            else:
                print("sent:%8d Bytes, recv:%8d Bytes, rq:%8.1f ms, rs:%8.1f ms%s" %
                    (bytes[0], bytes[1], times[0]*1000, times[1]*1000, err))
        # if result is last one eoln
        else:
            if res is not None: print
        # flush
        self.print_flush()
        return


    @staticmethod
    def dbg(msg, level='DBG'):
        """
        static method for debug output to stderr
        :param msg:
        :return:
        """
        # return if debug is not active
        if NetConf.dbg_active is None: return
        # caller function name
        fnc = inspect.stack()[1][3]
        # * means debug all
        if NetConf.dbg_active != '*' and fnc not in NetConf.dbg_active: return
        # print debug info into stderr
        print >>sys.stderr, "%s: %s() - %s" % (level.upper(), fnc,msg)
        return


    @staticmethod
    def process_parameters(lst, idx=1, rs_prefix='rs-', nc=None, loopstat=None, tstamp=False, hformat=False, recursive=True):
        """

        :param lst:
        :param idx:
        :param rs_prefix:
        :param nc:
        :param loopstat:
        :param tstamp:
        :param recursive:
        :return:
        """

        loop = []
        loopcnt = 0
        rsfname = None

        it = iter(lst)
        for par in it:

            # debug
            NetConf.dbg("processing par(%s)" % par)

            # ignore empty values
            if par in ['', ' ']:
                  continue

            # help
            if par in ['-h', '-help', '-?']:
                  usage()
                  sys.exit(1)

            # help
            if par in ['-examples']:
                  usage_examples()
                  sys.exit(1)

            # activate debug
            if par in ['-dbg', '-debug', '-v']:
                  dbg = next(it)
                  if dbg == '*':
                      NetConf.dbg_active = dbg
                  else:
                      NetConf.dbg_active = dbg.split(',')
                  continue

            # response prefix
            if par in ['-rs', '-response', '-prefix']:
                  rs_prefix = next(it)
                  loop.extend([par, rs_prefix])
                  continue

            # no response saving
            if par in ['-nors', '-noresponse']:
                  rs_prefix = None
                  loop.append(par)
                  continue

            # human readable format
            if par in ['-hrf', '-hformat']:
                  hformat = True
                  continue

            # timestamp
            if par in ['-t', '-time', '-timestamp']:
                  tstamp = True
                  continue

            # variable name=val
            if par in ['-var', '-set']:
                  varval = next(it).split('=', 1)
                  name = '${%s}' % varval[0]
                  val  = varval[1]
                  nc.VARS[name] = val
                  nc.print_line(None, tstamp, 'VAR', '%s = %s' % (name, val), 'SET')
                  continue

            # get xpath/xml tag text
            if par in ['-get', '-tag']:
                  tag = next(it)
                  loop.extend([par, tag])
                  if rsfname is not None and rsfname != '/dev/null':
                        val = nc.find_in_xmlfile(rsfname, tag)
                        nc.print_line(None, tstamp, 'TAG', '%s = %s' % (tag, val), 'GET')
                  else:
                        nc.print_line(None, tstamp, 'TAG', 'Missing response', 'WARNING')
                  continue

            # loop
            if par in ['-l', '-loop', '-repeat']:
                  loopcnt = int(next(it))
                  nc.print_line(None, tstamp, 'LOOP', 'REPEAT %d x ' % loopcnt, 'START')
                  loopstat = dict([
                      ('sent',   0),
                      ('recv',   0),
                      ('sentsc', 0),
                      ('recvsc', 0)
                  ])
                  continue

            # connect
            if par in ['-c', '-con', '-connect', '-url']:
                  url = next(it)
                  nc = NetConf(url)
                  nc.print_line(None, tstamp, 'NC.CONNECT', url)
                  err = nc.connect()
                  nc.print_line(res='FAIL - %s' % err if err else 'OK')
                  if err is None: continue
                  sys.exit(-1)

            # hello handshake
            if par in ['-hello']:
                  nc.print_line(None, tstamp, 'HELLO')
                  sessionid, bytes, times =  nc.send_recv_hello()
                  nc.print_line(hrf=hformat, par='session_id=%s' % sessionid, bytes=bytes, times=times)
                  continue

            # hello file handshake
            if par in ['-o', '-hellofile', '-hellorq']:
                  rqfname = next(it)
                  rsfname = rs_prefix+os.path.basename(rqfname) if rs_prefix is not None else '/dev/null'
                  sent, senttime = nc.send_rq10_file(rqfname)
                  recv, recvtime = nc.recv_rs10_file(rsfname)
                  nc.print_line(None, tstamp, 'HELLO')
                  sessionid = nc.sessionid_fromfile(rsfname)
                  nc.print_line(hrf=hformat, par='session_id=%s' % sessionid, bytes=(sent,recv), times=(senttime,recvtime))
                  continue

            # send request from file
            if par in ['-f', '-file', '-rq']:
                  rqfname = next(it)
                  loop.extend([par, rqfname])
                  rsfname = rs_prefix+os.path.basename(rqfname) if rs_prefix is not None else '/dev/null'
                  rsfname = rsfname.replace('${i}', '%03d' % idx)
                  nc.print_line(None, tstamp, 'FILE' if loopstat is None else '%4d. FILE' % idx, '%s -> %s' % (rqfname,rsfname))
                  sent, senttime = nc.send_rq11_file(rqfname)
                  recv, recvtime = nc.recv_rs11_file(rsfname)
                  nc.print_line(hrf=hformat, bytes=(sent,recv), times=(senttime,recvtime))
                  if loopstat is not None:
                      loopstat['sent']   += sent
                      loopstat['recv']   += recv
                      loopstat['sentsc'] += senttime
                      loopstat['recvsc'] += recvtime
                  continue

            # sleep
            if par in ['-s', '-sleep']:
                  sec = next(it)
                  loop.extend([par, sec])
                  sec = float(sec)
                  nc.print_line(None, tstamp, 'SLEEP', 'for %.2f sec' % sec, '%s' % nc.sec(sec))
                  time.sleep(sec)
                  continue

            # commit
            if par in ['-commit']:
                  nc.print_line(None, tstamp, 'COMMIT')
                  bytes, times, status =  nc.send_commit()
                  nc.print_line(hrf=hformat, par=status, bytes=(sent,recv), times=(senttime,recvtime))
                  continue

            # close session
            if par in ['-close']:
                  nc.print_line(None, tstamp, 'CLOSE')
                  bytes, times, status =  nc.send_close_session()
                  nc.print_line(hrf=hformat, par=status, bytes=bytes, times=times)
                  continue

            print >>sys.stderr, 'CLI - invalid parameter [%s] ignored' % par

        # if looping was requested and not inside re-call
        if recursive and loopcnt:
            # loop loopcnt-1 x
            for i in xrange(2, loopcnt+1):
                NetConf.process_parameters(loop, i, rs_prefix, nc, loopstat, tstamp, hformat, recursive=False)
            # final statistics from loop
            nc.print_line(hformat, tstamp, 'LOOP', '=== SUMMARY.STATS ===', None,
                          (loopstat['sent'], loopstat['recv']),
                          (loopstat['sentsc'], loopstat['recvsc']))
        # terminate ssh process
        if recursive and nc: nc.terminate()

        return


    @staticmethod
    def version_check(min=0x02040500, max=0x02090000):
        if min < sys.hexversion < max: return
        print >>sys.stderr, 'WARNING: Unsupported Python %s version' % sys.version_info
        return


if __name__ == '__main__':

    NetConf.version_check()
    NetConf.process_parameters(sys.argv[1:])

