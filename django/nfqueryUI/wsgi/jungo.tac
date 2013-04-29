from twisted.application import internet, service
from jungo import JungoHttpService

application = service.Application("jungo")
jungoService = JungoHttpService(8000)
jungoService.setServiceParent(application)
