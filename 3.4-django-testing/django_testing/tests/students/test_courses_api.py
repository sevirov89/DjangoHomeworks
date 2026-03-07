import pytest
from rest_framework.test import APIClient
from model_bakery import baker
from students.models import Course, Student


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def course_factory():
    def factory(**kwargs):
        return baker.make(Course, **kwargs)

    return factory


@pytest.fixture
def student_factory():
    def factory(**kwargs):
        return baker.make(Student, **kwargs)

    return factory


@pytest.mark.django_db
def test_retrieve_course(api_client, course_factory):
    # Arrange
    course = course_factory(name='Test Course')

    # Act
    response = api_client.get(f'/api/v1/courses/{course.id}/')

    # Assert
    assert response.status_code == 200
    assert response.data['id'] == course.id
    assert response.data['name'] == 'Test Course'


@pytest.mark.django_db
def test_list_courses(api_client, course_factory):
    # Arrange
    courses = course_factory(_quantity=3)

    # Act
    response = api_client.get('/api/v1/courses/')

    # Assert
    assert response.status_code == 200
    assert len(response.data) == 3
    for i, course in enumerate(courses):
        assert response.data[i]['id'] == course.id


@pytest.mark.django_db
def test_filter_courses_by_id(api_client, course_factory):
    # Arrange
    courses = course_factory(_quantity=3)
    target_id = courses[1].id

    # Act
    response = api_client.get('/api/v1/courses/', data={'id': target_id})

    # Assert
    assert response.status_code == 200
    assert len(response.data) == 1
    assert response.data[0]['id'] == target_id


@pytest.mark.django_db
def test_filter_courses_by_name(api_client, course_factory):
    # Arrange
    course_factory(name='Course 1')
    course_factory(name='Course 2')
    target_course = course_factory(name='Target Course')

    # Act
    response = api_client.get('/api/v1/courses/', data={'name': 'Target Course'})

    # Assert
    assert response.status_code == 200
    assert len(response.data) == 1
    assert response.data[0]['id'] == target_course.id
    assert response.data[0]['name'] == 'Target Course'


@pytest.mark.django_db
def test_create_course(api_client):
    # Arrange
    data = {'name': 'New Course'}

    # Act
    response = api_client.post('/api/v1/courses/', data=data)

    # Assert
    assert response.status_code == 201
    assert Course.objects.count() == 1
    assert Course.objects.get().name == 'New Course'


@pytest.mark.django_db
def test_update_course(api_client, course_factory):
    # Arrange
    course = course_factory(name='Old Name')
    data = {'name': 'Updated Name'}

    # Act
    response = api_client.patch(f'/api/v1/courses/{course.id}/', data=data)

    # Assert
    assert response.status_code == 200
    course.refresh_from_db()
    assert course.name == 'Updated Name'


@pytest.mark.django_db
def test_delete_course(api_client, course_factory):
    # Arrange
    course = course_factory()

    # Act
    response = api_client.delete(f'/api/v1/courses/{course.id}/')

    # Assert
    assert response.status_code == 204
    assert Course.objects.count() == 0
