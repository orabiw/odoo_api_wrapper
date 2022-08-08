""" Error Classes """


class APIError(Exception):
    """API Error Base Class"""

    def __init__(self, description, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.description = description
