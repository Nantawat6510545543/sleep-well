from abc import ABC, abstractmethod
from myapi.models import *
import plotly.express as px

# interface for type hinting/ forcing implementation
class VisualizeStrategy(ABC):
    @abstractmethod
    def get_chart(): pass

class GenderStrategy:
    def get_chart():
        gender_list = ["Male", "Female", "Other"]
        gender_count_list = [Person.objects.filter(sex=each_gender).count() for each_gender in gender_list]

        fig = px.pie(values=gender_count_list, names=gender_list, title="Gender Visualization")
        chart = fig.to_html()
        return chart

class AgeStrategy:
    def get_chart():
        age_list = Person.objects.values_list('age', flat=True)
        fig = px.histogram(age_list, title="Age Visualization", nbins=100)
        fig.update_xaxes(title_text='Age')
        chart = fig.to_html()
        return chart

class HeightStrategy:
    def get_chart():
        height_list = Person.objects.values_list('height', flat=True)
        fig = px.histogram(height_list, title="Height Visualization", nbins=20)
        fig.update_xaxes(title_text='Height')
        chart = fig.to_html()
        return chart

class WeightStrategy:
    def get_chart():
        weight_list = Person.objects.values_list('weight', flat=True)
        fig = px.histogram(weight_list, title="Weight Visualization", nbins=20)
        fig.update_xaxes(title_text='Time')
        chart = fig.to_html()
        return chart