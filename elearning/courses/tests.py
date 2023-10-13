from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse

from .models import Course, Module, Content, Subject


class CourseTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser", password="testpassword"
        )

    def test_manage_course_list_view(self):
        self.client.login(username="testuser", password="testpassword")

        Course.objects.create(
            title="Test Course",
            owner=self.user,
        )

        response = self.client.get(reverse("manage_course_list"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Test Course")

    def test_course_create_view(self):
        self.client.login(username="testuser", password="testpassword")

        response = self.client.post(
            reverse("course_create"),
            data={
                "subject": "Test Subject",
                "title": "New Test Course",
                "slug": "new-test-course",
                "overview": "Course overview",
            },
        )

        self.assertEqual(response.status_code, 302)  # 302 significa redirección
        self.assertTrue(Course.objects.filter(title="New Test Course").exists())

    def test_course_update_view(self):
        course = Course.objects.create(
            title="Test Course",
            owner=self.user,
        )

        self.client.login(username="testuser", password="testpassword")

        response = self.client.post(
            reverse("course_update", args=[course.id]),
            data={
                "subject": "Updated Subject",
                "title": "Updated Test Course",
                "slug": "updated-test-course",
                "overview": "Updated Course overview",
            },
        )

        self.assertEqual(response.status_code, 302)
        updated_course = Course.objects.get(id=course.id)
        self.assertEqual(updated_course.title, "Updated Test Course")
        self.assertEqual(updated_course.subject, "Updated Subject")

    def test_course_detail_view(self):
        course = Course.objects.create(
            title="Test Course",
            owner=self.user,
        )

        response = self.client.get(reverse("course_detail", args=[course.id]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Test Course")
