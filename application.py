from config import Config
import os
import logging

from app.cucm import helper as cucm_helper

logging.error(os.environ["REQUESTS_CA_BUNDLE"])

logging.info(cucm_helper.get_unassigned_devices())