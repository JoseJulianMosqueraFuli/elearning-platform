# tests/test_views.py

from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User

from courses.models import Course, Module


class StudentRegistrationViewTest(TestCase):
    def setUp(self):
        self.url = reverse("student_registration")

    def test_get_registration_page(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "students/student/registration.html")

    def test_valid_registration(self):
        data = {
            "username": "testuser",
            "password1": "testpass123",
            "password2": "testpass123",
        }
        response = self.client.post(self.url, data)
        self.assertRedirects(response, reverse("student_course_registration"))
        self.assertTrue(User.objects.filter(username="testuser").exists())


class StudentEnrollCourseViewTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser", password="testpass123"
        )
        self.course = Course.objects.create(title="Test Course", owner=self.user)
        self.url = reverse("student_enroll_course")

    def test_enroll_course(self):
        self.client.login(username="testuser", password="testpass123")

        data = {"course": self.course.id}
        response = self.client.post(self.url, data)

        self.assertRedirects(
            response, reverse("student_course_detail", args=[self.course.id])
        )
        self.assertIn(self.user, self.course.students.all())


class StudentCourseListViewTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser", password="testpass123"
        )
        self.course1 = Course.objects.create(title="Course 1", owner=self.user)
        self.course2 = Course.objects.create(title="Course 2", owner=self.user)
        self.course1.students.add(self.user)

    def test_course_list(self):
        self.client.login(username="testuser", password="testpass123")
        url = reverse("student_course_list")
        response = self.client.get(url)

        self.assertContains(response, self.course1.title)
        self.assertNotContains(response, self.course2.title)


class StudentCourseDetailViewTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser", password="testpass123"
        )
        self.course = Course.objects.create(title="Test Course", owner=self.user)
        self.module = Module.objects.create(title="Test Module", course=self.course)
        self.course.students.add(self.user)

    def test_course_detail(self):
        self.client.login(username="testuser", password="testpass123")
        url = reverse("student_course_detail", args=[self.course.id])
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.course.title)
        self.assertContains(response, self.module.title)
