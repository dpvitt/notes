import unittest
from app.helpers import TimeHelper

class TimeHelperTestCase(unittest.TestCase):

    timestamp = '1990-06-29 13:00:00.245934';

    def test_time_formatted_correctly(self):
        response = TimeHelper.format_time(self.timestamp)
        self.assertTrue('13:00 - Friday 29 June 1990')

    def test_day_formatted_correctly(self):
        response = TimeHelper.get_day(self.timestamp)
        self.assertTrue('29' in response)

    def test_month_formatted_correctly(self):
        response = TimeHelper.get_month(self.timestamp)
        self.assertTrue('June' in response.values())
        self.assertTrue('06' in response.values())

    def test_year_formatted_correctly(self):
        response = TimeHelper.get_year(self.timestamp)
        self.assertTrue('1990' in response)
