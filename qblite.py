"""
For now, just scratch paper for Leigh to think about design of classes.
"""

import requests
import json
import pandas as pd
from typing import List, Dict


class App:
    """
    Hybrid of App as in Quickbase app and client--
    intended as client for single app, not entire Quickbase software.
    Meant to provide a familiar interface to navigating an app.
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
    Request for querying records from a table.
    """

    def __init__(self, body: dict = None):
        if body:
            self.body = body
        else:
            pass

    def __repr__(self) -> str:
        return self.body

    def filter(
        self,
        criteria: List[Dict] = [{"field": int, "operator": str, "value": str}],
    ) -> str:
        """
        Format valid string to be used as "where" parameter in query API call.
        criteria dict should follow pattern of {"field": int, "operator": str, "value": str}.
        """
        for criterion in criteria:
            if not isinstance(criterion["field"], int):
                try:
                    criterion["field"] = int(criterion["field"])
                except ValueError:
                    return ValueError("Key 'field' must have value of type int")
        strings = []
        for criterion in criteria:
            # Each dict becomes one valid "where"-string component.
            strings.append(
                ".".join(
                    [str(criterion["field"]), criterion["operator"], criterion["value"]]
                )
            )
        # TODO: compose into single string
        return strings

    def build(
        self,
        table: str = None,
        fields: list = None,
        filter_string: str = None,
        sortby: List[Dict[int, str]] = None,
        groupby: List[Dict[int, str]] = None,
        options: dict = None,
    ) -> dict:
        """
        Construct valid dictionary to be used as request body in query API call.
        Requires filter -> filter_string; if omitted, will query all records.
        """
        query_body = {
            "from": table,
            "select": fields,
            "where": filter_string,
            "sortBy": sortby,
            "groupBy": groupby,
            "options": options,
        }
        self.body = query_body

    def run(self, url: str = None):
        """Execute a call to Quickbase query API using Query.body as request body."""
        response = requests.get(url, params=self.body)
        return response


class Table:
    """
    Representation of a Quickbase table's fields and metadata.
    """

    def __init__(self, id: str, connection: dict = None) -> None:
        self.id = id
        self.fields = self._get_fields(connection)
        pass

    def _get_fields(self, connection):
        if not self.fields:
            api_url = f"https://api.quickbase.com/v1/fields?tableId={self.id}"
            response = requests.get(api_url, headers=connection)
            if response.status_code == 200:
                fields = response.json()
                fields_dict = {d["id"]: d["label"] for d in fields}
                return fields_dict
            return None
        else:
            return self.fields

    # if not self.data:
    # self.data = self.get_data()
