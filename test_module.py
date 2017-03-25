import app
import time
import icon_get
import unittest


class SmokeTests(unittest.TestCase):
    def test_get_urls(self):
        T = icon_get.get_urls
        assert T("minecraft")
        assert T("Dota 2")
        assert T("Photoshop")

    """
    def app_run_test(self):
        test_app = app.RainApp()
        test_app.run()
        app.RainApp.get_running_app().stop()
    """
