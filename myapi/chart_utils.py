from abc import ABC, abstractmethod
from myapi.models import *

import numpy as np
import plotly.express as px

# TODO fix for vertical
def add_mean_line_to_chart(data_list, fig):
    # Add mean value line
    mean_data = np.mean(data_list)
    line_settings = {
        "line_dash": "dash",
        "line_color": "red",
        "annotation_text": f'Mean: {mean_data:.2f}'
    }
    chart_type = fig.data[0].type

    # Add vertical line if chart is Histogram
    if chart_type == 'histogram':
        fig.add_vline(x=mean_data, **line_settings)

    # Else, Add horizontal line if chart is Line
    elif chart_type == 'scatter':
        fig.add_hline(y=mean_data, **line_settings)


# interface for type hinting/ forcing implementation
class VisualizeStrategy(ABC):
    @abstractmethod
    def get_chart(): pass

class GenderStrategy(VisualizeStrategy):
    def get_chart():
        gender_list = ["Male", "Female", "Other"]
        gender_count_list = [Person.objects.filter(sex=each_gender).count() for each_gender in gender_list]

        fig = px.pie(values=gender_count_list, names=gender_list, title="Gender Visualization")
        chart = fig.to_html()
        return chart

class AgeStrategy(VisualizeStrategy):
    def get_chart():
        age_list = Person.objects.values_list('age', flat=True)
        fig = px.histogram(age_list, title="Age Visualization", nbins=100)
        fig.update_xaxes(title_text='Age')
        fig.update_traces(name=f"Age Data", showlegend=True)
        add_mean_line_to_chart(age_list, fig)
        chart = fig.to_html()
        return chart

class HeightStrategy(VisualizeStrategy):
    def get_chart():
        height_list = Person.objects.values_list('height', flat=True)
        fig = px.histogram(height_list, title="Height Visualization", nbins=20)
        fig.update_xaxes(title_text='Height')
        fig.update_traces(name=f"Height Data", showlegend=True)
        add_mean_line_to_chart(height_list, fig)
        chart = fig.to_html()
        return chart

class WeightStrategy(VisualizeStrategy):
    def get_chart():
        weight_list = Person.objects.values_list('weight', flat=True)
        fig = px.histogram(weight_list, title="Weight Visualization", nbins=20)
        fig.update_xaxes(title_text='Weight')
        fig.update_traces(name=f"Weight Data", showlegend=True)
        add_mean_line_to_chart(weight_list, fig)
        chart = fig.to_html()
        return chart

# TODO handle where person_id doesn't exists
# TODO format graph position
# TODO refactor
# interface for type hinting/ forcing implementation
class VisualizeByPersonStrategy(ABC):
    @abstractmethod
    def get_chart_by_id(person_id: int): pass

class SleepTimeStrategy(VisualizeByPersonStrategy):
    def get_chart_by_id(person_id: int):
        sleep_list_by_person = Sleep.objects.filter(person_id=person_id)
        sleep_time_list = sleep_list_by_person.values_list('sleep_time', flat=True)
        hour_list = [dt.hour for dt in sleep_time_list]
        fig = px.histogram(hour_list, title="Sleep Time Visualization", nbins=24)
        fig.update_xaxes(title_text='Sleep Hour')
        fig.update_traces(name=f"Person {person_id}'s sleep time", showlegend=True)

        add_mean_line_to_chart(hour_list, fig)
        chart = fig.to_html()
        return chart

class SleepDurationStrategy(VisualizeByPersonStrategy):
    def get_chart_by_id(person_id: int):
        sleep_list_by_person = Sleep.objects.filter(person_id=person_id)
        sleep_time_list = sleep_list_by_person.values_list('sleep_time', flat=True)
        sleep_duration_list = sleep_list_by_person.values_list('sleep_duration', flat=True)
        fig = px.line(x=sleep_time_list, y=sleep_duration_list, title="Sleep Duration Visualization")
        fig.update_xaxes(title_text='Sleep Time')
        fig.update_yaxes(title_text='Sleep Duration (hours)')
        fig.update_traces(name=f"Person {person_id}'s sleep duration", showlegend=True)

        add_mean_line_to_chart(sleep_duration_list, fig)
        chart = fig.to_html()
        return chart

class SleepScoreStrategy(VisualizeByPersonStrategy):
    def get_chart_by_id(person_id: int):
        sleep_list_by_person = Sleep.objects.filter(person_id=person_id)
        sleep_time_list = sleep_list_by_person.values_list('sleep_time', flat=True)
        sleep_score_list = sleep_list_by_person.values_list('sleep_score', flat=True)
        fig = px.line(x=sleep_time_list, y=sleep_score_list, title="Sleep Score Visualization")
        fig.update_xaxes(title_text='Sleep Time')
        fig.update_yaxes(title_text='Sleep Score')
        fig.update_traces(name=f"Person {person_id}'s sleep score", showlegend=True)

        add_mean_line_to_chart(sleep_score_list, fig)
        chart = fig.to_html()
        return chart