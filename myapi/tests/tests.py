from django.test import TestCase
from django.utils import timezone
from datetime import timedelta
from myapi.models import Sleep, Weather, Noise, Person
from myapi.views import get_environments


class TestGetEnvironments(TestCase):
    def setUp(self):
        # Create sample data for testing
        self.person1 = Person.objects.create(
            sex='Male',
            age=30,
            height=175.0,
            weight=70.0,
        )
        self.sleep1 = Sleep.objects.create(
            person=self.person1,
            sleep_time=timezone.now(),
            lat=0,
            lon=0,
            sleep_duration=12,
            sleep_score=90
        )
        self.sleep2 = Sleep.objects.create(
            person=self.person1,
            sleep_time=timezone.now() - timedelta(days=1),
            lat=0,
            lon=0,
            sleep_duration=9,
            sleep_score=50
        )
        self.weather1 = Weather.objects.create(
            lat=0,
            lon=0,
            timestamp=timezone.now(),
            temp_c=25.0,
            precip_mm=5.0,
            humidity=60,
        )
        self.weather2 = Weather.objects.create(
            lat=0,
            lon=0,
            timestamp=timezone.now() - timedelta(days=1),
            temp_c=30.0,
            precip_mm=2.0,
            humidity=50,
        )
        self.noise1 = Noise.objects.create(
            lat=0,
            lon=0,
            timestamp=timezone.now(),
            noise=60.0,
        )
        self.noise2 = Noise.objects.create(
            lat=0,
            lon=0,
            timestamp=timezone.now() - timedelta(days=1),
            noise=55.0,
        )

    def test_get_environments(self):
        sleeps = [self.sleep1, self.sleep2]
        expected_avg_temp_c = (self.weather1.temp_c + self.weather2.temp_c) / 2
        expected_avg_precip_mm = (self.weather1.precip_mm
                                  + self.weather2.precip_mm) / 2
        expected_avg_humidity = (self.weather1.humidity
                                 + self.weather2.humidity) / 2
        expected_avg_noise = (self.noise1.noise + self.noise2.noise) / 2

        result = get_environments(sleeps)

        self.assertAlmostEqual(result['avg_temp_c'],
                               expected_avg_temp_c, places=2)
        self.assertAlmostEqual(result['avg_precip_mm'],
                               expected_avg_precip_mm, places=2)
        self.assertAlmostEqual(result['avg_humidity'],
                               expected_avg_humidity, places=2)
        self.assertAlmostEqual(result['avg_noise'],
                               expected_avg_noise, places=2)

    def tearDown(self):
        # Clean up after the test
        Person.objects.all().delete()
        Sleep.objects.all().delete()
        Weather.objects.all().delete()
        Noise.objects.all().delete()
