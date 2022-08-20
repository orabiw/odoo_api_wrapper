""" model_name tests """
# pylint:disable=redefined-outer-name
import pytest
import odoo_api_wrapper


@pytest.fixture
def api(mock_server, init_params):
    """create an api instance"""
    del mock_server
    return odoo_api_wrapper.Api(*init_params)


@pytest.fixture
def model(api, model_name):
    """model fixture"""
    return odoo_api_wrapper.Model(api, model_name)


def test_model_search(init_params, api, model, model_name):
    """test model.search"""
    args = [[["is_company", "=", True]]]

    assert model.search(args)
    api.server.execute_kw.assert_called_with(
        *init_params[1:], model_name, "search", args, {}
    )


def test_model_search_read(init_params, api, model, model_name):
    """test model.search_read"""
    args = [[["is_company", "=", True]]]
    kwargs = {"fields": ["name", "country_id", "comment"], "limit": 5}

    assert model.search_read(args, kwargs)
    api.server.execute_kw.assert_called_with(
        *init_params[1:], model_name, "search_read", args, kwargs
    )


def test_model_read(init_params, api, model, model_name):
    """test model.read"""
    args = [[["is_company", "=", True]]]
    kwargs = {"limit": 1}

    assert model.read(args, kwargs)
    api.server.execute_kw.assert_called_with(
        *init_params[1:], model_name, "read", args, kwargs
    )


def test_model_write(init_params, api, model, model_name):
    """test model.write"""
    args = [[1], {"name": "Newer partner"}]

    assert model.write(args)
    api.server.execute_kw.assert_called_with(
        *init_params[1:], model_name, "write", args, {}
    )


def test_model_create(init_params, api, model, model_name):
    """test model.create"""
    args = [{"name": "New Partner"}]

    assert model.create(args)
    api.server.execute_kw.assert_called_with(
        *init_params[1:], model_name, "create", args, {}
    )


def test_model_fields_get(init_params, api, model, model_name):
    """test model.fields_get"""

    args = []
    kwargs = {"attributes": ["string", "help", "type"]}

    assert model.fields_get(args, kwargs)
    api.server.execute_kw.assert_called_with(
        *init_params[1:], model_name, "fields_get", args, kwargs
    )


def test_model_search_count(init_params, api, model, model_name):
    """test model.search_count"""
    args = [[["is_company", "=", True]]]

    assert model.search_count(args)
    api.server.execute_kw.assert_called_with(
        *init_params[1:], model_name, "search_count", args, {}
    )


def test_model_unlink(init_params, api, model, model_name):
    """test model.unlink"""
    args = [[1]]

    assert model.unlink(args)
    api.server.execute_kw.assert_called_with(
        *init_params[1:], model_name, "unlink", args, {}
    )
