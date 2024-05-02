from abc import ABC, abstractmethod
from myapi.models import *
import plotly.express as px

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
        chart = fig.to_html()
        return chart

class HeightStrategy(VisualizeStrategy):
    def get_chart():
        height_list = Person.objects.values_list('height', flat=True)
        fig = px.histogram(height_list, title="Height Visualization", nbins=20)
        fig.update_xaxes(title_text='Height')
        chart = fig.to_html()
        return chart

class WeightStrategy(VisualizeStrategy):
    def get_chart():
        weight_list = Person.objects.values_list('weight', flat=True)
        fig = px.histogram(weight_list, title="Weight Visualization", nbins=20)
        fig.update_xaxes(title_text='Time')
        chart = fig.to_html()
        return chart

# TODO handle where person_id doesn't exists
# TODO update legend
# TODO add mean value
# TODO format graph position
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
        chart = fig.to_html()
        return chart