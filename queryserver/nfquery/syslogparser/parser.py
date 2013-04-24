#!/usr/bin/python
#imports standart library
import sys
import re

#import third party modules
import tailer
from config import Config, ConfigError
from logsparser import lognormalizer

from nfquery import db
from nfquery.models import *


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

    def insert_to_database(self, syslog_data):
        log_packet = LogPacket() 
        if 'program' in syslog_data.keys():
            program = self.store.find(Program, Program.name == unicode(syslog_data['program'])).one()
            if program == None:
                program = Program()
                program.name = unicode(syslog_data['program'])
                self.store.add(program)      
            log_packet.program = program
        if 'severity_code' in syslog_data.keys():
            severity = self.store.find(Severity, Severity.severity == unicode(syslog_data['severity_code'])).one()
            if severity == None:
                severity = Severity()
                severity.severity = unicode(syslog_data['severity_code'])
                self.store.add(severity)       
            log_packet.severity = severity
 
        if 'facility_code' in syslog_data.keys():
            facility = self.store.find(Facility, Facility.facility == unicode(syslog_data['facility_code'])).one()
            if facility == None:
                facility = Facility()
                facility.facility = unicode(syslog_data['facility'])
                self.store.add(facility) 
            log_packet.facility = facility
        
        if 'date' in syslog_data.keys():
            date = self.store.find(Time, Time.time == syslog_data['date']).one()
            if date == None:
                date = Time()
                date.time = syslog_data['date']
                self.store.add(date) 
            log_packet.creation_time = date
        
        if 'information' in syslog_data.keys():
            informations = syslog_data['information']
            if 'user' in informations.keys():
                log_user = self.store.find(LogUser, LogUser.user == unicode(informations['user'])).one()
                if log_user == None:
                    log_user = LogUser()
                    log_user.user = unicode(informations['user'])
                    self.store.add(log_user)
                log_packet.user = log_user
 
            if 'host' in informations.keys():
                client = self.store.find(Client, Client.client == unicode(informations['host'])).one()
                if client == None:
                    client = Client()
                    client.client = unicode(informations['host'])
                    self.store.add(client) 
                log_packet.client = client
        self.store.add(log_packet) 
        self.store.commit()     

    def __init__(self, configfile):
        # Parse Config File
        try:
            self.config = Config(configfile)
        except ConfigError, e:
            self.qslogger.info("Please check configuration file syntax")
            self.qslogger.info("%s" % e)
            sys.exit(1)

        self.store = db.get_store(self.config.database)
         
        self.parserFile = self.config.syslog[0].syslog_path

        self.lognorm = lognormalizer.LogNormalizer(self.config.syslog[0].normalizers)

    def parse(self, logline):
        log = {'raw' : logline}
        self.lognorm.lognormalize(log)
        print log
        if 'program' in log.keys():
            if log['program'] == "apache":
                self.pattern = Pattern("apache")
                apache_line = log['raw'].split(":",3)[-1].lstrip()
                matched = self.pattern.pattern.match(apache_line)
                if matched:
                    log['information'] = matched.groupdict()
                    self.insert_to_database(log)
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
                vsftpd_log = {"user" : user, "message" : message, "host" : client}
                log['information'] = vsftpd_log
                self.insert_to_database(log)
                print vsftpd_log
       
        print "\n\n"
        print "LOGG"
        print log
        print "\n\n"
    def start(self):
        for logline in tailer.follow(open(self.parserFile)):
            self.parse(logline)


if __name__ == "__main__":
    configfile = sys.argv[1]
    parser = Parser(configfile)
    parser.start()