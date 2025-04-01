import unittest
from . import main, webapi

def main_():
    main_suite = main.get_test_suite()
    webapi_suite = webapi.get_test_suite()
    runner = unittest.TextTestRunner(verbosity=2)
    runner.run(webapi_suite)
