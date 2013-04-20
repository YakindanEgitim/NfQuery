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

from storm.locals import *
from MySQLdb import Error as MySQLException
import sys


__all__ = [ 'get_store' ]

__store = None

def initialize_db(store):


    store.execute(
		  "CREATE TABLE time ("						     +
  		  "id int(10) unsigned NOT NULL AUTO_INCREMENT," 		     +
 		  "time datetime NOT NULL,"					     +
		  "PRIMARY KEY (id)"						     +
		  ") ENGINE=InnoDB AUTO_INCREMENT=13357 DEFAULT CHARSET=utf8;"
		 )
    store.execute(
		  "CREATE TABLE category ("					     +
	          "id int(10) unsigned NOT NULL AUTO_INCREMENT,"                     +
  		  "category varchar(20) NOT NULL,"			             +
  	          "PRIMARY KEY (id)"			                             +
	          ") ENGINE=InnoDB  DEFAULT CHARSET=utf8"
		 )
    store.execute(
		  "CREATE TABLE type ("						     +
		  "id int(10) unsigned NOT NULL AUTO_INCREMENT,"                     +
		  "type varchar(40) NOT NULL,"                                       +
		  "PRIMARY KEY (id)"                                                 +
		  ") ENGINE=InnoDB DEFAULT CHARSET=utf8"
		 )
    store.execute(
                  "CREATE TABLE prefix("                                             + 
                  "id INT UNSIGNED NOT NULL AUTO_INCREMENT,"                         +
                  "prefix TEXT  COLLATE utf8_unicode_ci NOT NULL,"            +
                  "PRIMARY KEY (id)"                                                 +
                  ")ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci"      
                 )

    store.execute(
		"CREATE TABLE application ("					     +
  		"id int(10) unsigned NOT NULL AUTO_INCREMENT,"			     +
  		"version int(10) unsigned NOT NULL,"                                 +
  		"creation_time varchar(20) NOT NULL,"                                +
  		"PRIMARY KEY (id)"                                                   +
		") ENGINE=InnoDB DEFAULT CHARSET=utf8"
		)

   

    store.execute(
		"CREATE TABLE plugin ("						     +
 		"id int(10) unsigned NOT NULL AUTO_INCREMENT,"			     +
  		"organization varchar(30) COLLATE utf8_unicode_ci NOT NULL,"         +
  		"adm_name varchar(30) COLLATE utf8_unicode_ci NOT NULL,"             +
  		"adm_mail varchar(30) COLLATE utf8_unicode_ci NOT NULL,"             +
  		"adm_tel varchar(20) COLLATE utf8_unicode_ci NOT NULL,"              +
  		"adm_publickey_file varchar(50) COLLATE utf8_unicode_ci NOT NULL,"   +
  		"prefix_id int(10) unsigned NOT NULL,"                               +
  		"plugin_ip varchar(20) COLLATE utf8_unicode_ci NOT NULL,"            +
  		"checksum varchar(32) COLLATE utf8_unicode_ci NOT NULL,"             +
  		"registered INT NOT NULL,"                                           +
  		"PRIMARY KEY (id),"                                                  +
  		"UNIQUE KEY plugin_ip (plugin_ip),"                                  +
  		"KEY prefix_id (prefix_id),"                                         +
  		"CONSTRAINT plugin_ibfk_1 FOREIGN KEY (prefix_id) REFERENCES prefix (id)"+
		") ENGINE=InnoDB AUTO_INCREMENT=70 DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;"

	         ) 


    store.execute(
                  "CREATE TABLE parser("                                             + 
                  "id INT UNSIGNED NOT NULL AUTO_INCREMENT,"                         +
                  "name VARCHAR(75) COLLATE utf8_unicode_ci NOT NULL,"               +
                  "time_interval SMALLINT(6) NOT NULL,"                              +
		  "checksum varchar(32) COLLATE utf8_unicode_ci DEFAULT NULL, "      +                 
		   "PRIMARY KEY (id)"                                                +
                  ")ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci"
                 )


    store.execute(
                  "CREATE TABLE threat("                                             + 
                  "id INT UNSIGNED NOT NULL AUTO_INCREMENT,"                         +
                  "type VARCHAR(20) COLLATE utf8_unicode_ci NOT NULL,"               +
                  "UNIQUE KEY type (type),"                                          + 
                  "PRIMARY KEY (id)"                                                 +
                  ")ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci"
                 )

    store.execute(
                  "CREATE TABLE source("                                             +
                  "id INT UNSIGNED NOT NULL AUTO_INCREMENT,"                         +
                  "name VARCHAR(75) COLLATE utf8_unicode_ci NOT NULL,"               +
                  "parser_id INT UNSIGNED NOT NULL,"                                 +
                  "checksum VARCHAR(32) COLLATE utf8_unicode_ci NOT NULL,"           +
                  "link VARCHAR(75) COLLATE utf8_unicode_ci NOT NULL,"               +
                  "is_active INT UNSIGNED NOT NULL,"                                 +
                  "threat_id int unsigned NOT NULL,"                                 +
                  "FOREIGN KEY (threat_id) REFERENCES threat (id),"		     +
                  "FOREIGN KEY (parser_id) REFERENCES parser (id) ON UPDATE CASCADE,"+
                  "PRIMARY KEY (id)"                                                 +
                  ")ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci"
                 )

    store.execute(
                  "CREATE TABLE query ("                                             + 
                  "id INT UNSIGNED NOT NULL AUTO_INCREMENT,"                         + 
                  "source_id INT UNSIGNED NOT NULL,"                                 +
		  "update_time_id int(10) unsigned DEFAULT NULL,"		     +
                  "type SMALLINT UNSIGNED NOT NULL,"                                 + 
                  "checksum VARCHAR(32) NOT NULL,"                                   + 
		  "creation_time_id int(10) unsigned NOT NULL,"		     	     +
	          "type_id int(10) unsigned NOT NULL,"				     +
                  "category_id int(10) unsigned NOT NULL,"                           +
                  "PRIMARY KEY (id),"                                                +
                  "FOREIGN KEY (source_id) REFERENCES source(id) ON DELETE CASCADE"  + 
                  ")ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci"
                 )

    store.execute(
		  "CREATE TABLE alert ("					     +
  		  "id int(10) unsigned NOT NULL AUTO_INCREMENT,"                     +
  		  "alert_type int(10) unsigned NOT NULL,"                              +
  		  "query_id int(10) unsigned NOT NULL,"                              +
  		  "identified_plugin_id int(10) unsigned NOT NULL,"                  +
  		  "identifier_plugin_id int(10) unsigned,"                           +
  		  "start_time int(11) unsigned NOT NULL,"                            +
  		  "end_time int(11) unsigned NOT NULL,"                              +
  		  "first_seen int(11) unsigned NOT NULL,"                            +
  		  "checksum varchar(32) COLLATE utf8_unicode_ci NOT NULL,"           +
  		  "PRIMARY KEY (id),"                                                +
  		  "FOREIGN KEY (identified_plugin_id) REFERENCES plugin(id) ON DELETE CASCADE,"     +
  		  "FOREIGN KEY (identifier_plugin_id) REFERENCES plugin(id) ON DELETE CASCADE,"     +
  		 # "FOREIGN KEY (start_time_id) REFERENCES time(id) ON DELETE CASCADE,"                    +
  		 # "FOREIGN KEY (end_time_id) REFERENCES time(id) ON DELETE CASCADE,"                      +
  		  "FOREIGN KEY (query_id) REFERENCES query(id)"                      +
                  ")ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci"
		)

    store.execute(
		  "CREATE TABLE query_packet ("				     +
  		  "id int(10) unsigned NOT NULL AUTO_INCREMENT,"		     +
  		  "validation_id int(10) unsigned NOT NULL,"			     +
		  "query_id int(10) unsigned NOT NULL,"				     +
		  "PRIMARY KEY (id),"                                                +
		  "KEY validation_id (validation_id),"                               +
		  "KEY query_id (query_id),"					     +
		  "CONSTRAINT query_packet_ibfk_1 FOREIGN KEY (validation_id) REFERENCES query (id) ON DELETE CASCADE,"+
		  "CONSTRAINT query_packet_ibfk_2 FOREIGN KEY (query_id) REFERENCES query (id) ON DELETE CASCADE"      +
	     	  ")ENGINE=InnoDB AUTO_INCREMENT=15086 DEFAULT CHARSET=utf8"	     

    		 )
    store.execute(
                  "CREATE TABLE subscription("                                       + 
                  "id INT UNSIGNED NOT NULL AUTO_INCREMENT,"                         +
                  "type SMALLINT unsigned NOT NULL,"                                 +
                  "name VARCHAR(50) COLLATE utf8_unicode_ci NOT NULL,"               +
                  "PRIMARY KEY (id),"                                                +
                  "UNIQUE KEY name (name)"                                           +
                  ")ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci"
                 )

    store.execute(
		  "CREATE TABLE subscription_packet ("  			     +
  		  "id int(10) unsigned NOT NULL AUTO_INCREMENT,"		     +
		  "subscription_id int(10) unsigned NOT NULL,"			     +
		  "query_packet_id int(10) unsigned NOT NULL,"			     +
		  "PRIMARY KEY (id),"						     +
		  "KEY subscription_id (subscription_id),"			     +
		  "KEY query_packet_id (query_packet_id),"			     +
		  "CONSTRAINT subscription_packet_ibfk_1 FOREIGN KEY (subscription_id) REFERENCES subscription (id),"+
		  "CONSTRAINT subscription_packet_ibfk_2 FOREIGN KEY (query_packet_id) REFERENCES query_packet (id) ON DELETE CASCADE"+
		  ") ENGINE=InnoDB AUTO_INCREMENT=35836 DEFAULT CHARSET=utf8;"

                 )

    store.execute(
                  "CREATE TABLE ip("                                                 +
                  "id INT UNSIGNED NOT NULL AUTO_INCREMENT,"                         +
                  "ip VARCHAR(20) COLLATE utf8_unicode_ci NOT NULL,"                 +
                  "ip_int BIGINT(20) UNSIGNED NOT NULL,"                             +
                  "PRIMARY KEY (id)"                                                 +
                  ")ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci"
                 )

    store.execute(
                  "CREATE TABLE src_ip("                                             + 
                  "id INT UNSIGNED NOT NULL AUTO_INCREMENT,"                         +
                  "query_id INT UNSIGNED NOT NULL,"                                  +
                  "ip_id INT UNSIGNED NOT NULL,"                                     +
                  "FOREIGN KEY (ip_id) REFERENCES ip(id) ON DELETE CASCADE,"         + 
                  "FOREIGN KEY (query_id) REFERENCES query(id) ON DELETE CASCADE,"   + 
                  "PRIMARY KEY (id)"                                                 +
                  ")ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci"
                 )

    store.execute(
                  "CREATE TABLE dst_ip("                                             + 
                  "id INT UNSIGNED NOT NULL AUTO_INCREMENT,"                         +
                  "query_id INT UNSIGNED NOT NULL,"                                  +
                  "ip_id INT UNSIGNED NOT NULL,"                                     +
                  "FOREIGN KEY (ip_id) REFERENCES ip(id) ON DELETE CASCADE,"         + 
                  "FOREIGN KEY (query_id) REFERENCES query(id) ON DELETE CASCADE,"   + 
                  "PRIMARY KEY (id)"                                                 +
                  ")ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci"
                 )

    store.execute(
                  "CREATE TABLE port("                                               + 
                  "id INT UNSIGNED NOT NULL AUTO_INCREMENT,"                         +
                  "port INT UNSIGNED NOT NULL,"                                      +
                  "PRIMARY KEY (id)"                                                 +
                  ")ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci"
                 )

    store.execute(
                  "CREATE TABLE src_port("                                           + 
                  "id INT UNSIGNED NOT NULL AUTO_INCREMENT,"                         +
                  "query_id INT UNSIGNED NOT NULL,"                                  +
                  "port_id INT UNSIGNED NOT NULL,"                                   +
                  "FOREIGN KEY (port_id) REFERENCES port(id) ON DELETE CASCADE,"     +
                  "FOREIGN KEY (query_id) REFERENCES query(id) ON DELETE CASCADE,"   +
                  "PRIMARY KEY (id)"                                                 +
                  ")ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci"
                 )

    store.execute(
                  "CREATE TABLE dst_port("                                           + 
                  "id INT UNSIGNED NOT NULL AUTO_INCREMENT,"                         +
                  "query_id INT UNSIGNED NOT NULL,"                                  +
                  "port_id INT UNSIGNED NOT NULL,"                                   +
                  "FOREIGN KEY (port_id) REFERENCES port(id) ON DELETE CASCADE,"     +
                  "FOREIGN KEY (query_id) REFERENCES query(id) ON DELETE CASCADE,"   +
                  "PRIMARY KEY (id)"                                                 +
                  ")ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci"
                 )

    store.execute(
                  "CREATE TABLE proto("                                              + 
                  "id INT UNSIGNED NOT NULL AUTO_INCREMENT,"                         +
                  "query_id INT UNSIGNED NOT NULL,"                                  +
                  "proto VARCHAR(3) NOT NULL,"                                       +
                  "PRIMARY KEY (id),"                                                +
                  "FOREIGN KEY (query_id) REFERENCES query(id) ON DELETE CASCADE"    +
                  ")ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci"
                 )

    store.execute(
                  "CREATE TABLE protocol_version("                                   + 
                  "id INT UNSIGNED NOT NULL AUTO_INCREMENT,"                         +
                  "query_id INT UNSIGNED NOT NULL,"                                  +
                  "protocol_version VARCHAR(4) NOT NULL,"                            +
                  "PRIMARY KEY (id),"                                                +
                  "FOREIGN KEY (query_id) REFERENCES query(id) ON DELETE CASCADE"    +
                  ")ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci"
                 )

    store.execute(
                  "CREATE TABLE packets("                                            + 
                  "id INT UNSIGNED NOT NULL AUTO_INCREMENT,"                         +
                  "query_id INT UNSIGNED NOT NULL,"                                  +
                  "packets INT UNSIGNED NOT NULL,"                                   +
                  "PRIMARY KEY (id),"                                                +
                  "FOREIGN KEY (query_id) REFERENCES query(id) ON DELETE CASCADE"    +
                  ")ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci"
                 )

    store.execute(
                  "CREATE TABLE bytes("                                              + 
                  "id INT UNSIGNED NOT NULL AUTO_INCREMENT,"                         +
                  "query_id INT UNSIGNED NOT NULL,"                                  +
                  "bytes INT UNSIGNED NOT NULL,"                                     +
                  "PRIMARY KEY (id),"                                                +
                  "FOREIGN KEY (query_id) REFERENCES query(id) ON DELETE CASCADE"    +
                  ")ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci"
                 )

    store.execute(
                  "CREATE TABLE bps("                                                + 
                  "id INT UNSIGNED NOT NULL AUTO_INCREMENT,"                         +
                  "query_id INT UNSIGNED NOT NULL,"                                  +
                  "bps INT UNSIGNED NOT NULL,"                                       +
                  "PRIMARY KEY (id),"                                                +
                  "FOREIGN KEY (query_id) REFERENCES query(id) ON DELETE CASCADE"    +
                  ")ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci"
                 )

    store.execute(
                  "CREATE TABLE pps("                                                + 
                  "id INT UNSIGNED NOT NULL AUTO_INCREMENT,"                         +
                  "query_id INT UNSIGNED NOT NULL,"                                  +
                  "bps INT UNSIGNED NOT NULL,"                                       +
                  "PRIMARY KEY (id),"                                                +
                  "FOREIGN KEY (query_id) REFERENCES query(id) ON DELETE CASCADE"    +
                  ")ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci"
                 )

    store.execute(
                  "CREATE TABLE bpp("                                                + 
                  "id INT UNSIGNED NOT NULL AUTO_INCREMENT,"                         +
                  "query_id INT UNSIGNED NOT NULL,"                                  +
                  "bpp INT UNSIGNED NOT NULL,"                                       +
                  "PRIMARY KEY (id),"                                                +
                  "FOREIGN KEY (query_id) REFERENCES query(id) ON DELETE CASCADE"    +
                  ")ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci"
                 )

    store.execute(
                  "CREATE TABLE duration("                                           + 
                  "id INT UNSIGNED NOT NULL AUTO_INCREMENT,"                         +
                  "query_id INT UNSIGNED NOT NULL,"                                  +
                  "duration INT UNSIGNED NOT NULL,"                                  +
                  "PRIMARY KEY (id),"                                                +
                  "FOREIGN KEY (query_id) REFERENCES query(id) ON DELETE CASCADE"    +
                  ")ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci"
                 )

    store.execute(
                  "CREATE TABLE tos("                                                + 
                  "id INT UNSIGNED NOT NULL AUTO_INCREMENT,"                         +
                  "query_id INT UNSIGNED NOT NULL,"                                  +
                  "tos TINYINT UNSIGNED NOT NULL,"                                   +
                  "PRIMARY KEY (id),"                                                +
                  "FOREIGN KEY (query_id) REFERENCES query(id) ON DELETE CASCADE"    +
                  ")ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci"
                 )

    store.execute(
                  "CREATE TABLE flags("                                              + 
                  "id INT UNSIGNED NOT NULL AUTO_INCREMENT,"                         +
                  "query_id INT UNSIGNED NOT NULL,"                                  +
                  "flags VARCHAR(20) NOT NULL,"                                       +
                  "PRIMARY KEY (id),"                                                +
                  "FOREIGN KEY (query_id) REFERENCES query(id) ON DELETE CASCADE"    +
                  ")ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci"
                 )

    store.execute(
                  "CREATE TABLE scale("                                              + 
                  "id INT UNSIGNED NOT NULL AUTO_INCREMENT,"                         +
                  "query_id INT UNSIGNED NOT NULL,"                                  +
                  "scale VARCHAR(1) NOT NULL,"                                       +
                  "PRIMARY KEY (id),"                                                +
                  "FOREIGN KEY (query_id) REFERENCES query(id) ON DELETE CASCADE"    +
                  ")ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci"
                 )

    store.execute(
                  "CREATE TABLE asn("                                                + 
                  "id INT UNSIGNED NOT NULL AUTO_INCREMENT,"                         +
                  "query_id INT UNSIGNED NOT NULL,"                                  +
                  "asn VARCHAR(20) NOT NULL,"                                        +
                  "PRIMARY KEY (id),"                                                +
                  "FOREIGN KEY (query_id) REFERENCES query(id) ON DELETE CASCADE"    +
                  ")ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci"
                 )

    store.execute(
                  "CREATE TABLE statistics("                                         + 
                  "id INT UNSIGNED NOT NULL AUTO_INCREMENT,"                         +
                  "alert_id INT UNSIGNED NOT NULL,"                                  +
                  "number_of_flows INT UNSIGNED NOT NULL,"                           +
                  "number_of_bytes INT UNSIGNED NOT NULL,"                           +
                  "number_of_packets INT UNSIGNED NOT NULL,"                         +
                  "PRIMARY KEY (id),"                                                +
                  "FOREIGN KEY (alert_id) REFERENCES alert(id) ON DELETE CASCADE"    +
                  ")ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci"
                 )



 
    store.execute(
                  "CREATE TABLE program("                                                 +
                  "id INT UNSIGNED NOT NULL AUTO_INCREMENT,"                         +
                  "program VARCHAR(20) COLLATE utf8_unicode_ci NOT NULL,"                 +
                  "PRIMARY KEY (id)"                                                 +
                  ")ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci"
                 )
    
    store.execute(
                  "CREATE TABLE log_user("                                          + 
                  "id INT UNSIGNED NOT NULL AUTO_INCREMENT,"                        +
                  "user VARCHAR(30) COLLATE utf8_unicode_ci NOT NULL,"              +
                  "PRIMARY KEY (id)"                                                +
                  ")ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci"
                 )

    store.execute(
                  "CREATE TABLE client("                                             + 
                  "id INT UNSIGNED NOT NULL AUTO_INCREMENT,"                         +
                  "client VARCHAR(30) NOT NULL,"                                     +
                  "PRIMARY KEY (id)"                                                +
                  ")ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;"
                 )

	
