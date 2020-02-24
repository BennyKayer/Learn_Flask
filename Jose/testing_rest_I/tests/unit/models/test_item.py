from unittest import TestCase

# Cases
from models.item import ItemModel


class UnitTestItem(TestCase):
    def test_init(self):
        item = ItemModel("Socks", 13)

        self.assertEqual("Socks", item.name)
        self.assertEqual(13, item.price)

    def test_json(self):
        item = ItemModel("Socks", 13)

        self.assertDictEqual({"name": "Socks", "price": 13}, item.json())

