''' Odoo API wrapper '''
from enum import Enum
import socket

from xmlrpc.client import ServerProxy, Fault

import config

from .errors import APIError


class Operations(Enum):
    """ Allowed API Operations """
    WRITE = 'write'
    CREATE = 'create'
    READ = 'read'
    SEARCH = 'search'
    SEARCH_COUNT = 'search_count'
    SEARCH_READ = 'search_read'
    FIELDS_GET = 'fields_get'
    UNLINK = 'unlink'


def call(model: str, operation: Operations, args: tuple,
         kwargs: dict = None) -> list:
    """
    call the api w/ model and an operation
    :param model: str
    :param operation: Operations
    :param args: a list of parameters passed by position
    :param kwargs: a dict of parameters to pass by keyword (optional)
    """
    kwargs = kwargs if kwargs else {}
    uid = kwargs.pop('uid', config.ODOO_API_UID)
    password = kwargs.pop('password', config.ODOO_API_PASSWORD)

    models = ServerProxy('{}/xmlrpc/2/object'.format(config.ODOO_BASE_URL))

    if not isinstance(operation, Operations):
        raise APIError('Invalid operation')

    try:
        return models.execute_kw(config.ODOO_DB_NAME, uid, password, model,
                                 operation.value,
                                 args,
                                 kwargs)
    except Fault as error:
        raise APIError(error.faultString)
    except socket.gaierror as error:
        raise APIError(error)


def search_read(model: str, args: tuple, kwargs: dict = None) -> list:
    """
    call the api w/ model and a "SEARCH_READ" operation
    :param model: str
    :param args: a list of parameters passed by position
    :param kwargs: a dict of parameters to pass by keyword (optional)
    """
    return call(model, Operations.SEARCH_READ, args, kwargs)


def read(model: str, args: tuple, kwargs: dict = None) -> list:
    """
    call the api w/ model and a "READ" operation
    :param model: str
    :param args: a list of parameters passed by position
    :param kwargs: a dict of parameters to pass by keyword (optional)
    """
    return call(model, Operations.READ, args, kwargs)


def write(model: str, args: tuple, kwargs: dict = None) -> list:
    """
    call the api w/ model and a "WRITE" operation
    :param model: str
    :param args: a list of parameters passed by position
    :param kwargs: a dict of parameters to pass by keyword (optional)
    """
    return call(model, Operations.WRITE, args, kwargs)


def create(model: str, args: tuple, kwargs: dict = None) -> list:
    """
    call the api w/ model and a "CREATE" operation
    :param model: str
    :param args: a list of parameters passed by position
    :param kwargs: a dict of parameters to pass by keyword (optional)
    """
    return call(model, Operations.CREATE, args, kwargs)


def search(model: str, args: tuple, kwargs: dict = None) -> list:
    """
    call the api w/ model and a "SEARCH" operation
    :param model: str
    :param args: a list of parameters passed by position
    :param kwargs: a dict of parameters to pass by keyword (optional)
    """
    return call(model, Operations.SEARCH, args, kwargs)


def search_count(model: str, args: tuple, kwargs: dict = None) -> list:
    """
    call the api w/ model and a "SEARCH_COUNT" operation
    :param model: str
    :param args: a list of parameters passed by position
    :param kwargs: a dict of parameters to pass by keyword (optional)
    """
    return call(model, Operations.SEARCH_COUNT, args, kwargs)


def fields_get(model: str, args: tuple, kwargs: dict = None) -> list:
    """
    call the api w/ model and a "FIELDS_GET" operation
    :param model: str
    :param args: a list of parameters passed by position
    :param kwargs: a dict of parameters to pass by keyword (optional)
    """
    return call(model, Operations.FIELDS_GET, args, kwargs)


def unlink(model: str, args: tuple, kwargs: dict = None) -> list:
    """
    call the api w/ model and a "FIELDS_GET" operation
    :param model: str
    :param args: a list of parameters passed by position
    :param kwargs: a dict of parameters to pass by keyword (optional)
    """
    return call(model, Operations.FIELDS_GET, args, kwargs)
