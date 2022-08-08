""" Example call """
import odoo_api_wrapper


def main():
    """main"""
    api = odoo_api_wrapper.Api(
        "http://localhost:89",
        "Demo Company",
        "1001",
        "password",
    )

    api.search("somemodel", "something")


if __name__ == "__main__":
    main()
