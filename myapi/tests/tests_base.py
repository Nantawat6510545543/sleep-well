from datetime import timedelta
from django.utils import timezone
from django.test import TestCase
from myapi.models import Person, Sleep, Weather, Noise


class TestFactory:
    @staticmethod
    def create_person(sex, age, height, weight):
        return Person.objects.create(sex=sex, age=age, height=height,
                                     weight=weight)

    @staticmethod
    def create_sleep(person, days_ago, duration, score, lat, lon,
                     sleep_comment="No comments"):
        sleep_time = timezone.now() - timedelta(days=days_ago)
        return Sleep.objects.create(
            person=person,
            sleep_time=sleep_time,
            lat=lat,
            lon=lon,
            sleep_duration=duration,
            sleep_score=score,
            sleep_comment=sleep_comment,
        )

    @staticmethod
    def create_weather(days_ago, temp_c, precip_mm, humidity, lat, lon):
        timestamp = timezone.now() - timedelta(days=days_ago)
        return Weather.objects.create(
            lat=lat,
            lon=lon,
            timestamp=timestamp,
            temp_c=temp_c,
            precip_mm=precip_mm,
            humidity=humidity,
        )

    @staticmethod
    def create_noise(days_ago, noise, lat, lon):
        timestamp = timezone.now() - timedelta(days=days_ago)
        return Noise.objects.create(
            lat=lat,
            lon=lon,
            timestamp=timestamp,
            noise=noise,
        )


class BaseTest(TestCase):
    def setUp(self):
        factory = TestFactory()
        # A very closet to station
        self.personA = factory.create_person('Male', 30, 175.0, 70.0)
        self.sleepA1 = factory.create_sleep(self.personA, 0, 12, 90, 0, 0)
        self.sleepA2 = factory.create_sleep(self.personA, 1, 9, 50, 0, 0)

        # B is too far from any station
        self.personB = factory.create_person('Female', 25, 155.0, 50.0)
        self.sleepB1 = factory.create_sleep(self.personB, 0, 8, 70, 50, 100)
        self.sleepB2 = factory.create_sleep(self.personB, 1, 7, 40, 50, 100)

        # C has some sleep that have no station within range
        self.personC = factory.create_person('Male', 50, 185.0, 90.0)
        self.sleepC1 = factory.create_sleep(self.personC, 0, 12, 90, 0, 0)
        self.sleepC2 = factory.create_sleep(self.personC, 1, 9, 50, 0, 0)
        self.sleepC3 = factory.create_sleep(self.personC, 2, 9, 50, 0, 0)

        # D has some sleep that have different station within range to A
        self.personD = factory.create_person('Female', 12, 120.0, 30.0)
        self.sleepD1 = factory.create_sleep(self.personD, 0, 12, 90, 0.06,
                                            0.06)
        self.sleepD2 = factory.create_sleep(self.personD, 1, 9, 50, 0.06,
                                            0.06)
        self.sleepD3 = factory.create_sleep(self.personD, 2, 9, 50, 0.06,
                                            0.06)

        # station for all tests
        self.weather1 = factory.create_weather(0, 25.0, 5.0, 60, 0.03, 0.03)
        self.weather2 = factory.create_weather(1, 30.0, 2.0, 50, 0.03, 0.03)
        self.noise1 = factory.create_noise(0, 60.0, 0.03, 0.03)
        self.noise2 = factory.create_noise(1, 55.0, 0.03, 0.03)

        # station for D only
        self.weather3 = factory.create_weather(2, 40.0, 0, 50, 0.06, 0.06)
        self.noise3 = factory.create_noise(2, 75.0, 0.06, 0.06)
