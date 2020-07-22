def test_default_and_getting(db):
    db.add_server(123)
    assert db.get_setting("prefix", 123) == "!"


def test_updating(db):
    db.add_server(123)

    db.update_setting(123, "prefix", "?")
    assert db.get_setting("prefix", 123) == "?"
