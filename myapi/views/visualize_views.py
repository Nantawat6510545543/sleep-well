from django.shortcuts import render
from django.views.generic import TemplateView

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

class SleepAnalyticsView(BaseVisualizeView):
    strategy_class = SleepAnalyticsStrategy

class TempCView(BaseVisualizeView):
    strategy_class = TempCStrategy

class ConditionTextView(BaseVisualizeView):
    strategy_class = ConditionTextStrategy

class PrecipMMView(BaseVisualizeView):
    strategy_class = PrecipMMStrategy

class HumidityView(BaseVisualizeView):
    strategy_class = HumidityStrategy

class NoiseView(BaseVisualizeView):
    strategy_class = NoiseStrategy

class SleepDurationVSSleepScoreView(BaseVisualizeView):
    strategy_class = SleepDurationVSSleepScoreStrategy

class SleepView(TemplateView):
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
            'sleep_time_chart': sleep_time_chart,
            'sleep_duration_chart': sleep_duration_chart,
            'sleep_score_chart': sleep_score_chart,
        }

        return render(request, self.template_name, context)
