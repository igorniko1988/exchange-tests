def test_two_users(make_user):
    alice = make_user()
    bob = make_user()

    alice_details = alice.auth.me()
    assert alice_details.status_code == 200
    alice_email = alice_details.json()["email"]

    bob_details = bob.auth.me()
    assert bob_details.status_code == 200
    bob_email = bob_details.json()["email"]

    assert alice_email != bob_email
