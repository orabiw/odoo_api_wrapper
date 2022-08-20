""" test configutation """
# pylint:disable=redefined-outer-name
import random
import string
from unittest import mock

import pytest


@pytest.fixture
def random_string():
    """random string generator"""

    def _wrapped(length: int = 8):
        return "".join(random.choices(string.ascii_lowercase, k=length))

    return _wrapped


@pytest.fixture
def init_params(random_string):
    """init params"""
    return (
        f"http://{random_string()}.com:8069",
        random_string(),
        random_string(),
        random_string(),
    )


@pytest.fixture
def mock_server():
    """patch `xmlrpc.client`"""
    with mock.patch("odoo_api_wrapper.api.xmlrpc.client"):
        yield


@pytest.fixture
def model_name(random_string):
    """model_name fixture"""
    return random_string()


@pytest.fixture
def args(random_string):
    """args for methods fixture"""
    operators = [
        "=",
        "!=",
        ">",
        ">=",
        "<",
        "<=",
        "=?",
        "=like",
        "like",
        "not like",
        "ilike",
        "not ilike",
        "=ilike",
        "in",
        "not in",
        "child_of",
        "parent_of",
    ]

    operator = random.choice(operators)
    return [[random_string(), operator, random_string()]]


@pytest.fixture
def kwargs(random_string):
    """args for methods fixture"""
    return {random_string(): random_string()}
