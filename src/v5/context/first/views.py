from django.shortcuts import render
from django.views.generic import TemplateView, ListView, FormView, DetailView

from . import signals
from . import models
from . import forms


class Index(ListView):
   model = models.TemporalInput


class InputDetailView(DetailView):
    model = models.TemporalInput


class InputFormView(FormView):
    form_class = forms.TemporalInputForm
    success_url = '/'
    template_name = 'first/form.html'

    def form_valid(self, form):
        print('Saving form')
        self.object = form.save(commit=False)
        signals.pre_save_input.send(sender=self.object.__class__, instance=self.object)
        self.object.save()
        signals.post_save_input.send(sender=self.object.__class__, instance=self.object)
        return super().form_valid(form)
