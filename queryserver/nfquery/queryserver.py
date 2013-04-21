# This file is part of NfQuery.  NfQuery is free software: you can
# redistribute it and/or modify it under the terms of the GNU General Public
# License as published by the Free Software Foundation, version 3.
#
# This program is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE.  See the GNU General Public License for more
# details.
#
# You should have received a copy of the GNU General Public License along with
# this program; if not, write to the Free Software Foundation, Inc., 51
# Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.
#
# Copyright NfQuery Team Members

#!/usr/local/bin/python

import os
import sys
import time
import logging
import resource
import threading
import multiprocessing
import atexit
from datetime import date
from config import Config, ConfigError

# package imports
import db
import logger
from querymanager import QueryManager



from syslogparser.parser import *
######################################################
# Special Imports For Twisted JSON_RPC  -> txjsonrpc
from twisted.web import server
from twisted.internet import ssl,reactor
from OpenSSL import SSL
from twisted.internet import task
#from twisted.internet.protocol import Factory
#from twisted.application import service,internet

from jsonrpc import jsonRPCServer
######################################################


class QueryServer:
    
    def __init__(self, configfile, loglevel=None):
        # start logging
        logger.LOGLEVEL = loglevel
        self.qslogger = logger.createLogger('queryserver')
        
        # Parse Config File
        try:
            self.configfile = configfile
            self.config = Config(configfile)
        except ConfigError, e:
            self.qslogger.info("Please check configuration file syntax")
            self.qslogger.info("%s" % e)
            sys.exit(1)
   
        self.qslogger.debug('Parsing configuration file options')

        # Prepare Config File Sections
        ConfigSections = {
            'nfquery'  : ['path','sources_path','syslog_parser_path','host','port','ipv6', 'cert_file', 'key_file', 'logfile'], 
            'plugins'  : ['organization', 'adm_name', 'adm_mail', 'adm_tel', 'adm_publickey_file', 'prefix_list', 'plugin_ip'],
            'database' : ['db_host','db_name','db_user','db_password'], 
            'sources'  : ['source_name','source_link','source_file','threat_type','output_file','parser','time_interval'],
            'syslog'  : ['host','syslog_path','parser_script','normalizers']
        }

        # Check Config File Sections
        #self.qslogger.debug(self.config)
        sections = self.config.keys()
        if(set(ConfigSections.keys()).issubset(set(sections))):
            self.qslogger.debug('Main configuration options are OK')
            for section,option in self.config.iteritems():
                #print section,option
                #print dir(option)
                # Check if the section has a loop like 'sources' option.
                if hasattr(option, 'keys') and hasattr(option, '__getitem__') and (option):
                    if (set(ConfigSections[section]).issubset(set(option.keys()))):
                        self.qslogger.debug(str(ConfigSections[section]) + 'exists')
                    else:
                        raise ConfigError(str(ConfigSections[section]) + ' option does not exists in the configuration file.' + 
                                          'Please add the required option to conf file and check the manual' )
                elif hasattr(option, '__iter__') and (option):
                    if (set(ConfigSections[section]).issubset(set(option[0].keys()))):
                        self.qslogger.debug(str(ConfigSections[section]) + 'exists')
                    else:
                        self.qslogger.info(str(ConfigSections[section]) + ' option does not exists in the configuration file.')
                        self.qslogger.info('Please add the required option to conf file and check the manual')
                        sys.exit(1)
                else:
                    self.qslogger.info('Unknown configuration file option, Check the code!')
                    sys.exit(1)
        else:
            self.qslogger.info('One of the main configuration options does not exists')
            self.qslogger.info('You should have all \'nfquery, database, plugin, sources\' options in the configuration file')
            self.qslogger.info('Please add the required option and check the manual')
        
    def verifyCallback(self, connection, x509, errnum, errdepth, ok):
        if not ok:
            print 'invalid cert from subject:', x509.get_subject()
            return False
        else:
            print "Certs are fine"
        return True



    def startSyslogParser(self):
        '''
            Start Syslog Parser
        '''
        self.queryManager.executeSyslogParser(self.config.syslog[0].parser_script,self.configfile)

       
    def startJSONRPCServer(self):
        '''
            Start Json RPC Server, bind to socket and listen for incoming connections from plugins.
        '''
        rpc_protocol = jsonRPCServer(self.queryManager)
        rpcserver = server.Site(rpc_protocol)
        
        # sslmethod = ssl.SSL.SSLv23_METHOD and other could be implemented here.
        # For TLSV1
        
        contextFactory = ssl.DefaultOpenSSLContextFactory(self.config.nfquery.key_file, self.config.nfquery.cert_file,
                                                                                        sslmethod=ssl.SSL.SSLv23_METHOD)
        ctx = contextFactory.getContext()
        ctx.set_verify(SSL.VERIFY_PEER | SSL.VERIFY_FAIL_IF_NO_PEER_CERT, self.verifyCallback)
        
        # Since we have self-signed certs we have to explicitly
        # tell the server to trust them.
        ctx.load_verify_locations(self.config.nfquery.root_cert_file)
        reactor.listenSSL( self.config.nfquery.port, rpcserver, contextFactory)

        #reactor.listenTCP(self.config.nfquery.port, rpcserver)

        self.qslogger.info('Starting QueryServer')
        self.qslogger.info('Listening for plugin connections on port : %s' % self.config.nfquery.port)


    def startScheduler(self):
        '''
            Schedule parsers to be called according to time interval parameter indicated in conf file.
        '''
        for index in range(len(self.config.sources)):
            routine = task.LoopingCall(self.queryManager.executeParsers, self.config.sources[index].parser) # call the parser
            routine.start(int(self.config.sources[index].time_interval) * 60, now=False) # call according to time interval in seconds
        self.qslogger.info('Starting the Scheduler')


    def start(self):
        '''
            Starting all modules.
        ''' 
        # Start Database Connection 
        self.store = db.get_store(self.config.database)

        # Check if configuration file has changed or not
        # If changed run reconfig sources or reconfig plugins.
        # ASSUME THAT WE HANDLED HERE!!
        # So db and conf file is consistent.

        # Start QueryManager
        self.queryManager = QueryManager(sources=self.config.sources, plugins=self.config.plugins)
        self.queryManager.start()

        # Start JSONRPCServer
        self.startJSONRPCServer()

        # Start Scheduler
        self.startScheduler()


        #Start syslog parser
        self.startSyslogParser()

        # Set shutdown handler
        atexit.register(self.stop)


    def stop(self):
        # Stop reactor and exit
        if reactor.running:
            reactor.stop()
        self.qslogger.info('QueryServer is stopped')
        sys.exit()


    def reconfigure(self, flag):
        # Start Database Connection
        self.store = db.get_store(self.config.database)
        # Start Query Manager
        if flag == 'sources':
            self.queryManager = QueryManager(sources=self.config.sources)
            self.queryManager.reconfigureSources()
        elif flag == 'plugins':
            self.queryManager = QueryManager(plugins=self.config.plugins)
            self.queryManager.reconfigurePlugins()


    def run(self):
        reactor.callWhenRunning(self.start)
        reactor.run()



