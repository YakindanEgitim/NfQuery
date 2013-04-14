import tailer
#from tail import *
from config import Config
from logsparser import lognormalizer
import re



class Parser:
    def __init__(self, parserFile):
        self.parserFile = parserFile
        f = file('parser.cfg')
        self.config = Config(f)
        self.lognorm = lognormalizer.LogNormalizer(self.config.logparser.normalizers)

##    def getLineFromLogFile(self, logline):
##        self.parse(logline)

    def parse(self, logline):
        log = {'raw' : logline}
        self.lognorm.lognormalize(log)
        print log
        if log['program'] == "apache":
            self.pattern = Pattern("apache")
            apache_line = log['raw'].split("apache: ")[1]
            matched = self.pattern.pattern.match(apache_line)
            print matched.groupdict()
            print matched.groupdict()['host']
            print "\n\n"

    def start(self):
        #self.pattern = Pattern("apache")
        for logline in tailer.follow(open(self.parserFile)):
            self.parse(logline)
        #tail(self.parserFile, self.getLineFromLogFile).mainloop()
