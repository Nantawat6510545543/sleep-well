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
    closest_weather = WeatherSerializer(required=False, allow_null=True)
    closest_noise_station = NoiseStationSerializer(required=False, allow_null=True)

    class Meta:
        model = Sleep
        fields = '__all__'


class PersonInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Person
        fields = '__all__'


class SleepTrainSerializer(SleepInfoSerializer):
    person = PersonInfoSerializer()


class SentimentAnalyticsSerializer(serializers.Serializer):
    total_comments = serializers.IntegerField()
    positive_percentage = serializers.FloatField()
    negative_percentage = serializers.FloatField()
    neutral_percentage = serializers.FloatField()
    average_sentiment = serializers.FloatField()


class EnvironmentSerializer(serializers.Serializer):
    avg_temp_c = serializers.FloatField()
    avg_precip_mm = serializers.FloatField()
    avg_humidity = serializers.FloatField()
    avg_noise = serializers.FloatField()


class SleepInfoAnalyticsSerializer(serializers.Serializer):
    person_id = serializers.IntegerField()
    average_score = serializers.FloatField()
    opinion_analytics = SentimentAnalyticsSerializer()
    environment = EnvironmentSerializer()
