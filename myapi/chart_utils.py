from abc import ABC, abstractmethod
from typing import Any
from myapi.models import *

from myapi.analytics import get_sentiment
from myapi.utils import get_closest_station
import numpy as np
import plotly.express as px
import plotly.graph_objects as go


def add_mean_line_to_chart(data_list: list[Any], fig: go.Figure):
    arr = np.array(data_list, dtype=float)
    mean_data = np.nanmean(arr)  # get mean
    chart_type = fig.data[0].type   # get chart type

    line_settings = {
        "line_dash": "dash",
        "line_color": "red",
        "annotation_text": f'Mean: {mean_data:.2f}'
    }

    # Add vertical line if chart is Histogram
    if chart_type == 'histogram':
        fig.add_vline(x=mean_data, **line_settings)

    # Else, Add horizontal line if chart is Line
    elif chart_type == 'scatter':
        fig.add_hline(y=mean_data, **line_settings)


# interface for type hinting/ forcing implementation
class VisualizeStrategy(ABC):
    # Should return HTML string representation
    @abstractmethod
    def get_chart() -> str: 
        pass


class GenderStrategy(VisualizeStrategy):
    layout = {
        "title": "Gender Visualization"
    }

    # TODO fix hardcode
    def get_chart() -> str:
        gender_list = ["Male", "Female", "Other"]
        gender_count_list = [Person.objects.filter(sex=each_gender).count() for each_gender in gender_list]
        fig = px.pie(values=gender_count_list, names=gender_list)
        fig.update_layout(**GenderStrategy.layout)

        chart = fig.to_html()
        return chart


class AgeStrategy(VisualizeStrategy):
    layout = {
        "title": "Age Visualization",
        "xaxis_title": "Age",
    }

    def get_chart() -> str:
        age_list = Person.objects.values_list('age', flat=True)
        fig = px.histogram(age_list, nbins=100)
        fig.update_layout(**AgeStrategy.layout)
        fig.update_traces(name=f"Age Data")
        add_mean_line_to_chart(age_list, fig)
        chart = fig.to_html()
        return chart


class HeightStrategy(VisualizeStrategy):
    layout = {
        "title": "Height Visualization",
        "xaxis_title": "Height",
    }

    def get_chart() -> str:
        height_list = Person.objects.values_list('height', flat=True)
        fig = px.histogram(height_list, nbins=20)
        fig.update_layout(**HeightStrategy.layout)
        fig.update_traces(name=f"Height Data")
        add_mean_line_to_chart(height_list, fig)
        chart = fig.to_html()
        return chart


class WeightStrategy(VisualizeStrategy):
    layout = {
        "title": "Weight Visualization",
        "xaxis_title": "Weight",
    }

    def get_chart() -> str:
        weight_list = Person.objects.values_list('weight', flat=True)
        fig = px.histogram(weight_list, nbins=20)
        fig.update_layout(**WeightStrategy.layout)
        fig.update_traces(name=f"Weight Data", showlegend=True)
        add_mean_line_to_chart(weight_list, fig)
        chart = fig.to_html()
        return chart


class SleepAnalyticsStrategy(VisualizeStrategy):
    layout = {
        "title": "Average Sleep Score Visualization",
        "xaxis_title": "Sleep Score",
    }

    def get_chart() -> str:
        data = []
        for person in Person.objects.all():
            sleeps = Sleep.objects.filter(person_id=person.person_id).select_related('person')
            comments_list = sleeps.values_list('sleep_comment', flat=True)
            sentiments_list = [get_sentiment(comment) for comment in comments_list]
            average_sentiment = np.mean(sentiments_list) if sentiments_list else None
            data.append(average_sentiment)

        fig = px.histogram(x=data, nbins=20)
        fig.update_layout(**SleepAnalyticsStrategy.layout)
        fig.update_traces(name=f"Sleep Score Data", showlegend=True)
        chart = fig.to_html()
        return chart


