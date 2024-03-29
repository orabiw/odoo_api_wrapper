""" `odoo_api_wrapper.api.Api` tests """
# pylint:disable=too-many-arguments
import socket
import xmlrpc.client
from unittest import mock

import pytest

import odoo_api_wrapper


def test_api_init(init_params):
    """test initializing an api"""
    assert odoo_api_wrapper.Api(*init_params)


def test_api_search(mock_server, init_params, model_name):
    """test api.search"""
    del mock_server

    api = odoo_api_wrapper.Api(*init_params)

    args = [[["is_company", "=", True]]]
    kwargs = {}

    assert api.search(model_name, args, kwargs)
    api.server.execute_kw.assert_called_with(
        *init_params[1:], model_name, "search", args, kwargs
    )


def test_api_search_read(mock_server, init_params, model_name):
    """test api.search_read"""
    del mock_server

    api = odoo_api_wrapper.Api(*init_params)

    args = [[["is_company", "=", True]]]
    kwargs = {"fields": ["name", "country_id", "comment"], "limit": 5}

    assert api.search_read(model_name, args, kwargs)
    api.server.execute_kw.assert_called_with(
        *init_params[1:], model_name, "search_read", args, kwargs
    )


def test_api_read(mock_server, init_params, model_name):
    """test api.read"""
    del mock_server

    api = odoo_api_wrapper.Api(*init_params)

    args = [[["is_company", "=", True]]]
    kwargs = {"limit": 1}

    assert api.read(model_name, args, kwargs)
    api.server.execute_kw.assert_called_with(
        *init_params[1:], model_name, "read", args, kwargs
    )


def test_api_write(mock_server, init_params, model_name):
    """test api.write"""
    del mock_server

    api = odoo_api_wrapper.Api(*init_params)

    args = [[1], {"name": "Newer partner"}]
    kwargs = {}

    assert api.write(model_name, args, kwargs)
    api.server.execute_kw.assert_called_with(
        *init_params[1:], model_name, "write", args, kwargs
    )


def test_api_create(mock_server, init_params, model_name):
    """test api.create"""
    del mock_server

    api = odoo_api_wrapper.Api(*init_params)

    args = [{"name": "New Partner"}]
    kwargs = {}

    assert api.create(model_name, args, kwargs)
    api.server.execute_kw.assert_called_with(
        *init_params[1:], model_name, "create", args, kwargs
    )


def test_api_fields_get(mock_server, init_params, model_name):
    """test api.fields_get"""
    del mock_server

    api = odoo_api_wrapper.Api(*init_params)

    args = []
    kwargs = {"attributes": ["string", "help", "type"]}

    assert api.fields_get(model_name, args, kwargs)
    api.server.execute_kw.assert_called_with(
        *init_params[1:], model_name, "fields_get", args, kwargs
    )


def test_api_search_count(mock_server, init_params, model_name):
    """test api.search_count"""
    del mock_server

    api = odoo_api_wrapper.Api(*init_params)

    args = [[["is_company", "=", True]]]

    assert api.search_count(model_name, args)
    api.server.execute_kw.assert_called_with(
        *init_params[1:], model_name, "search_count", args, {}
    )


def test_api_unlink(mock_server, init_params, model_name):
    """test api.unlink"""
    del mock_server

    api = odoo_api_wrapper.Api(*init_params)

    args = [[1]]
    kwargs = {}

    assert api.unlink(model_name, args, kwargs)

    api.server.execute_kw.assert_called_with(
        *init_params[1:], model_name, "unlink", args, kwargs
    )


def test_invalid_operation(
    mock_server, init_params, random_string, model_name, args, kwargs
):
    """test with an invalid operation"""
    del mock_server

    api = odoo_api_wrapper.Api(*init_params)

    with pytest.raises(odoo_api_wrapper.api.APIError):
        api.call(model_name, random_string(), args, kwargs)


def test_xml_rpc_fault(init_params, random_string, model_name, args, kwargs):
    """test that raises `xmlrpc.client.Fault`"""
    api = odoo_api_wrapper.Api(*init_params)

    with mock.patch.object(api, "server") as mock_server:
        mock_server.execute_kw.side_effect = xmlrpc.client.Fault(
            random_string(),
            random_string(),
        )

        with pytest.raises(odoo_api_wrapper.api.APIError):
            api.search(model_name, args, kwargs)


def test_socket_gaierror(init_params, random_string, model_name, args, kwargs):
    """test that raises `socket.gaierror`"""
    api = odoo_api_wrapper.Api(*init_params)

    with mock.patch.object(api, "server") as mock_server:
        mock_server.execute_kw.side_effect = socket.gaierror(
            random_string(),
            random_string(),
        )

        with pytest.raises(odoo_api_wrapper.api.APIError):
            api.search(model_name, args, kwargs)


def test_error_description(init_params, random_string, model_name, args, kwargs):
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
            api.search(model_name, args, kwargs)
        except odoo_api_wrapper.APIError as error:
            assert str(error) == f"[Errno {error_no}] {error_string}"
