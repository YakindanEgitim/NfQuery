#!/usr/local/bin/python

from datetime import date
from config import Config
import os
import SocketServer
import argparse
import MySQLdb

# nfquery imports
from db import db
from querygenerator import *

# List of stuff accessible to importers of this module.

# global paths
nfquery = "/usr/local/nfquery/"
sourcepath = nfquery + "sources/amada/"
outputpath = nfquery + "outputs/amada/"

#q=Query(1, "amada", "FAKE-AV", "27.03.1990", ip="193.140.94.94").__dict__
#queryfile = open('outputs/test.jason', mode='w')
#queryfile.writelines(simplejson.dumps(q, indent=4)+"\n")
#queryfile.write(simplejson.dumps(q, indent=4))
#queryfile.write(simplejson.dumps(q, indent=4))
#queryfile.close()
#
#anotherfile=open('test.jason', mode='r')

#loaded = simplejson.load(anotherfile)
#print loaded


class ThreadingTCPRequestHandler(SocketServer.BaseRequestHandler):
    '''
        The RequestHandler class for our server.

        It is instantiated once per connection to the server, and must
        override the handle() method to implement communication to the
        client.
    '''
    def handle(self):
        # self.request is the TCP socket connected to the client
        self.data = self.request.recv(1024).strip()
        print "%s wrote:" % self.client_address[0]
        print self.data
        # just send back the same data, but upper-cased
        self.request.send(self.data.upper())

class ThreadingTCPServer(SocketServer.ThreadingMixIn, SocketServer.TCPServer):
    daemon_threads=True
    allow_reuse_address=True
    def __init__(self, server_address, RequestHandlerClass):
        SocketServer.TCPServer.__init__(self, server_address, RequestHandlerClass)


if __name__ == "__main__":
    # Parse Command Line Arguments
    parser = argparse.ArgumentParser(description="Process arguments")
    parser.add_argument('conf_file', metavar="--conf", type=str, nargs='?', help='nfquery configuration file')
    args = parser.parse_args()

    # Parse Configuration File
    # Notice that configuration file is assigned to args object as args.conf_file
    # We pass nfquery.conf file to Config object to parse general configuration 
    # parameters of NfQuery
    nffile=Config(args.conf_file)
    try:
        database = db(nffile.DB_HOST, nffile.DB_USER, nffile.DB_PASSWORD, nffile.DB_NAME)
        cursor1 = database.get_database_cursor()
        cursor2 = database.get_database_cursor()
    except MySQLdb.Error, e:
        #print "Error %d: %s" % (e.args[0], e.args[1])
        sys.exit ("Error %d: %s" % (e.args[0], e.args[1]))

    subscription_list = generateSourceSubscriptionPackets(1, cursor1, cursor2)
    for i in subscription_list:
        print i.__dict__
    
    database.end_database_cursor()

    HOST, PORT = "localhost", 7777

    ## Create the server, binding to localhost on port 9999
    server = SocketServer.ThreadingTCPServer((HOST, PORT), ThreadingTCPRequestHandler)
 
    ## Activate the server; this will keep running until you
    ## interrupt the program with Ctrl-C
    server.serve_forever()





