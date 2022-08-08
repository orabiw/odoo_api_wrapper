""" Odoo API wrapper

`odoo_api_wrapper.api.Api` is the main class, `odoo_api_wrapper.api.Operations` defines
the operations used for `odoo_api_wrapper.api.Api.call`, raises
`odoo_api_wrapper.api.APIError`.

## Example Usage

```python
import odoo_api_wrapper

# Instantiate an `Api`
api = odoo_api_wrapper.Api("http://localhost:8069", "db", "1001", "password")

# search
api.search("somemodel", "something")
```


"""
import enum
import socket
import xmlrpc.client
from typing import Any


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

    def __init__(self, description, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.description = description


class Api:
    """API Wrapper"""

    def __init__(self, base_url: str, db_name: str, uid: str, password: str):
        self.base_url = base_url
        self.db_name = db_name
        self.uid = uid
        self.password = password

        self.server = xmlrpc.client.ServerProxy(f"{self.base_url}/xmlrpc/2/object")

    def call(self, model: str, operation: Operations, *args: Any, **kwargs: Any) -> Any:
        """
        Call the api w/ model and an operation

        :param model: str
        :param operation: Operations
        :param args: a list of parameters passed by position
        :param kwargs: a dict of parameters to pass by keyword (optional)
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
            raise APIError(error) from error

    def search_read(self, model: str, *args: Any, **kwargs: Any) -> list:
        """
        call the api w/ model and a "SEARCH_READ" operation
        :param model: str
        :param args: a list of parameters passed by position
        :param kwargs: a dict of parameters to pass by keyword (optional)
        """
        return self.call(model, Operations.SEARCH_READ, *args, **kwargs)

    def read(self, model: str, *args: Any, **kwargs: Any) -> list:
        """
        call the api w/ model and a "READ" operation
        :param model: str
        :param args: a list of parameters passed by position
        :param kwargs: a dict of parameters to pass by keyword (optional)
        """
        return self.call(model, Operations.READ, *args, **kwargs)

    def write(self, model: str, *args: Any, **kwargs: Any) -> list:
        """
        call the api w/ model and a "WRITE" operation
        :param model: str
        :param args: a list of parameters passed by position
        :param kwargs: a dict of parameters to pass by keyword (optional)
        """
        return self.call(model, Operations.WRITE, *args, **kwargs)

    def create(self, model: str, *args: Any, **kwargs: Any) -> list:
        """
        call the api w/ model and a "CREATE" operation
        :param model: str
        :param args: a list of parameters passed by position
        :param kwargs: a dict of parameters to pass by keyword (optional)
        """
        return self.call(model, Operations.CREATE, *args, **kwargs)

    def search(self, model: str, *args: Any, **kwargs: Any) -> list:
        """
        call the api w/ model and a "SEARCH" operation
        :param model: str
        :param args: a list of parameters passed by position
        :param kwargs: a dict of parameters to pass by keyword (optional)
        """
        return self.call(model, Operations.SEARCH, *args, **kwargs)

    def search_count(self, model: str, *args: Any, **kwargs: Any) -> list:
        """
        call the api w/ model and a "SEARCH_COUNT" operation
        :param model: str
        :param args: a list of parameters passed by position
        :param kwargs: a dict of parameters to pass by keyword (optional)
        """
        return self.call(model, Operations.SEARCH_COUNT, *args, **kwargs)

    def fields_get(self, model: str, *args: Any, **kwargs: Any) -> list:
        """
        call the api w/ model and a "FIELDS_GET" operation
        :param model: str
        :param args: a list of parameters passed by position
        :param kwargs: a dict of parameters to pass by keyword (optional)
        """
        return self.call(model, Operations.FIELDS_GET, *args, **kwargs)

    def unlink(self, model: str, *args: Any, **kwargs: Any) -> list:
        """
        call the api w/ model and a "UNLINK" operation
        :param model: str
        :param args: a list of parameters passed by position
        :param kwargs: a dict of parameters to pass by keyword (optional)
        """
        return self.call(model, Operations.UNLINK, *args, **kwargs)
