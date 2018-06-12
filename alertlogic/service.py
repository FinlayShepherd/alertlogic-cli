import requests

class InvalidEndpointCall(Exception):
    pass


class Service:

    def __init__(self):
        self._session = None

    def set_session(self, session):
        """ changes current session, this session object is used to authenticate
         api calls
        :param session: an authenticated alertlogic.auth.Session object
        """
        self._session = session

    def call_endpoint(self, method, endpoint_path, params=None, json=None):
        url = self._session.region.get_api_endpoint() + endpoint_path
        try:
            return requests.request(method, url, params=params, json=json, auth=self._session)
        except requests.exceptions.HTTPError as e:
            raise InvalidEndpointCall(e.message)