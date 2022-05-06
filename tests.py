from django.test import TestCase
from projects.views import *
from p_users.views import *
from math import sqrt, log, factorial, pow
import logging
logger = logging.getLogger(__name__)

class OpsTestCase(TestCase):
    def setUp(self):
        pass
    def test_operations(self):
        """WE WILL TEST ALL OPERATIONS ARE PERFORMED CORRECTLY OR NOT"""

        logger.info("Running three assert tests")
        self.assertEqual(200, get_queries_api().status_code)
        self.assertEqual(200, get_profiles().status_code)
        self.assertEqual(200, get_projects_api().status_code)
        logger.info("All three assert tests, passed!")