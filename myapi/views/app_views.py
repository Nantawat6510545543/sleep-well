from myapi.chart_utils import *
from django.shortcuts import redirect, render
from django.views.generic import View, TemplateView


def index(request):
    return render(request, 'myapi/index.html')

def get_visualize_list_view(request):
    return render(request, 'myapi/visualize_list.html')


class BaseVisualizeView(TemplateView):
    template_name = 'myapi/visualize.html'
    strategy_class: VisualizeStrategy = None

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        if self.strategy_class:
            chart = self.strategy_class.get_chart()
            context['chart'] = chart or "Chart is unavailable"
        return context

class GenderView(BaseVisualizeView):
    strategy_class = GenderStrategy

class AgeView(BaseVisualizeView):
    strategy_class = AgeStrategy

class HeightView(BaseVisualizeView):
    strategy_class = HeightStrategy

class WeightView(BaseVisualizeView):
    strategy_class = WeightStrategy

# class SleepView(TemplateView):
#     template_name = 'myapi/sleep_visualize.html'

#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)

#         if 'person_id' in context:
#             sleep_time_chart = SleepTimeStrategy.get_chart_by_id(context['person_id'])
#             context['sleep_time_chart'] = sleep_time_chart or "Sleep Time Chart is unavailable"

#             sleep_duration_chart = SleepDurationStrategy.get_chart_by_id(context['person_id'])
#             context['sleep_duration_chart'] = sleep_duration_chart or "Sleep Duration Chart is unavailable"

#             sleep_score_chart = SleepScoreStrategy.get_chart_by_id(context['person_id'])
#             context['sleep_score_chart'] = sleep_score_chart or "Sleep Score Chart is unavailable"
#         return context

# TODO Fix bugs
class SleepView(View):
    template_name = 'myapi/sleep_visualize.html'

    def get(self, request, *args, **kwargs):
        if "person_id" not in self.kwargs:
            return render(request, self.template_name)
        
        person_id = self.kwargs["person_id"]
        sleep_time_chart = SleepTimeStrategy.get_chart_by_id(person_id) or "Sleep Time Chart is unavailable"
        sleep_duration_chart = SleepDurationStrategy.get_chart_by_id(person_id) or "Sleep Duration Chart is unavailable"
        sleep_score_chart = SleepScoreStrategy.get_chart_by_id(person_id) or "Sleep Score Chart is unavailable"

        context = {
            'person_id': person_id,
            'sleep_time_chart': sleep_time_chart,
            'sleep_duration_chart': sleep_duration_chart,
            'sleep_score_chart': sleep_score_chart,
        }

        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        person_id = request.POST.get("person_id")
        # print(person_id)

        return redirect('sleep-detail', person_id=person_id)