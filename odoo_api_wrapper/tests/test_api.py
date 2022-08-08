""" `odoo_api_wrapper.api.Api` tests """
# pylint:disable=too-many-arguments
import socket
from unittest import mock
import xmlrpc.client

import pytest
import odoo_api_wrapper


def test_api_init(init_params):
    """test initializing an api"""
    assert odoo_api_wrapper.Api(*init_params)


def test_api_search(mock_server, init_params, model, args, kwargs):
    """test api.search"""
    del mock_server

    api = odoo_api_wrapper.Api(*init_params)

    assert api.search(model, args, kwargs)
    api.server.execute_kw.assert_called_with(
        *init_params[1:], model, "search", args, kwargs
    )


def test_api_search_read(mock_server, init_params, model, args, kwargs):
    """test api.search_read"""
    del mock_server

    api = odoo_api_wrapper.Api(*init_params)

    assert api.search_read(model, args, kwargs)
    api.server.execute_kw.assert_called_with(
        *init_params[1:], model, "search_read", args, kwargs
    )


def test_api_read(mock_server, init_params, model, args, kwargs):
    """test api.read"""
    del mock_server

    api = odoo_api_wrapper.Api(*init_params)

    assert api.read(model, args, kwargs)
    api.server.execute_kw.assert_called_with(
        *init_params[1:], model, "read", args, kwargs
    )


def test_api_write(mock_server, init_params, model, args, kwargs):
    """test api.write"""
    del mock_server

    api = odoo_api_wrapper.Api(*init_params)

    assert api.write(model, args, kwargs)
    api.server.execute_kw.assert_called_with(
        *init_params[1:], model, "write", args, kwargs
    )


def test_api_create(mock_server, init_params, model, args, kwargs):
    """test api.create"""
    del mock_server

    api = odoo_api_wrapper.Api(*init_params)

    assert api.create(model, args, kwargs)
    api.server.execute_kw.assert_called_with(
        *init_params[1:], model, "create", args, kwargs
    )


def test_api_fields_get(mock_server, init_params, model, args, kwargs):
    """test api.fields_get"""
    del mock_server

    api = odoo_api_wrapper.Api(*init_params)

    assert api.fields_get(model, args, kwargs)
    api.server.execute_kw.assert_called_with(
        *init_params[1:], model, "fields_get", args, kwargs
    )


def test_api_search_count(mock_server, init_params, model, args):
    """test api.search_count"""
    del mock_server

    api = odoo_api_wrapper.Api(*init_params)

    assert api.search_count(model, args)
    api.server.execute_kw.assert_called_with(
        *init_params[1:], model, "search_count", args, {}
    )


def test_api_unlink(mock_server, init_params, model, args, kwargs):
    """test api.unlink"""
    del mock_server

    api = odoo_api_wrapper.Api(*init_params)

    assert api.unlink(model, args, kwargs)
    api.server.execute_kw.assert_called_with(
        *init_params[1:], model, "unlink", args, kwargs
    )


def test_invalid_operation(
    mock_server, init_params, random_string, model, args, kwargs
):
    """test with an invalid operation"""
    del mock_server

    api = odoo_api_wrapper.Api(*init_params)

    with pytest.raises(odoo_api_wrapper.api.APIError):
        api.call(model, random_string(), args, kwargs)


def test_xml_rpc_fault(init_params, random_string, model, args, kwargs):
    """test that raises `xmlrpc.client.Fault`"""
    api = odoo_api_wrapper.Api(*init_params)

    with mock.patch.object(api, "server") as mock_server:
        mock_server.execute_kw.side_effect = xmlrpc.client.Fault(
            random_string(),
            random_string(),
        )

        with pytest.raises(odoo_api_wrapper.api.APIError):
            api.search(model, args, kwargs)


def test_socket_gaierror(init_params, random_string, model, args, kwargs):
    """test that raises `socket.gaierror`"""
    api = odoo_api_wrapper.Api(*init_params)

    with mock.patch.object(api, "server") as mock_server:
        mock_server.execute_kw.side_effect = socket.gaierror(
            random_string(),
            random_string(),
        )

        with pytest.raises(odoo_api_wrapper.api.APIError):
            api.search(model, args, kwargs)


def test_error_description(init_params, random_string, model, args, kwargs):
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
            api.search(model, args, kwargs)
        except odoo_api_wrapper.APIError as error:
            assert str(error) == f"[Errno {error_no}] {error_string}"
