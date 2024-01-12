from django.shortcuts import render
from django.urls import reverse
from django.views import View
from django.views.generic import DetailView, FormView, CreateView
from django.views.generic.base import TemplateResponseMixin, TemplateView
from django.views.generic.detail import SingleObjectMixin

from . import models
from . import forms


def details_view(request, id: int):
    pass


class VehicleDetailView(DetailView):
    model = models.Vehicle
    context_object_name = "vehicle"
    template_name = "main/vehicle_detail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context["open_defects"] = context["vehicle"].defect_set.filter(
            status=models.Defect.DefectStatus.OPEN
        )

        if "defect_form" not in context:
            context["defect_form"] = forms.DefectForm()

        return context

    def post(self, request, *args, **kwargs):
        defect_form = forms.DefectForm(request.POST)
        self.object = self.get_object()
        defect_form.instance.vehicle = self.object
        if defect_form.is_valid():
            defect_form.save()
            return self.render_to_response(self.get_context_data(defect_created=True))
        else:
            return self.render_to_response(
                self.get_context_data(defect_form=defect_form)
            )
