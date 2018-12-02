
from tests.persist.baseTest import BaseTest
from app.persist import configDao


class ConfigDaoTestCase(BaseTest):

    def test_get_config_by_key(self):
        print("running test_get_config_by_key...")

        config_item = configDao.get_config_by_key("app.release_number")
        print("config_value: " + str(config_item))
        self.assertTrue(len(config_item.value) > 0)

    def test_get_config_all(self):
        print("running get_config_all...")

        config_items = configDao.get_config_all()
        print("config_items: " + str(config_items))
        self.assertTrue(len(config_items) > 0)

        self.assertTrue(len(config_items[0].key) > 0)
        self.assertTrue(len(config_items[0].value) > 0)
