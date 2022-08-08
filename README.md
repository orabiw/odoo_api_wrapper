# Odoo API Wrapper

A wrapper for [Odoo](https://www.odoo.com/)'s API.

You can check out Odoo's API documentation on
[link](https://www.odoo.com/documentation/13.0/webservices/odoo.html).


## Usage

```python
import odoo_api_wrapper

api = odoo_api_wrapper.Api("http://localhost:8069", "db", "1001", "password")
api.search('res.partner', [[['is_company', '=', True]]])
```
