""" Odoo API wrapper

A wrapper for [Odoo](https://www.odoo.com/)'s External API.

You can check out the official documentation
[here](https://www.odoo.com/documentation/master/developer/api/external_api.html).

`odoo_api_wrapper.api.Api` is the main class, `odoo_api_wrapper.api.Operations` defines
the operations used for `odoo_api_wrapper.api.Api.call`, raises
`odoo_api_wrapper.api.APIError`.

## Usage Examples

### Instantiate an `Api`
Create an instance of the API to start using it.
```python
import odoo_api_wrapper

api = odoo_api_wrapper.Api("http://localhost:8069", "db", "1001", "password")
```

### List records
Records can be listed and filtered via `search()`.
```python
api.search('res.partner', [[['is_company', '=', True]]])
```

### Count records
Rather than retrieve a possibly gigantic list of records and count them,
`search_count()` can be used to retrieve only the number of records matching the query.
It takes the same domain filter as `search()` and no other parameter.
```python
api.search_count('res.partner', [[['is_company', '=', True]]])
```

### Read records
Record data are accessible via the `read()` method, which takes a list of ids (as
returned by `search()`), and optionally a list of fields to fetch. By default, it
fetches all the fields the current user can read, which tends to be a huge amount.
```python
ids = api.search('res.partner', [[['is_company', '=', True]]], {'limit': 1})
[record] = api.read('res.partner', [ids])
# count the number of fields fetched by default
len(record)
```

### List record fields
`fields_get()` can be used to inspect a model’s fields and check which ones seem to be
of interest.
```python
api.fields_get('res.partner', [], {'attributes': ['string', 'help', 'type']})
```

### Search and read
Because it is a very common task, Odoo provides a `search_read()` shortcut which, as
its name suggests, is equivalent to a `search()` followed by a `read()`, but avoids
having to perform two requests and keep ids around.
```python
api.search_read(
    'res.partner',
    [[['is_company', '=', True]]],
    {'fields': ['name', 'country_id', 'comment'], 'limit': 5},
)
```

### Create records
Records of a model are created using `create()`. The method creates a single record and
returns its database identifier.
```python
id = api.create('res.partner', [{'name': "New Partner"}])
```

### Update records
Records can be updated using `write()`. It takes a list of records to update and a
mapping of updated fields to values similar to `create()`.
```python
api.write('res.partner', [[id], {'name': "Newer partner"}])
```

### Delete records
Records can be deleted in bulk by providing their ids to `unlink()`.
```python
api.unlink('res.partner', [[id]])
```

"""
import enum
import functools
import socket
import xmlrpc.client
from typing import Any, Callable, Dict, List


class Operations(enum.Enum):
    """Allowed API Operations"""

    WRITE = "write"
    CREATE = "create"
    READ = "read"
    SEARCH = "search"
    SEARCH_COUNT = "search_count"
    SEARCH_READ = "search_read"
    FIELDS_GET = "fields_get"
    UNLINK = "unlink"


class APIError(Exception):
    """API Error Base Class"""

    def __init__(self, description: str, *args: Any, **kwargs: Any):
        super().__init__(*args, **kwargs)
        self.description = description

    def __str__(self) -> str:
        return self.description


class Api:  # pylint:disable=too-few-public-methods
    """API Wrapper"""

    # define the methods we'll add dynamically
    write: Callable[[str, List, Dict[str, Any]], Any]
    create: Callable[[str, List, Dict[str, Any]], Any]
    read: Callable[[str, List, Dict[str, Any]], Any]
    search: Callable[[str, List, Dict[str, Any]], Any]
    search_count: Callable[[str, List, Dict[str, Any]], Any]
    search_read: Callable[[str, List, Dict[str, Any]], Any]
    fields_get: Callable[[str, List, Dict[str, Any]], Any]
    unlink: Callable[[str, List, Dict[str, Any]], Any]

    def __new__(cls, *args, **kwargs):  # pylint:disable=unused-argument
        instance = super().__new__(cls)

        # add the dynamic method
        for operation in Operations.__members__.values():
            setattr(
                instance,
                operation.value,
                functools.partial(instance.call, operation),
            )

        return instance

    def __init__(self, base_url: str, db_name: str, uid: str, password: str):
        self.base_url = base_url
        self.db_name = db_name
        self.uid = uid
        self.password = password

        self.server = xmlrpc.client.ServerProxy(f"{self.base_url}/xmlrpc/2/object")

    def call(
        self,
        operation: Operations,
        model: str,
        args: List,
        kwargs: Dict[str, Any] = None,
    ) -> Any:
        """Call the api with a model and an operation

        Args:
            operation: the operation to call
            model: the name of the model
            args: a list of parameters passed by position
            kwargs: a dict of parameters to pass by keyword (optional)
        """
        if not isinstance(operation, Operations):
            raise APIError("Invalid operation")

        kwargs = kwargs if kwargs else {}

        try:
            return self.server.execute_kw(
                self.db_name,
                self.uid,
                self.password,
                model,
                operation.value,
                args,
                kwargs,
            )
        except xmlrpc.client.Fault as error:
            raise APIError(error.faultString) from error
        except socket.gaierror as error:
            raise APIError(str(error)) from error
