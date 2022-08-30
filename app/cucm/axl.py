"""axl.py

Provides AXL interface to CUCM cluster

===

Version 1.0
Initial release

===

This script requires that `zeep and Flask` be installed within the Python environment you are running this script

This file can be imported as a module and contains the following function(s):

    * execute_sql_query - Runs executeSQLQuery against AXL interface
    * list_phone - Run listPhone against AXL interface
"""
from requests.exceptions import ConnectionError
from zeep.exceptions import Fault
from app.cucm.soap import Soap

import logging
import sys


def get_history():

    print(Soap().show_history())


def execute_sql_query(query):
    """
    Runs executeSQLQuery against AXL interface
    :param query: SQL query to be executed
    :return: executeSQLQueryResponse
    """

    try:
        logging.info(query)

        resp = Soap().get_service().executeSQLQuery(sql=query)

        return resp

    except Fault as error:
        Soap().show_history()
        logging.error('executeSQLQuery Fault: Credentials? {}'.format(error))
        raise

    except ConnectionError as error:
        logging.error('Unable to reach CUCM: {}'.format(error))
        raise

    except:
        logging.error('Unexpected error: {}'.format(sys.exc_info()[0]))
        raise


def list_phone(query):
    """
    Runs listPhone against AXL interface

    Note: This was implemented before care was taken and it may be missing somethings
    :param query: Name of device to get information about
    :return:
        Returns the name and description of the resulting phone
    """

    try:
        logging.info(query)

        resp = Soap().get_service().listPhone(searchCriteria={'name': query},
                                              returnedTags={'name': '',
                                                            'description': ''})

        logging.info(resp)

    except Fault as error:
        Soap().show_history()
        logging.error('listPhone Fault: Credentials? {}'.format(error))
        raise

    except ConnectionError as error:
        logging.error('Unable to reach CUCM: {}'.format(error))
        raise

    except:
        logging.error('Unexpected error: {}'.format(sys.exc_info()[0]))
        raise