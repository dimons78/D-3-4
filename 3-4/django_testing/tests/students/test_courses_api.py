import pytest

import random

from django.urls import reverse
from rest_framework.status import HTTP_200_OK, HTTP_201_CREATED, HTTP_204_NO_CONTENT

from students.models import Course



def test_example():
    assert False, "Just test example"

# 1_проверка получения 1го курса (retrieve-логика)
@pytest.mark.django_db
def test_courses_retrieve(courses_factory, api_client):

    course = courses_factory()

    url = reverse('courses-detail', args=(course.id,))
    resp = api_client.get(url)
    resp_json = resp.json()

    assert resp.status_code == HTTP_200_OK
    assert course.name == resp_json['name']


# 2_проверка получения списка курсов (list-логика)
@pytest.mark.django_db
def test_courses_list(courses_factory, api_client):

    courses_factory(_quantity=11)
    url = reverse('courses-list')
    resp = api_client.get(url)
    resp_json = resp.json()

    assert resp.status_code == HTTP_200_OK
    assert len(resp_json) == 11


# 3_проверка фильтрации списка курсов по id
@pytest.mark.django_db
def test_courses_id_filter(courses_factory, api_client):

    courses_factory(_quantity=7)
    names = Course.objects.all()

    id_set = set()
    for name in names:
        id_set.add(name.id)

    id = random.sample(id_set, 1)[0]
    data = {'id': id}
    url = reverse('courses-list')

    resp = api_client.get(url, data=data)
    resp_json = resp.json()

    assert resp.status_code == HTTP_200_OK
    assert resp_json[0]['id'] == id

# 4_проверка фильтрации списка курсов по name
@pytest.mark.django_db
def test_courses_name_filter(courses_factory, api_client):

    for i in range(8):
        courses_factory(name=f'Course {i}')

    name = 'Course 7'
    data = {'name': name}
    url = reverse('courses-list')
    resp = api_client.get(url, data=data)
    resp_json = resp.json()

    assert resp.status_code == HTTP_200_OK
    assert resp_json[0]['name'] == name


# 5_тест успешного создания курса
@pytest.mark.django_db
def test_courses_create(api_client):

    url = reverse('courses-list')
    name = 'Sample course'
    data = {'name': name}
    resp = api_client.post(url, data=data)
    resp_json = resp.json()

    assert resp.status_code == HTTP_201_CREATED
    assert resp_json['name'] == name

# 6_тест успешного обновления курса
@pytest.mark.django_db
def test_courses_update(courses_factory, api_client):

    course = courses_factory(name='Sample course')
    course_id = course.id

    new_course_name = 'New sample course'
    data = {'name': new_course_name}
    url = reverse('courses-detail', args=(course_id,))
    resp = api_client.put(url, data=data)
    new_course = Course.objects.get(id=course_id)

    assert resp.status_code == HTTP_200_OK
    assert new_course.name == new_course_name

# 7 тест успешного удаления курса
@pytest.mark.django_db
def test_courses_delete(courses_factory, api_client):

    course = courses_factory(name='Sample course')

    url = reverse('courses-detail', args=(course.id,))
    resp = api_client.delete(url)

    assert resp.status_code == HTTP_204_NO_CONTENT
