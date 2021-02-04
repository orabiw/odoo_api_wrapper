""" config values """
import os

LOG_LEVEL = os.getenv('LOG_LEVEL', 'ERROR')
ODOO_DB_NAME = os.getenv('ODOO_DB_NAME')
ODOO_API_PASSWORD = os.getenv('ODOO_API_PASSWORD')
ODOO_BASE_URL = os.getenv('ODOO_BASE_URL')
ODOO_API_UID = int(os.getenv('ODOO_API_UID'))
