#!/usr/local/bin/python

from storm.locals import In
import logging
import sys

import db
import logger
from models import Source, List, Query, Subscription, SubscriptionPackets

__all__ = ['SubscriptionGenerator']
 

class SubscriptionGenerator:
    
    def __init__(self):
        self.slogger = logger.createLogger('subscriptiongenerator')
        self.store = db.get_store()

    def createSubscriptionTypes(self):
        self.slogger.debug('In %s' % sys._getframe().f_code.co_name)
        '''
            We have 2 different subscription types.
            
            1) Source -> example : "Amada,Malc0de,DFN-Honeypot,ABC-NREN_Special_Source"
            2) List Type -> example : "Botnet,Malware,Honeypot Output, Special Source Output"
            
            These subscription types are inserted into subscription table
            according to the condition of "if that subscription type have queries" 
            in query table. "createSubscriptions" function fills the subscription 
            table by inserting these subscription types. 
    
    		!!!!!! SUBSCRIPTION_TAGS NE OLACAK !!!!!!!!
    
        '''
    
        # 1) Source Name
        subscription_type=1
        source_name_list = self.store.find(Source.source_name)
        source_name_list.group_by(Source.source_name)
        for source_name in source_name_list:
            subscription = self.store.find(Subscription.subscription_id, Subscription.subscription_name == '%s' % (source_name))
            if subscription.count < 1:
                subscription = Subscription()
                subscription.subscription_type = subscription_type
                subscription.subscription_name = source_name
                self.store.add(subscription)
    
        # 2) List Type
        subscription_type=2
        list_type_list = self.store.find(List.list_type)
        list_type_list.group_by(List.list_type)
        for list_type in list_type_list:
            subscription = self.store.find(Subscription.subscription_id, Subscription.subscription_name == '%s' % (list_type))
            if subscription.count < 1:
                subscription = Subscription()
                subscription.subscription_type = subscription_type
                subscription.subscription_name = list_type
                self.store.add(subscription)
    
        self.store.commit()
        self.slogger.debug('Subscription types are created')
    
    
    def createSubscriptions(self):
        self.slogger.debug('In %s' % sys._getframe().f_code.co_name)
        self.slogger.info('Generating Subscriptions...')
        self.createSourceSubscriptionPackets()
        self.createListSubscriptionPackets()
    
    
    
    def createSourceSubscriptionPackets(self):
        self.slogger.debug('In %s' % sys._getframe().f_code.co_name)
        self.store = db.get_store()
    
        # Check if source_name is not given, means we work for all sources.
        source_name_list = self.store.find(Subscription.subscription_name, Subscription.subscription_type == 1)
        if source_name_list is None:
            self.slogger.error("Source is not registered to database. Run 'reconfig sources' or check sources.")
            sys.exit()
        self.slogger.debug(source_name_list)
        for source_name in source_name_list:
            source_id = self.store.find(Source.source_id, Source.source_name == '%s' % unicode(source_name)).one()
            query_id_list = self.store.find(Query.query_id, Query.source_id == source_id)
            if query_id_list is None:
                self.slogger.warning("We don't have any query for this source.")
                self.slogger.warning("%s subscription creation is failed." % (source_name) )
                continue
            subscription_id = self.store.find(Subscription.subscription_id, Subscription.subscription_name == '%s' % unicode(source_name)).one()
            subs_packet_id = self.store.find(SubscriptionPackets.subs_packet_id, SubscriptionPackets.subscription_id == subscription_id).one()
            if subs_packet_id is None:
                for qid in query_id_list:
                    spacket = SubscriptionPackets()
                    spacket.subscription_id = subscription_id
                    spacket.query_id = qid
                    self.store.add(spacket)
            else:
                query_ids = self.store.find(SubscriptionPackets.query_id, SubscriptionPackets.subscription_id == subscription_id)
                for qid in query_id_list:
                    if not (qid in query_ids):
                        spacket = SubscriptionPackets(subscription_id, qid)
                        self.store.add(spacket)
        self.store.commit()
    
    
    def createListSubscriptionPackets(self):
        self.slogger.debug('In %s' % sys._getframe().f_code.co_name)
        list_type_list = self.store.find(Subscription.subscription_name, Subscription.subscription_type == 2)
        if list_type_list is None:
            self.slogger.error("List type is not registered to subscriptions. Run reconfig or check sources.")
            sys.exit()
        self.slogger.debug(list_type_list)
        for list_type in list_type_list:
            list_id = self.store.find(List.list_id, List.list_type == '%s' % unicode(list_type)).one()
            source_id = self.store.find(Source.source_id, Source.list_id == list_id)
            if source_id.count() < 1:
                continue
            query_id_list = self.store.find(Query.query_id, In(Query.source_id, list(source_id)))
            if query_id_list.count() > 1:
                subscription_id = self.store.find(Subscription.subscription_id, Subscription.subscription_name == '%s' % unicode(list_type)).one()
                subs_packet_id = self.store.find(SubscriptionPackets.subs_packet_id, SubscriptionPackets.subscription_id == subscription_id)
                if subs_packet_id.count() < 1 :
                    for qid in query_id_list:
                        spacket = SubscriptionPackets()
                        spacket.subscription_id = subscription_id
                        spacket.query_id = qid
                        self.store.add(spacket)
                else:
                    query_ids = self.store.find(SubscriptionPackets.query_id, SubscriptionPackets.subscription_id == subscription_id)
                    for qid in query_id_list:
                        if not (qid in query_ids):
                            spacket = SubscriptionPackets()
                            spacket.subscription_id = subscription_id
                            spacket.query_id = qid
                            self.store.add(spacket)
            else:
                self.slogger.debug("We don't have any query for this list type.")
                self.slogger.debug("%s subscription is not created." % (list_type))
        self.store.commit()
    
    
    def fetchSubscriptionPackets(self):
        subscription_list = self.store.find(Subscription.subscription_name)
        return list(subscription_list)
    
