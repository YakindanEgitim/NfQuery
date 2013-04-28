from twisted.application import internet
from twisted.web import resource, wsgi, static, server
from twisted.python import threadpool
from twisted.internet import reactor
from nfquery import application

class SharedRoot(resource.Resource):
    """Root resource that combines the two sites/entry points"""
    WSGI = None

    def getChild(self, child, request):
        request.prepath.pop()
        request.postpath.insert(0, child)
        return self.WSGI

    def render(self, request):
        return self.WSGI.render(request)

class JungoHttpService(internet.TCPServer):

    def __init__(self, port):
        self.__port = port
        pool = threadpool.ThreadPool()
        sharedRoot = SharedRoot()

                          # substitute with your custom WSGIResource
        sharedRoot.WSGI = wsgi.WSGIResource(reactor, pool, application)
        sharedRoot.putChild('static', static.File("/home/serhat/NfQuery/django/nfqueryUI/static"))
        internet.TCPServer.__init__(self, port, server.Site(sharedRoot))
        self.setName("WSGI/HttpJungo")
        self.pool = pool


    def startService(self):
        internet.TCPServer.startService(self)
        self.pool.start()

    def stopService(self):
        self.pool.stop()
        return internet.TCPServer.stopService(self)

    def getServerPort(self):
        """ returns the port number the server is listening on"""
        return self.__port
