from framework.http_client import HttpClient


class BaseService:
    def __init__(self, client: HttpClient):
        self.client = client
