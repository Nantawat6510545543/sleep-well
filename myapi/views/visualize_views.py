from django.shortcuts import redirect, render
from django.views.generic import View, TemplateView

from myapi.chart_utils import *


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


class SleepView(View):
    template_name = 'myapi/sleep_visualize.html'

    def get(self, request, *args, **kwargs):
        person_id = self.kwargs.get("person_id")

        if not person_id:
            return render(request, self.template_name)

        every_person_id = Person.objects.values_list("person_id", flat=True)
        person_has_sleep = Sleep.objects.filter(person_id=person_id).exists()

        if (person_id in every_person_id) and person_has_sleep:
            sleep_time_chart = SleepTimeStrategy.get_chart_by_id(person_id)
            sleep_duration_chart = SleepDurationStrategy.get_chart_by_id(person_id)
            sleep_score_chart = SleepScoreStrategy.get_chart_by_id(person_id)
        else:
            sleep_time_chart = "Sleep Time Chart is unavailable"
            sleep_duration_chart = "Sleep Duration Chart is unavailable"
            sleep_score_chart = "Sleep Score Chart is unavailable"

        context = {
            'person_id': person_id,
            'sleep_time_chart': sleep_time_chart,
            'sleep_duration_chart': sleep_duration_chart,
            'sleep_score_chart': sleep_score_chart,
        }

        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        return redirect('sleep-detail', person_id=request.POST.get("person_id"))