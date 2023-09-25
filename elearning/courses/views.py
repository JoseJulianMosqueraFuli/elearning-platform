from typing import Any
from django.db.models.query import QuerySet
from django.shortcuts import render
from django.views.generic import ListView
from .models import Course


class ManageCourseListView(ListView):
    model = Course
    template_name = "manage_course_list.html"

    def get_queryset(self) -> QuerySet[Any]:
        query_set = super().get_queryset()
        return query_set.filter(owner=self.request.user)
