from rest_framework import serializers
from .models import Sleep, Person


class SleepInfoSerializer(serializers.ModelSerializer):
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


class AverageEnvironmentSerializer(serializers.Serializer):
    noise_avg = serializers.FloatField()
    temp_c_avg = serializers.FloatField()
    precip_mm_avg = serializers.FloatField()
    humidity_avg = serializers.FloatField()
