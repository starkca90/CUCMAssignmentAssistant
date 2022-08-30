"""mongodbclient.py

Initializes AXL interface to CUCM environment.

Requires the following environment variables to be defined:

CUCM_VERSION
CUCM_PUBLISHER
CUCM_USERNAME
CUCM_PASSWORD

The schema directory from the axlsqltoolkit package must be in the same directory as this file
    The version directory specified in the CUCM_VERSION variable must be present in the schema directory

===

Version 1.0
Initial release

===

This script requires that `zeep, lxml and Flask` be installed within the Python environment you are running this script

This file can be imported as a module and contains the following class(es):
logging
    * Soap - Provides Soap interface to CUCM cluster
"""

from zeep import Client
from zeep.cache import SqliteCache
from zeep.transports import Transport
from zeep.plugins import HistoryPlugin
from requests.auth import HTTPBasicAuth
from lxml import etree
import os
import sys
import logging

from app import session


class Soap:

    class __Soap:

        def __init__(self):
            try:
                basedir = os.path.abspath(os.path.dirname(__file__))

                __wsdl = 'file://{}/schema/{}/AXLAPI.wsdl'.format(basedir, os.environ['CUCM_VERSION'])
                __location = 'https://{}:8443/axl/'.format(os.environ['CUCM_PUBLISHER'])
                __binding = "{http://www.cisco.com/AXLAPIService/}AXLAPIBinding"

                session.auth = HTTPBasicAuth(os.environ['CUCM_USERNAME'], os.environ['CUCM_PASSWORD'])
                __transport = Transport(cache=SqliteCache(), session=session, timeout=20)
                self.__history = HistoryPlugin()
                __client = Client(wsdl=__wsdl, transport=__transport, plugins=[self.__history])
                self.__service = __client.create_service(__binding, __location)

            except:
                logging.error('Unexpected error: {}'.format(sys.exc_info()[0]))
                raise

        def show_history(self):
            for item in [self.__history.last_sent, self.__history.last_received]:
                logging.info(etree.tostring(item["envelope"], encoding="unicode", pretty_print=True))

        def get_service(self):
            return self.__service

        def get_history(self):
            return self.__history

    singleton = None

    def __new__(cls):
        if not Soap.singleton:
            Soap.singleton = Soap.__Soap()

        return Soap.singleton