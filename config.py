"""config.py

Provides wrapper for gathering config parameters from several sources

Sources include:
    - .env file created in project's root (Recommended for development machines)
    - System environments (Recommended for production environments)
    - Fall back hard-codded strings (Not recommended)

===

Version 1.0
Initial release

===

This script requires that `python-dotenv==0.13.0` be installed within the Python environment you are running this script

This file can be imported as a module and contains the following class(es):

    * Config - Provides access to required configuration variables
"""

import os
from dotenv import load_dotenv

basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, '.env'))


class Config(object):
    """
    Configuration parameters for the application

    Attributes
    ----------
    CUCM_PUBLISHER : str
        FQDN of CUCM Publisher

    CUCM_VERSION : str
        CUCM version when application uses AXL queries

    CUCM_USERNAME : str
        CUCM username to use when application does not use user provided credentials

    CUCM_PASSWORD : str
        CUCM password to use when application does not use user provided credentials
    """
    CUCM_PUBLISHER = os.environ.get('CUCM_PUBLISHER') or 'cucm01.contoso.com'
    CUCM_VERSION = os.environ.get('CUCM_VERSION') or '12.5'
    CUCM_USERNAME = os.environ.get('CUCM_USERNAME') or ''
    CUCM_PASSWORD = os.environ.get('CUCM_PASSWORD') or ''