""" `odoo_api_wrapper.api.Api` tests """
import socket
from unittest import mock
import xmlrpc.client

import pytest
import odoo_api_wrapper


def test_api_init(init_params):
    """test initializing an api"""
    assert odoo_api_wrapper.Api(*init_params)


def test_api_search(mock_server, init_params, random_string):
    """test api.search"""
    del mock_server

    api = odoo_api_wrapper.Api(*init_params)
    assert api.search(random_string())


def test_api_search_read(mock_server, init_params, random_string):
    """test api.search_read"""
    del mock_server

    api = odoo_api_wrapper.Api(*init_params)
    assert api.search_read(random_string())


def test_api_read(mock_server, init_params, random_string):
    """test api.read"""
    del mock_server

    api = odoo_api_wrapper.Api(*init_params)
    assert api.read(random_string())


def test_api_write(mock_server, init_params, random_string):
    """test api.write"""
    del mock_server

    api = odoo_api_wrapper.Api(*init_params)
    assert api.write(random_string())


def test_api_create(mock_server, init_params, random_string):
    """test api.create"""
    del mock_server

    api = odoo_api_wrapper.Api(*init_params)
    assert api.create(random_string())


def test_api_fields_get(mock_server, init_params, random_string):
    """test api.fields_get"""
    del mock_server

    api = odoo_api_wrapper.Api(*init_params)
    assert api.fields_get(random_string())


def test_api_search_count(mock_server, init_params, random_string):
    """test api.search_count"""
    del mock_server

    api = odoo_api_wrapper.Api(*init_params)
    assert api.search_count(random_string())


def test_api_unlink(mock_server, init_params, random_string):
    """test api.unlink"""
    del mock_server

    api = odoo_api_wrapper.Api(*init_params)
    assert api.unlink(random_string())


def test_invalid_operation(mock_server, init_params, random_string):
    """test with an invalid operation"""
    del mock_server

    api = odoo_api_wrapper.Api(*init_params)

    with pytest.raises(odoo_api_wrapper.api.APIError):
        api.call(random_string(), random_string())


def test_xml_rpc_fault(init_params, random_string):
    """test that raises `xmlrpc.client.Fault`"""
    api = odoo_api_wrapper.Api(*init_params)

    with mock.patch.object(api, "server") as mock_server:
        mock_server.execute_kw.side_effect = xmlrpc.client.Fault(
            random_string(),
            random_string(),
        )

        with pytest.raises(odoo_api_wrapper.api.APIError):
            api.search(random_string(), random_string())


def test_socket_gaierror(init_params, random_string):
    """test that raises `socket.gaierror`"""
    api = odoo_api_wrapper.Api(*init_params)

    with mock.patch.object(api, "server") as mock_server:
        mock_server.execute_kw.side_effect = socket.gaierror(
            random_string(),
            random_string(),
        )

        with pytest.raises(odoo_api_wrapper.api.APIError):
            api.search(random_string(), random_string())


def test_error_description(init_params, random_string):
    """test that raises `socket.gaierror`"""
    api = odoo_api_wrapper.Api(*init_params)

    with mock.patch.object(api, "server") as mock_server:
        error_no = random_string()
        error_string = random_string()

        mock_server.execute_kw.side_effect = socket.gaierror(
            error_no,
            error_string,
        )

        try:
            api.search(random_string(), random_string())
        except odoo_api_wrapper.APIError as error:
            assert str(error) == f"[Errno {error_no}] {error_string}"