def insert_threats(store):

    #import logger
    from models import Threat
    #threat_list = ['Generic', 'Other', 'Botnet', 'Malware', 'Spam', 'Phishing', 'DNSBL', 'Worm', 'Honeypot' ]
    threat_list = ['Botnet', 'Spam']

    for name in threat_list:
        threat = Threat()
        threat.type = unicode(name)
        store.add(threat)
        store.flush()
    store.commit()
    #logger.info('Threat list is inserted into database.')
    print('Threat list is inserted into database.')


def insert_type(store):

    #import logger
    from models import Type
    type_list = ['0', '1', '0,2,1,3', '0,3', '0,2,3', '0,2,3', '0,1,3' ]

    for name in type_list:
        type = Type()
        type.type = unicode(name)
        store.add(type)
        store.flush()
    store.commit()
    #logger.info('Type list is inserted into database.')
    print('Type list is inserted into database.')


def insert_category(store):

    #import logger
    from models import Category
    category_list = ['validation', 'mandatory', 'optional' ]
    for name in category_list:
        category = Category()
        category.category = unicode(name)
        store.add(category)
        store.flush()
    store.commit()
    #logger.info('Category list is inserted into database.')
    print('Category list is inserted into database.')



def get_store(conf=None):
    '''
        Create and return a database connection if not exists yet.
    '''
    global __store
    global database 
    if not __store:
        if conf is None:
            print 'initiate the db first'
            sys.exit(1)
        else:
            try:
                db = 'mysql://' + conf.db_user  + ':' + conf.db_password + '@' + conf.db_host + '/' + conf.db_name
                #db = "mysql://test@localhost/test"
		database = create_database(db)
                __store = Store(database)
                # Check if table exists
                result = __store.execute("SELECT version FROM application")
                if result:
                    print 'connection established'
                    __store = Store(database)
                    return __store
            except MySQLException, e:
                __store = Store(database)
                if e.args[0] == 1146:
                    print 'Creating the tables'
                    initialize_db(__store)
                    insert_threats(__store)
		    insert_type(__store)
		    insert_category(__store)
		    __store.flush()
                    __store = Store(database)
                    return __store
                else:
                    print 'Another mysql error is happened'
                    print e
            except Exception, e:
                print e
                sys.exit()
    else:
        __store = Store(database)
        return __store



