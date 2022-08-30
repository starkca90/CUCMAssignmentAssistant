"""helper.py

Provides helper functions to CUCM AXL interface

===

Version 1.0
Initial release

Version 1.1
Added get unassigned devices to get any SEP, BOT, TAB, TCT or CSF devices that does not have a owner set

===

This script requires that `Flask` be installed within the Python environment you are running this script

This file can be imported as a module and contains the following function(s):

    * get_device_enums - Queries CUCM for the enum of a device
    * find_users_with_devices - Queries CUCM for a list of users with a specified device enum
"""

from app.cucm import axl
import re
import logging


def __get_device_enum(name: str):
    """
    Formats a SQL query to get the enum of the specified device

    Query is tested in a LIKE search and surrounded by '%'s
    :param name: Plain text name of device
    :return: list of enums that match the device name query
    """

    sql_resp = axl.execute_sql_query("SELECT enum, name from typemodel WHERE name LIKE '{}'".format(name))

    enums = []

    if sql_resp:
        for i in range(len(sql_resp['return']['row'])):
            enums.append(sql_resp['return']['row'][i][0].text)
    else:
        logging.error('Query Failed')

    logging.info(enums)

    return enums


def get_device_enums(devices: str):
    """
    Splits comma separated list of devices and queries CUCM for their equivalent enums
    :param devices: Comma separated list of devices to get enums for
    :return: list of matching enums
    """
    pattern = re.compile("^\s+|\s*,\s*|\s+$")

    device_list = [x for x in pattern.split(devices) if x]

    enums = []

    for i in range(len(device_list)):
        temp_enums = __get_device_enum(device_list[i])

        for j in range(len(temp_enums)):
            enums.append(temp_enums[j])

    return enums


def get_unassigned_devices():
    """
    Retrieves list of devices that do not have an Owner set
    :return: list of devices that do not have an owner set
    """
    query = "SELECT name, description, fkenduser FROM device WHERE fkenduser is null AND (name like \"SEP%\" OR name like \"BOT%\" OR name like \"TAB%\" OR name like \"TCT%\" OR name like \"CSF%\")"

    sql_resp = axl.execute_sql_query(query)

    return sql_resp

 


def find_users_with_devices(devices: list):
    """
    Queries CUCM for users with matching devices and returns their mailID
    :param devices: List of enums to query users
    :return: List of mailIDs that has the specified device(s)
    """
    search_string = ''

    for i in range(len(devices)):
        search_string = search_string + "'" + devices[i] + "'"

        if i != (len(devices) - 1):
            search_string = search_string + ","

    query = "SELECT enduser.mailid FROM enduser JOIN (SELECT count(*) as numdevices,fkenduser,tkmodel FROM device GROUP BY device.fkenduser,device.tkmodel) as dev ON dev.fkenduser = enduser.pkid WHERE dev.tkmodel IN ({})".format(search_string)

    sql_resp = axl.execute_sql_query(query)

    users = []

    if sql_resp:
        if sql_resp['return']:
            for i in range(len(sql_resp['return']['row'])):
                users.append(sql_resp['return']['row'][i][0].text)
    else:
        logging.error('Query Failed')

    return users