import logging
from twisted.internet import reactor, ssl
from txjsonrpc.web.jsonrpc import Proxy

from OpenSSL import SSL
from twisted.python import log
from nfqueryUI.settings import ROOT_CERTIFICATE, CLIENT_CERTIFICATE, CLIENT_KEY, RPC_URL

class AltCtxFactory(ssl.ClientContextFactory):
    def verifyCallback(self, connection, x509, errnum, errdepth, ok):
        pass

    def getContext(self):
        #self.method = SSL.SSLv23_METHOD
        ctx = ssl.ClientContextFactory.getContext(self)
        ctx.set_verify(SSL.VERIFY_PEER, self.verifyCallback)
        ctx.load_verify_locations(ROOT_CERTIFICATE)
        ctx.use_certificate_file(CLIENT_CERTIFICATE)
        ctx.use_privatekey_file(CLIENT_KEY)
        return ctx

class Client:
    def __init__(self):
        self.proxy = Proxy(RPC_URL, ssl_ctx_factory=AltCtxFactory)
        self.result = None

    def printValue(self, value):
        self.result = value        
        reactor.stop()

    def printError(self, error):
        pass 

    def call(self, method, *args):
        d = self.proxy.callRemote(method, *args)
        d.addCallback(self.printValue).addErrback(self.printError)
        reactor.run()

        return self.result
