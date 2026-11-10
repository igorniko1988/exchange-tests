from asyncio import timeout

import pytest
import requests

from framework.http_client import HttpClient

WM = 'http://localhost:18090'


@pytest.fixture()
def wm():
    yield WM
    requests.post(f'{WM}/__admin/mappings/reset')
    requests.post(f'{WM}/__admin/requests')

@pytest.fixture()
def client(wm):
    return HttpClient(WM, timeout=1)

def stub(request, response):
    r = requests.post(f'{WM}/__admin/mappings', json={"request": request,
                                                      'response': response})
    assert r.status_code == 201, r.text

def test_price(wm, client):
    stub(
        {'method': 'GET', 'urlPath': '/prices/BTC-USDT'},
        {"status": 200, 'jsonBody': {'price': '3000'},"fixedDelayMilliseconds": 3000}
    )
    r = client.get('/prices/BTC-USDT', timeout=20)
    print(r.json())