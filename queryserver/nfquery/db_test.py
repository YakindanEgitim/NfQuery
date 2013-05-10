# -*- coding: utf8 -*- 
from storm.locals import *
from MySQLdb import Error as MySQLException
from config import Config, ConfigError
import sys
from models import *
from datetime import * 

def get_store():
    configfile = "/etc/nfquery.conf"
#    configfile = "/home/ahmetcan/Workspace/projects/cfg/nfquery.conf"
    try:
        config = Config(configfile)
    except ConfigError, e:
        print "hata olustu"
        sys.exit(1)

    
    db_user = config.database.db_user
    db_host = config.database.db_host
    db_name = config.database.db_name
    db_password = config.database.db_password

    db = 'mysql://' + db_user  + ':' + db_password + '@' + db_host + '/' + db_name
    database = create_database(db)
    store = Store(database)
    return store


store = get_store()
log_packet = {}
now = datetime.now()
before_thirty_min = now - timedelta(minutes = 30)
now = int(datetime.now().strftime("%s"))
before_thirty_min = now - (30 * 60)

log_packets =store.find(LogPacket, And(LogPacket.creation_time < now, LogPacket.creation_time > before_thirty_min) )
packet_number = 0
for packet in log_packets:
    if packet.host.host_name not in log_packet.keys():
        log_packet[packet.host.host_name] = {}
    log_packet[packet.host.host_name][packet_number] = {}
    log_packet[packet.host.host_name][packet_number]['user'] = packet.user.user
    log_packet[packet.host.host_name][packet_number]['client'] = packet.client.client
    log_packet[packet.host.host_name][packet_number]['creation_time'] = packet.creation_time
    log_packet[packet.host.host_name][packet_number]['facility'] = packet.facility.facility
    log_packet[packet.host.host_name][packet_number]['severity'] = packet.severity.severity
    log_packet[packet.host.host_name][packet_number]['program'] = packet.program.name
    log_packet[packet.host.host_name][packet_number]['host'] = packet.host.host_name
    packet_number = packet_number + 1
print log_packet
#return log_packet

