import plotly.express as px

from myapi.models import *
from myapi.utils import get_closest_station
from myapi.chart_utils import VisualizeStrategy

TRENDLINE_CONFIG = {
    "trendline": "ols",
    "trendline_color_override": "red",
    "trendline_scope": "overall"
}

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
        fig = px.scatter(x=sleep_duration_list, y=sleep_score_list, **TRENDLINE_CONFIG)
        fig.update_layout(**SleepDurationVSSleepScoreStrategy.layout)
        fig.update_traces(name=f"Sleep Data", showlegend=True)
        chart = fig.to_html()
        return chart


class SleepDurationVSTempCStrategy:
    layout = {
        "title": "Sleep Duration vs Temperature Visualization",
        "xaxis_title": "Sleep Duration",
        "yaxis_title": "Temperature (Celsius)",
    }

    def get_chart() -> str:
        sleep_objects = Sleep.objects.all()
        sleep_duration_list = sleep_objects.values_list('sleep_duration', flat=True)
        
        temp_c_list = []
        for sleep in sleep_objects:
            closest_weather = get_closest_station(sleep, Weather)

            if closest_weather:
                temp_c_list.append(closest_weather.temp_c)
            else:
                temp_c_list.append(None)

        fig = px.scatter(x=sleep_duration_list, y=temp_c_list, **TRENDLINE_CONFIG)
        fig.update_layout(**SleepDurationVSTempCStrategy.layout)
        chart = fig.to_html()
        return chart


class SleepDurationVSPrecipMMStrategy:
    layout = {
        "title": "Sleep Duration vs Precipitation Visualization",
        "xaxis_title": "Sleep Duration",
        "yaxis_title": "Precipitation (mm.)",
    }

    def get_chart() -> str:
        sleep_objects = Sleep.objects.all()
        sleep_duration_list = sleep_objects.values_list('sleep_duration', flat=True)

        precip_list = []
        for sleep in sleep_objects:
            closest_weather = get_closest_station(sleep, Weather)

            if closest_weather:
                precip_list.append(closest_weather.precip_mm)
            else:
                precip_list.append(None)

        fig = px.scatter(x=sleep_duration_list, y=precip_list, **TRENDLINE_CONFIG)
        fig.update_layout(**SleepDurationVSPrecipMMStrategy.layout)
        chart = fig.to_html()
        return chart


class SleepDurationVSHumidityStrategy:
    layout = {
        "title": "Sleep Duration vs Humidity Visualization",
        "xaxis_title": "Sleep Duration",
        "yaxis_title": "Humidity (%)",
    }

    def get_chart() -> str:
        sleep_objects = Sleep.objects.all()
        sleep_duration_list = sleep_objects.values_list('sleep_duration', flat=True)

        humidity_list = []
        for sleep in sleep_objects:
            closest_weather = get_closest_station(sleep, Weather)

            if closest_weather:
                humidity_list.append(closest_weather.humidity)
            else:
                humidity_list.append(None)

        fig = px.scatter(x=sleep_duration_list, y=humidity_list, **TRENDLINE_CONFIG)
        fig.update_layout(**SleepDurationVSHumidityStrategy.layout)
        chart = fig.to_html()
        return chart

class SleepDurationVSNoiseStrategy:
    layout = {
        "title": "Sleep Duration vs Noise Visualization",
        "xaxis_title": "Sleep Duration",
        "yaxis_title": "Noise (dB)",
    }

    def get_chart() -> str:
        sleep_objects = Sleep.objects.all()
        sleep_duration_list = sleep_objects.values_list('sleep_duration', flat=True)

        noise_list = []
        for sleep in sleep_objects:
            closest_noise = get_closest_station(sleep, Noise)

            if closest_noise:
                noise_list.append(closest_noise.noise)
            else:
                noise_list.append(None)

        fig = px.scatter(x=sleep_duration_list, y=noise_list, **TRENDLINE_CONFIG)
        fig.update_layout(**SleepDurationVSNoiseStrategy.layout)
        chart = fig.to_html()
        return chart


class SleepScoreVSTempCStrategy:
    layout = {
        "title": "Sleep Score vs Temperature Visualization",
        "xaxis_title": "Sleep Score",
        "yaxis_title": "Temperature (Celcius)",
    }

    def get_chart() -> str:
        sleep_objects = Sleep.objects.all()
        sleep_score_list = sleep_objects.values_list('sleep_score', flat=True)

        temp_c_list = []
        for sleep in sleep_objects:
            closest_weather = get_closest_station(sleep, Weather)

            if closest_weather:
                temp_c_list.append(closest_weather.temp_c)
            else:
                temp_c_list.append(None)

        fig = px.scatter(x=sleep_score_list, y=temp_c_list, **TRENDLINE_CONFIG)
        fig.update_layout(**SleepScoreVSTempCStrategy.layout)
        chart = fig.to_html()
        return chart

class SleepScoreVSPrecipMMStrategy:
    layout = {
        "title": "Sleep Score vs Precipitation Visualization",
        "xaxis_title": "Sleep Score",
        "yaxis_title": "Precipitation (mm.)",
    }

    def get_chart() -> str:
        sleep_objects = Sleep.objects.all()
        sleep_score_list = sleep_objects.values_list('sleep_score', flat=True)

        precip_list = []
        for sleep in sleep_objects:
            closest_weather = get_closest_station(sleep, Weather)

            if closest_weather:
                precip_list.append(closest_weather.precip_mm)
            else:
                precip_list.append(None)

        fig = px.scatter(x=sleep_score_list, y=precip_list, **TRENDLINE_CONFIG)
        fig.update_layout(**SleepScoreVSPrecipMMStrategy.layout)
        chart = fig.to_html()
        return chart


class SleepScoreVSHumidityStrategy:
    layout = {
        "title": "Sleep Score vs Humidity Visualization",
        "xaxis_title": "Sleep Score",
        "yaxis_title": "Humidity (%)",
    }

    def get_chart() -> str:
        sleep_objects = Sleep.objects.all()
        sleep_score_list = sleep_objects.values_list('sleep_score', flat=True)

        humidity_list = []
        for sleep in sleep_objects:
            closest_weather = get_closest_station(sleep, Weather)

            if closest_weather:
                humidity_list.append(closest_weather.humidity)
            else:
                humidity_list.append(None)

        fig = px.scatter(x=sleep_score_list, y=humidity_list, **TRENDLINE_CONFIG)
        fig.update_layout(**SleepScoreVSHumidityStrategy.layout)
        chart = fig.to_html()
        return chart


class SleepScoreVSNoiseStrategy:
    layout = {
        "title": "Sleep Score vs Noise Visualization",
        "xaxis_title": "Sleep Score",
        "yaxis_title": "Noise (dB)",
    }

    def get_chart() -> str:
        sleep_objects = Sleep.objects.all()
        sleep_score_list = sleep_objects.values_list('sleep_score', flat=True)

        noise_list = []
        for sleep in sleep_objects:
            closest_noise = get_closest_station(sleep, Noise)

            if closest_noise:
                noise_list.append(closest_noise.noise)
            else:
                noise_list.append(None)

        fig = px.scatter(x=sleep_score_list, y=noise_list, **TRENDLINE_CONFIG)
        fig.update_layout(**SleepDurationVSNoiseStrategy.layout)
        chart = fig.to_html()
        return chart