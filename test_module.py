import icon_get
import unittest


class SmokeTests(unittest.TestCase):
    def test_image_search(self):
        T = icon_get.get_image
        assert T("minecraft")
        assert T("Dota 2")
