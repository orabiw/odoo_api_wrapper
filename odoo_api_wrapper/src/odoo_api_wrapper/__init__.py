""" A wrapper for Odoo's xml-rpc api, provides a simple wrapper class to access common
operations.

## Example Usage

```python
import odoo_api_wrapper

api = odoo_api_wrapper.Api("http://localhost:8069", "db", "1001", "password")
api.search("somemodel", "something")
```

"""
from odoo_api_wrapper.api import Api
