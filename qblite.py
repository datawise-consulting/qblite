"""
For now, just scratch paper for Leigh to think about design of classes.
"""

import requests


class App:
    """
    Hybrid of App as in Quickbase app and client.
    Meant to provide a familiar experience to navigating a single app.
    """

    def __init__(self, id: str, headers: dict):
        """
        Connect to a Quickbase app by ID.
        """
        self.connection = headers
        self.id = id


# class Connection:
#     """
#     Representation of both request and response for authorizing access to Quickbase's REST API.
#     """

#     def __init__(self, headers=None):
#         self.headers = headers

#     def __repr__(self) -> str:
#         return str(self.headers)


class Query:
    """
    Request body required for querying records from a table.
    """

    def __init__(self):
        # table: str = None, select: list = None, filter: str = None, sortby = None, groupby = None, options = None
        pass

    def build(self):
        pass

    def run(self, url: str = None, body: dict = None):
        response = requests.get(url, params=body)
        return response


class Table:
    """
    Representation of a table including its fields and data.
    """
