from models.item import ItemModel
from tests.base_test import BaseTest


class IntegrationTestItem(BaseTest):
    def test_crud(self):
        with self.app_context():
            item = ItemModel("Socks", 13)

            # Make sure it's not there already then insert
            self.assertIsNone(ItemModel.find_by_name("Socks"))
            item.save_to_db()

            self.assertIsNotNone(ItemModel.find_by_name("Socks"))

            # Delete and make sure it's no longer there
            item.delete_from_db()
            self.assertIsNone(ItemModel.find_by_name("Socks"))
