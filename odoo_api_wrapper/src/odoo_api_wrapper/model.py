""" Odoo model class

## Usage Examples

### Instantiate an `Api`
Create an instance of the API to start using it.
```python
import odoo_api_wrapper

api = odoo_api_wrapper.Api("http://localhost:8069", "db", "1001", "password")
```

### Define your model
```python
partner = odoo_api_wrapper.Model(api, "res.partner")
```

### List records
Records can be listed and filtered via `search()`.
```python
partner.search([[['is_company', '=', True]]])
```

### Count records
Rather than retrieve a possibly gigantic list of records and count them,
`search_count()` can be used to retrieve only the number of records matching the query.
It takes the same domain filter as `search()` and no other parameter.
```python
partner.search_count([[['is_company', '=', True]]])
```

### Read records
Record data are accessible via the `read()` method, which takes a list of ids (as
returned by `search()`), and optionally a list of fields to fetch. By default, it
fetches all the fields the current user can read, which tends to be a huge amount.
```python
ids = partner.search([[['is_company', '=', True]]], {'limit': 1})
[record] = partner.read([ids])
# count the number of fields fetched by default
len(record)
```

### List record fields
`fields_get()` can be used to inspect a model’s fields and check which ones seem to be
of interest.
```python
partner.fields_get([], {'attributes': ['string', 'help', 'type']})
```

### Search and read
Because it is a very common task, Odoo provides a `search_read()` shortcut which, as
its name suggests, is equivalent to a `search()` followed by a `read()`, but avoids
having to perform two requests and keep ids around.
```python
partner.search_read(
    [[['is_company', '=', True]]],
    {'fields': ['name', 'country_id', 'comment'], 'limit': 5},
)
```

### Create records
Records of a model are created using `create()`. The method creates a single record and
returns its database identifier.
```python
id = partner.create([{'name': "New Partner"}])
```

### Update records
Records can be updated using `write()`. It takes a list of records to update and a
mapping of updated fields to values similar to `create()`.
```python
partner.write([[id], {'name': "Newer partner"}])
```

### Delete records
Records can be deleted in bulk by providing their ids to `unlink()`.
```python
partner.unlink([[id]])
```

"""
import functools
from typing import Any, Callable, Dict, List

import odoo_api_wrapper


class Model:  # pylint:disable=too-few-public-methods
    """Odoo model"""

    # define the methods we'll add dynamically
    write: Callable[[List, Dict[str, Any]], Any]
    create: Callable[[List, Dict[str, Any]], Any]
    read: Callable[[List, Dict[str, Any]], Any]
    search: Callable[[List, Dict[str, Any]], Any]
    search_count: Callable[[List, Dict[str, Any]], Any]
    search_read: Callable[[List, Dict[str, Any]], Any]
    fields_get: Callable[[List, Dict[str, Any]], Any]
    unlink: Callable[[List, Dict[str, Any]], Any]

    def __new__(  # pylint:disable=unused-argument
        cls,
        api: odoo_api_wrapper.api.Api,
        model_name: str,
        *args,
        **kwargs,
    ):
        instance = super().__new__(cls)

        for operation in odoo_api_wrapper.Operations.__members__.values():
            func = getattr(api, operation.value)
            setattr(instance, operation.value, functools.partial(func, model_name))

        return instance
