import pytest

from framework.masking import mask_body, mask_headers


@pytest.mark.parametrize(
    "raw, secret",
    [
        ('{"email":"a@b.com","password":"Pass12345"}', "Pass12345"),
        ('{"data":{"access_token":"tok123"}}', "tok123"),
        (b'{"refresh_token":"ref999"}', "ref999"),
    ],
    ids=["password", "nested-token", "bytes"],
)
def test_mask_body_hides_secrets(raw, secret):
    assert secret not in mask_body(raw)


def test_mask_body_keeps_non_json_and_none():
    assert mask_body("not json") == "not json"
    assert mask_body(None) == ""


def test_mask_headers_hides_authorization():
    out = mask_headers({"Authorization": "Bearer secret", "Accept": "application/json"})
    assert "secret" not in out
    assert "Accept: application/json" in out
