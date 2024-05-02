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
