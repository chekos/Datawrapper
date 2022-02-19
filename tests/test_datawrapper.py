from datawrapper import Datawrapper


def test_account_info():
    account_info = Datawrapper().account_info()
    assert "id" in account_info.keys()
    assert "email" in account_info.keys()
    assert "name" in account_info.keys()
    assert "role" in account_info.keys()
    assert "language" in account_info.keys()
    assert "teams" in account_info.keys()
    assert "chartCount" in account_info.keys()
    assert "url" in account_info.keys()
