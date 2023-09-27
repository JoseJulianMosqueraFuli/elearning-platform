from typing import Any
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.db.models.query import QuerySet
from django.shortcuts import render
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy

from .models import Course


class ManageCourseListView(ListView):
    model = Course
    template_name = "courses/manage/course/list.html"

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


class OwnerCourseMixin(OwnerMixin, LoginRequiredMixin, PermissionRequiredMixin):
    model = Course
    field = ["subject", "title", "slug", "overview"]
    success_url = reverse_lazy("manage_course_list")


class OwnerCourseEditMixin(OwnerCourseMixin, OwnerEditMixin):
    template_name = "courses/manage/course/form.html"


class ManageCourseListView(OwnerCourseMixin, ListView):
    template_name = "courses/manage/course/list.html"
    permission_required = "courses.view_course"


class CourseCreateView(OwnerCourseEditMixin, CreateView):
    permission_required = "courses.add_course"


class CourseUpdateView(OwnerCourseEditMixin, UpdateView):
    permission_required = "courses.change_course"


class CourseDeleteView(OwnerCourseMixin, DeleteView):
    template_name = "courses/manage/course/delete.html"
    permission_required = "courses.delete_course"
