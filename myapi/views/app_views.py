from myapi.chart_utils import *
from django.shortcuts import render
from django.views.generic import TemplateView


def index(request):
    return render(request, 'myapi/index.html')

def get_visualize_list_view(request):
    return render(request, 'myapi/visualize_list.html')


class BaseVisualizeView(TemplateView):
    template_name = 'myapi/visualize.html'
    strategy_class: VisualizeStrategy = None

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['chart'] = self.strategy_class.get_chart()
        return context

class GenderView(BaseVisualizeView):
    strategy_class = GenderStrategy