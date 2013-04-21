import tailer
#from tail import *
from config import Config, ConfigError
from logsparser import lognormalizer
import re
import sys

class Pattern:
    def __init__(self, program):
        if (program == "apache"):
            self.pattern = self.get_apache_log_pattern()


    def get_apache_log_pattern(self):
        # this pattern to parse apache access log
        pattern_re = [
         r'(?P<host>\S+)',                   # host %h
         r'\S+',                             # indent %l (unused)
         r'(?P<user>\S+)',                   # user %u
         r'\[(?P<time>.+)\]',                # time %t
         r'"(?P<request>.+)"',               # request "%r"
         r'(?P<status>[0-9]+)',              # status %>s
         r'(?P<size>\S+)',                   # size %b (careful, can be '-')
         r'"(?P<referer>.*)"',               # referer "%{Referer}i"
         r'"(?P<agent>.*)"',                 # user agent "%{User-agent}i"
   

        ]
        pattern = re.compile(r'\s+'.join(pattern_re)+r'\s*\Z')
        return pattern






class Parser:
    def __init__(self, configfile):

        # Parse Config File
        try:
            self.config = Config(configfile)
        except ConfigError, e:
            self.qslogger.info("Please check configuration file syntax")
            self.qslogger.info("%s" % e)
            sys.exit(1)
        self.parserFile = self.config.syslog[0].syslog_path

 #       f = file('parser.cfg')
 #       self.config = Config(f)
        self.lognorm = lognormalizer.LogNormalizer(self.config.syslog[0].normalizers)

##    def getLineFromLogFile(self, logline):
##        self.parse(logline)

    def parse(self, logline):
        log = {'raw' : logline}
        self.lognorm.lognormalize(log)
        print log
        if log['program'] == "apache":
            self.pattern = Pattern("apache")
            apache_line = log['raw'].split(":",3)[-1].lstrip()
            matched = self.pattern.pattern.match(apache_line)
            if matched:
                print matched.groupdict()
                print matched.groupdict()['host']
                print "\n\n"
        
        if log['program'] == "vsftpd":
            self.pattern = Pattern("vsftpd")
            vsftpd_line = log['body'].split(":")
            vsftpd_line_first_part = vsftpd_line[0]
            user = vsftpd_line_first_part.split("]")[0][1:]
            message = " ".join(vsftpd_line_first_part.split()[1:])
            client = vsftpd_line[1].lstrip().split()[1][1:-1]
            vsftpd_log = {"user" : user, "message" : message, "client" : client}
            print vsftpd_log
       

    def start(self):
        #self.pattern = Pattern("apache")
        for logline in tailer.follow(open(self.parserFile)):
            self.parse(logline)
        #tail(self.parserFile, self.getLineFromLogFile).mainloop()


if __name__ == "__main__":
    configfile = sys.argv[1]
    parser = Parser(configfile)
    parser.start()
