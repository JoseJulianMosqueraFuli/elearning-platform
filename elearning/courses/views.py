from typing import Any
from django.db.models.query import QuerySet
from django.shortcuts import render
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy

from .models import Course


class ManageCourseListView(ListView):
    model = Course
    template_name = "manage_course_list.html"

    def get_queryset(self) -> QuerySet[Any]:
        query_set = super().get_queryset()
        return query_set.filter(owner=self.request.user)


class OwnerMixin:
    def get_queryset(self):
        query_set = super.get_queryset()
        return query_set.filter(owner=self.request.user)


class OwnerEditMixin:
    def from_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)


class OwnerCourseMixin(OwnerMixin):
    model = Course
    field = ["subject", "title", "slug", "overview"]
    success_url = reverse_lazy("manage_course_list")


class OwnerCourseEditMixin(OwnerCourseMixin, OwnerEditMixin):
    pass


class CourseCreateView(OwnerCourseEditMixin, CreateView):
    pass


class CourseUpdateView(OwnerCourseEditMixin, UpdateView):
    pass


class CourseDeleteView(OwnerCourseMixin, DeleteView):
    pass