class TempCStrategy(VisualizeStrategy):
    layout = {
        "title": "Average Temperature Visualization",
        "xaxis_title": "Time",
        "yaxis_title": "Temperature (Celcius)",
    }

    def get_chart() -> str:
        temp_c_list = []
        sleep_time_list = []

        sleep_objects_sorted = Sleep.objects.all().order_by('sleep_time')
        for sleep in sleep_objects_sorted:
            sleep_time_list.append(sleep.sleep_time)

            closest_weather = get_closest_station(sleep, Weather)
            if closest_weather:
                temp_c_list.append(closest_weather.temp_c)
            else:
                temp_c_list.append(None)

        fig = px.line(x=sleep_time_list, y=temp_c_list)
        fig.update_layout(**TempCStrategy.layout)
        add_mean_line_to_chart(temp_c_list, fig)
        chart = fig.to_html()
        return chart


class ConditionTextStrategy(VisualizeStrategy):
    layout = {
        "title": "Condition Text Visualization"
    }

    def get_chart() -> str:
        condition_text_list = []

        for sleep in Sleep.objects.all():
            closest_weather = get_closest_station(sleep, Weather)
            if closest_weather:
                condition_text_list.append(closest_weather.condition_text)

        unique_text, text_count = np.unique(condition_text_list, return_counts=True)

        fig = px.pie(values=text_count, names=unique_text)
        fig.update_layout(**ConditionTextStrategy.layout)
        chart = fig.to_html()
        return chart


class PrecipMMStrategy(VisualizeStrategy):
    layout = {
        "title": "Average Precipitation Visualization",
        "xaxis_title": "Time",
        "yaxis_title": "Precipitation (mm.)",
    }

    def get_chart() -> str:
        precip_mm_list = []
        sleep_time_list = []

        sleep_objects_sorted = Sleep.objects.all().order_by('sleep_time')
        for sleep in sleep_objects_sorted:
            sleep_time_list.append(sleep.sleep_time)

            closest_weather = get_closest_station(sleep, Weather)
            if closest_weather:
                precip_mm_list.append(closest_weather.precip_mm)
            else:
                precip_mm_list.append(None)

        fig = px.line(x=sleep_time_list, y=precip_mm_list)
        fig.update_layout(**PrecipMMStrategy.layout)
        add_mean_line_to_chart(precip_mm_list, fig)
        chart = fig.to_html()
        return chart



class HumidityStrategy(VisualizeStrategy):
    layout = {
        "title": "Average Humidity Visualization",
        "xaxis_title": "Time",
        "yaxis_title": "Humidity (%)",
    }

    def get_chart() -> str:
        humidity_list = []
        sleep_time_list = []

        sleep_objects_sorted = Sleep.objects.all().order_by('sleep_time')
        for sleep in sleep_objects_sorted:
            sleep_time_list.append(sleep.sleep_time)

            closest_weather = get_closest_station(sleep, Weather)
            # closest_noise_station = get_closest_station(sleep, Noise)
            if closest_weather:
                humidity_list.append(closest_weather.humidity)
            else:
                humidity_list.append(None)

        fig = px.line(x=sleep_time_list, y=humidity_list)
        fig.update_layout(**HumidityStrategy.layout)
        add_mean_line_to_chart(humidity_list, fig)
        chart = fig.to_html()
        return chart



class NoiseStrategy(VisualizeStrategy):
    layout = {
        "title": "Average Noise Visualization",
        "xaxis_title": "Time",
        "yaxis_title": "Noise (dB)",
    }

    def get_chart() -> str:
        noise_list = []
        sleep_time_list = []

        sleep_objects_sorted = Sleep.objects.all().order_by('sleep_time')
        for sleep in sleep_objects_sorted:
            sleep_time_list.append(sleep.sleep_time)

            closest_noise = get_closest_station(sleep, Noise)
            # closest_noise_station = get_closest_station(sleep, Noise)
            if closest_noise:
                noise_list.append(closest_noise.noise)
            else:
                noise_list.append(None)

        fig = px.line(x=sleep_time_list, y=noise_list)
        fig.update_layout(**NoiseStrategy.layout)
        add_mean_line_to_chart(noise_list, fig)
        chart = fig.to_html()
        return chart


