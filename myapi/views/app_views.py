from django.shortcuts import render
from django.views.generic import TemplateView
import plotly.express  as px

from myapi.models import Person


def index(request):
    return render(request, 'myapi/index.html')


class GenderCountView(TemplateView):
    template_name = 'myapi/gender_visualizer.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        gender_list = ["Male", "Female", "Other"]
        gender_count_list = [Person.objects.filter(sex=each_gender).count() for each_gender in gender_list]

        fig = px.pie(values=gender_count_list, names=gender_list, title="Gender Visualization")
        chart = fig.to_html()
        context['chart'] = chart
        return context
