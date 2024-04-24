from django.shortcuts import render
from django.views.generic import TemplateView

from myapi.models import Person


def index(request):
    return render(request, 'myapi/index.html')


class GenderCountView(TemplateView):
    template_name = 'myapi/gender_visualizer.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['male_count'] = Person.objects.filter(sex='Male').count()
        context['female_count'] = Person.objects.filter(sex='Female').count()
        context['other_count'] = Person.objects.filter(sex='Other').count()
        return context
