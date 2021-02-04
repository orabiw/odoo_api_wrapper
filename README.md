# Odoo API Wrapper

A wrapper for [Odoo](https://www.odoo.com/)'s API.

You can check out Odoo's API documentation on
[link](https://www.odoo.com/documentation/13.0/webservices/odoo.html).


## Usage

```
from odoo_api_wrapper.api import read

read('res.partner', [1211], {'fields': ['name', 'country_id', 'comment']})
```
