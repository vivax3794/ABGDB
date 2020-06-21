class TestPrefix:
    def test_prefix_add(self, db):
        db.prefix_add(123, "!")
        assert db.prefix_get(123) == "!"

    def test_prefix_update(self, db):
        db.prefix_add(123, "!")

        db.prefix_update(123, "?")
        assert db.prefix_get(123) == "?"