
import unittest

from keyvault.store import KeyValueStore


class TestKeyValueStore(unittest.TestCase):
    def setUp(self):
        self.store = KeyValueStore()

    def test_set_and_get(self):
        self.store.set("name", "Deo")
        self.assertEqual(self.store.get("name"), "Deo")

    def test_overwrite(self):
        self.store.set("name", "first")
        self.store.set("name", "second")
        self.assertEqual(self.store.get("name"), "second")

    def test_missing_key(self):
        self.assertIsNone(self.store.get("missing"))

    def test_delete(self):
        self.store.set("name", "Deo")
        self.assertTrue(self.store.delete("name"))
        self.assertFalse(self.store.exists("name"))

    def test_exists(self):
        self.store.set("active", "yes")
        self.assertTrue(self.store.exists("active"))

    def test_count(self):
        self.store.set("a", "1")
        self.store.set("b", "2")
        self.assertEqual(self.store.count(), 2)


if __name__ == "__main__":
    unittest.main()
