import pytest
from model_bakery import baker

from rest_framework.test import APIClient


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def courses_factory():
    def factory(**kwargs):
        course = baker.make('students.Course', **kwargs)
        return course
    return factory


@pytest.fixture
def students_factory():
    def factory(**kwargs):
        student = baker.make('students.Student', **kwargs)
        return student
    return factory

