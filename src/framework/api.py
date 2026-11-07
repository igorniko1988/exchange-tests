from framework.http_client import HttpClient
from framework.services.auth_service import AuthService
from framework.services.balances_service import BalancesService
from framework.services.orders_service import OrdersService


class Api:
    def __init__(self, client: HttpClient):
        self.client = client
        self.auth = AuthService(self.client)
        self.balances = BalancesService(self.client)
        self.orders = OrdersService(self.client)
