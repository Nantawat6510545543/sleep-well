from rest_framework import serializers
from .models import Sleep, Person, Weather, Noise


class WeatherSerializer(serializers.ModelSerializer):
    class Meta:
        model = Weather
        fields = ('temp_c', 'condition_text', 'precip_mm', 'humidity')


class NoiseStationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Noise
        fields = ('noise',)


class SleepInfoSerializer(serializers.ModelSerializer):
    closest_weather = WeatherSerializer()
    closest_noise_station = NoiseStationSerializer()

    class Meta:
        model = Sleep
        fields = '__all__'


class PersonInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Person
        fields = '__all__'


class SentimentAnalyticsSerializer(serializers.Serializer):
    average_sentiment = serializers.FloatField()
    total_comments = serializers.IntegerField()


class SleepInfoAnalyticsSerializer(serializers.Serializer):
    person_info = PersonInfoSerializer()
    average_score = serializers.FloatField()
    opinion_analytics = SentimentAnalyticsSerializer()