class SleepDurationVSSleepScoreStrategy(VisualizeStrategy):
    layout = {
        "title": "Sleep Duration vs Sleep Score Visualization",
        "xaxis_title": "Sleep Duration",
        "yaxis_title": "Sleep Score",
    }

    def get_chart() -> str:
        sleep_objects = Sleep.objects.all()
        sleep_duration_list = sleep_objects.values_list('sleep_duration', flat=True)
        sleep_score_list = sleep_objects.values_list('sleep_score', flat=True)
        fig = px.scatter(x=sleep_duration_list, y=sleep_score_list)
        fig.update_layout(**SleepDurationVSSleepScoreStrategy.layout)
        fig.update_traces(name=f"Sleep  Data", showlegend=True)
        chart = fig.to_html()
        return chart


# TODO refactor
# interface for type hinting/ forcing implementation
class VisualizeByPersonStrategy(ABC):
    @abstractmethod
    def get_chart_by_id(person_id: int) -> str: pass


class SleepTimeStrategy(VisualizeByPersonStrategy):
    layout = {
        "title": "Sleep Time Visualization",
        "xaxis_title": "Sleep Hour",
        "showlegend": True
    }

    def get_chart_by_id(person_id: int) -> str:
        sleep_list_by_person = Sleep.objects.filter(person_id=person_id)
        sleep_time_list = sleep_list_by_person.values_list('sleep_time', flat=True)
        hour_list = [dt.hour for dt in sleep_time_list]
        fig = px.histogram(hour_list, nbins=24)
        fig.update_layout(**SleepTimeStrategy.layout)
        fig.update_traces(name=f"Person {person_id}'s sleep time")

        add_mean_line_to_chart(hour_list, fig)
        chart = fig.to_html()
        return chart


class SleepDurationStrategy(VisualizeByPersonStrategy):
    layout = {
        "title": "Sleep Duration Visualization",
        "xaxis_title": "Sleep Time",
        "yaxis_title": "Sleep Duration (hours)"
    }

    def get_chart_by_id(person_id: int) -> str:
        sleep_list_by_person = Sleep.objects.filter(person_id=person_id)
        sleep_time_list = sleep_list_by_person.values_list('sleep_time', flat=True)
        sleep_duration_list = sleep_list_by_person.values_list('sleep_duration', flat=True)
        fig = px.line(x=sleep_time_list, y=sleep_duration_list)
        fig.update_layout(**SleepDurationStrategy.layout)
        fig.update_traces(name=f"Person {person_id}'s sleep duration", showlegend=True)

        add_mean_line_to_chart(sleep_duration_list, fig)
        chart = fig.to_html()
        return chart


class SleepScoreStrategy(VisualizeByPersonStrategy):
    layout = {
        "title": "Sleep Score Visualization",
        "xaxis_title": "Sleep Time",
        "yaxis_title": "Sleep Score"
    }

    def get_chart_by_id(person_id: int):
        sleep_list_by_person = Sleep.objects.filter(person_id=person_id)
        sleep_time_list = sleep_list_by_person.values_list('sleep_time', flat=True)
        sleep_score_list = sleep_list_by_person.values_list('sleep_score', flat=True)
        fig = px.line(x=sleep_time_list, y=sleep_score_list)
        fig.update_layout(**SleepScoreStrategy.layout)
        fig.update_traces(name=f"Person {person_id}'s sleep score", showlegend=True)

        add_mean_line_to_chart(sleep_score_list, fig)
        chart = fig.to_html()
        return chart
