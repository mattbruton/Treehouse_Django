from django.test import TestCase
from django.utils import timezone
from django.core.urlresolvers import reverse

from .models import Course, Step

# Create your tests here.


class CourseModelTests(TestCase):

    def setUp(self):
        self.course = Course.objects.create(
            title='Python Testing',
            description='Learn to write tests in python'
        )
        self.course2 = Course.objects.create(
            title='Python Regular Expressions',
            description='Learn to write regular expressions in Python'
        )
        self.step = Step.objects.create(
            title="Tests Intro",
            description="Here is why you should test",
            course=self.course
        )

    def test_course_creation(self):
        now = timezone.now()
        self.assertLess(self.course.created_at, now)

    def test_step_creation(self):
        self.assertIs(self.course, self.step.course)


class CourseViewsTests(TestCase):

    def setUp(self):
        self.course = Course.objects.create(
            title='Python Testing',
            description='Learn to write tests in python'
        )
        self.course2 = Course.objects.create(
            title='Python Regular Expressions',
            description='Learn to write regular expressions in Python'
        )
        self.step = Step.objects.create(
            title="Tests Intro",
            description="Here is why you should test",
            course=self.course
        )

    def test_course_list_view(self):
        resp = self.client.get(reverse('courses:list'))
        self.assertEqual(resp.status_code, 200)
        # check for all test courses in list
        self.assertIn(self.course, resp.context['courses'])
        self.assertIn(self.course2, resp.context['courses'])
        # check correct templates used for list view
        self.assertTemplateUsed(resp, 'courses/course_list.html')
        self.assertTemplateUsed(resp, 'layout.html')
        self.assertContains(resp, self.course.title)
