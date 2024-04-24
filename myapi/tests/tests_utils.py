from myapi.tests.tests_base import BaseTest
from myapi.models import *
from myapi.utils import *


class UtilsTests(BaseTest):

    def test_get_closest(self):
        test_cases = [
            (self.sleepA1, Weather, self.weather1),
            (self.sleepA1, Noise, self.noise1),
            (self.sleepA2, Weather, self.weather2),
            (self.sleepA2, Noise, self.noise2),
            (self.sleepB1, Weather, None),
            (self.sleepB2, Noise, None),
            (self.sleepC1, Weather, self.weather1),
            (self.sleepC1, Noise, self.noise1),
            (self.sleepC2, Weather, self.weather2),
            (self.sleepC2, Noise, self.noise2),
            (self.sleepC3, Weather, None),
            (self.sleepC3, Noise, None),
            (self.sleepD1, Weather, self.weather1),
            (self.sleepD1, Noise, self.noise1),
            (self.sleepD2, Weather, self.weather2),
            (self.sleepD2, Noise, self.noise2),
            (self.sleepD3, Weather, self.weather3),
            (self.sleepD3, Noise, self.noise3),
        ]

        for sleep, station, expected_result in test_cases:
            self.assertEqual(get_closest(sleep, station), expected_result)

    def test_get_environments(self):
        temp_avg = (self.weather1.temp_c + self.weather2.temp_c) / 2
        precip_avg = (self.weather1.precip_mm + self.weather2.precip_mm) / 2
        humidity_avg = (self.weather1.humidity + self.weather2.humidity) / 2
        noise_avg = (self.noise1.noise + self.noise2.noise) / 2

        # Test case for "A": two closest stations, complete data expected
        sleeps = [self.sleepA1, self.sleepA2]
        self.check_environment(sleeps, temp_avg, precip_avg, humidity_avg,
                               noise_avg)

        # Test case for "B": no closest stations, all data should be null
        sleeps = [self.sleepB1, self.sleepB2]
        self.check_environment(sleeps)

        # Test case for "C": missing stations, same result as "A" expected
        sleeps = [self.sleepC1, self.sleepC2, self.sleepC3]
        self.check_environment(sleeps, temp_avg, precip_avg, humidity_avg,
                               noise_avg)

        temp_avg = (self.weather1.temp_c + self.weather2.temp_c
                    + self.weather3.temp_c) / 3
        precip_avg = (self.weather1.precip_mm + self.weather2.precip_mm
                      + self.weather3.precip_mm) / 3
        humidity_avg = (self.weather1.humidity + self.weather2.humidity
                        + self.weather3.humidity) / 3
        noise_avg = (self.noise1.noise + self.noise2.noise
                     + self.noise3.noise) / 3

        # Test case for "D": extra station
        sleeps = [self.sleepD1, self.sleepD2, self.sleepD3]
        self.check_environment(sleeps, temp_avg, precip_avg, humidity_avg,
                               noise_avg)

    def check_environment(self, sleeps, temp=None, precip=None, humidity=None,
                          noise=None):
        result = get_environments(sleeps)

        self.assertAlmostEqual(result.get('avg_temp_c'), temp, places=2)
        self.assertAlmostEqual(result.get('avg_precip_mm'), precip, places=2)
        self.assertAlmostEqual(result.get('avg_humidity'), humidity, places=2)
        self.assertAlmostEqual(result.get('avg_noise'), noise, places=2)
