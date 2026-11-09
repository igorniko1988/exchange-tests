import logging

import allure
import requests

from framework.masking import mask_body, mask_headers

logger = logging.getLogger(__name__)


class HttpClient:
    def __init__(self, base_url: str, timeout: float):
        self.base_url = base_url.rstrip("/")
        self.timeout = timeout
        self.session = requests.Session()
        self.session.headers.update({"Accept": "application/json"})

    def request(self, method, path, **kwargs) -> requests.Response:
        kwargs.setdefault("timeout", self.timeout)
        url = f"{self.base_url}/{path.lstrip('/')}"
        response = self.session.request(method, url, **kwargs)
        logger.info(f"{method} {url} {response.status_code} {response.elapsed}")
        self._attach(response)
        return response

    def _attach(self, response):
        req = response.request
        allure.attach(
            f"{req.method} {req.url}\n\n{mask_headers(req.headers)}\n\n{mask_body(req.body)}",
            name="request",
            attachment_type=allure.attachment_type.TEXT,
        )
        allure.attach(
            f"{response.status_code}\n\n{mask_body(response.text)}",
            name="response",
            attachment_type=allure.attachment_type.JSON,
        )

    def set_token(self, token):
        self.session.headers.update({"Authorization": f"Bearer {token}"})

    def clear_token(self):
        self.session.headers.pop("Authorization", None)

    def get(self, path, **kwargs) -> requests.Response:
        return self.request("GET", path, **kwargs)

    def post(self, path, **kwargs) -> requests.Response:
        return self.request("POST", path, **kwargs)

    def delete(self, path, **kwargs) -> requests.Response:
        return self.request("DELETE", path, **kwargs)

    def patch(self, path, **kwargs) -> requests.Response:
        return self.request("PATCH", path, **kwargs)
