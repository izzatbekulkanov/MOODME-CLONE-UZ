from datetime import time, datetime

import pytest
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import Client
from django.test.client import BOUNDARY, MULTIPART_CONTENT, encode_multipart  # noqa
from rest_framework import status
from rest_framework.reverse import reverse

from core.settings import MEDIA_ROOT
from groups.models import Course, Branch, Company
from shared.tests import TestBaseFixture


@pytest.mark.django_db
class TestBranchModelViewSet(TestBaseFixture):
    keys = {'name'}

    def test_list_branch(self, client: Client, branch):
        url = '%s?company=%s' % (reverse('branch-list'), branch.company.pk)
        response = client.get(url)

        assert response.data['count'] == Branch.objects.count()
        assert response.status_code == status.HTTP_200_OK
        item = response.data['results'][0]
        assert len(self.keys.difference(set(item))) == 0  # noqa
        assert item['name'] == branch.name

    def test_create_branch(self, client: Client, branch):
        url = '%s?company=%s' % (reverse('branch-list'), branch.company.id)
        image_path = MEDIA_ROOT + '/test.png'
        image = SimpleUploadedFile('test.png', content=open(image_path, 'rb').read(), content_type='image/jpeg')
        data = {
            'name': branch.name,
            'address': branch.address,
            'phone': '987654321',
            'about': branch.about,
            'company': branch.company.pk,
            'image': image
        }
        previous_count = Branch.objects.count()
        response = client.post(url, data)

        assert len(self.keys.difference(set(response.json()))) == 0
        assert response.status_code == status.HTTP_201_CREATED
        assert previous_count + 1 == Branch.objects.count()

        item = response.json()
        keys = ('name', 'address', 'phone', 'about', 'company')
        for key in keys:
            assert item[key] == data[key]

    def test_retrieve_branch(self, client: Client, branch):
        url = '%s?company=%s' % (reverse('branch-detail', args=[branch.id]), branch.company.id)
        response = client.get(url)

        assert len(self.keys.difference(set(response.json()))) == 0
        assert response.status_code == status.HTTP_200_OK

        item = response.data
        assert item['name'] == branch.name
        assert item['address'] == branch.address
        assert item['phone'] == branch.phone
        assert item['about'] == branch.about
        assert item['company'] == branch.company.pk

    def test_update_branch(self, client: Client, branch):
        url = '%s?company=%s' % (reverse('branch-detail', args=[branch.id]), branch.company.id)
        data = {
            'name': 'New updated Branch 1',
            'address': 'test_address',
            'phone': '11111111',
            'about': branch.about,
            'company': branch.company.pk,
            'image': branch.image,
        }
        response = client.put(url, encode_multipart(BOUNDARY, data), MULTIPART_CONTENT)

        assert len(self.keys.difference(set(response.json()))) == 0
        assert response.status_code == status.HTTP_200_OK

        item = response.data
        assert item['name'] == data['name']
        assert item['address'] == data['address']
        assert item['phone'] == data['phone']
        assert item['about'] == data['about']
        assert item['company'] == data['company']

    def test_delete_branch(self, client: Client, branch):
        url = '%s?company=%s' % (reverse('branch-detail', args=[branch.id]), branch.company.id)
        previous_count = Branch.objects.count()
        response = client.delete(url)

        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert previous_count - 1 == Branch.objects.count()


@pytest.mark.django_db
class TestHomeListAPIViewSet(TestBaseFixture):

    def test_list_home(self, client: Client, course):
        url = reverse('home')
        response = client.get(url)

        assert response.data['count'] == Course.objects.count()
        assert response.status_code == status.HTTP_200_OK

        keys = {'name', 'price', 'description', 'lesson_duration', 'course_duration', 'company'}
        item = response.data['results'][0]

        assert len(keys.difference(set(item))) == 0  # noqa
        assert item['name'] == course.name
        assert float(item['price']) == course.price  # problem , decimal 2 ta nol qoshilib qolib qolyapti
        assert item['description'] == course.description
        assert item['lesson_duration'] == course.lesson_duration
        assert item['course_duration'] == course.course_duration
        assert item['company'] == course.company.pk


@pytest.mark.django_db
class TestCompanyModelViewSet(TestBaseFixture):

    def test_list_company(self, client: Client, user, company, ):
        client.force_login(user)
        url = reverse('company-list')
        response = client.get(url)

        assert response.status_code == status.HTTP_200_OK
        assert response.data['count'] == Company.objects.count()

        item = response.data['results'][0]
        assert item['name'] == company.name

    def test_create_company(self, client: Client, company, user):
        client.force_login(user)
        url = reverse('company-list')
        image_path = MEDIA_ROOT + '/test.png'
        image = SimpleUploadedFile('test.png', content=open(image_path, 'rb').read(), content_type='image/jpeg')
        file_path = MEDIA_ROOT + '/test'
        file = SimpleUploadedFile('test', content=open(file_path, 'rb').read(), content_type='file/txt')
        data = {
            'name': 'PDP',
            'logo': image,
            'colors': Company.ColorChoice.RED,
            'start_working_time': str(time(hour=9, minute=00)),
            'end_working_time': str(time(hour=12, minute=00)),
            'phone': '991212334',
            'company_oferta': file
        }
        previous_count = Company.objects.count()

        response = client.post(url, data)

        assert response.status_code == status.HTTP_201_CREATED
        assert previous_count + 1 == Company.objects.count()
        assert datetime.strptime(data['start_working_time'], '%H:%M:%S').strftime('%H:%M:%S') == response.data[
            'start_working_time']
        assert datetime.strptime(data['end_working_time'], '%H:%M:%S').strftime('%H:%M:%S') == response.data[
            'end_working_time']

        item = response.json()
        keys = {'name', 'colors', 'start_working_time', 'end_working_time', 'phone'}

        assert len(keys.difference(set(response.json()))) == 0
        for key in keys:
            assert item[key] == data[key]

    def test_retrieve_company(self, client: Client, company, user):
        client.force_login(user)
        url = reverse('company-detail', args=(company.id,))
        response = client.get(url)

        assert response.status_code == status.HTTP_200_OK

        item = response.json()
        assert item['name'] == company.name

    def test_update_company(self, client: Client, company, user):
        client.force_login(user)
        url = reverse('company-detail', args=(company.id,))
        image_path = MEDIA_ROOT + '/test.png'
        image = SimpleUploadedFile('test.png', content=open(image_path, 'rb').read(), content_type='image/jpeg')
        file_path = MEDIA_ROOT + '/test'
        file = SimpleUploadedFile('test', content=open(file_path, 'rb').read(), content_type='file/txt')
        data = {
            'name': 'PDP',
            'logo': image,
            'colors': Company.ColorChoice.RED,
            'start_working_time': str(time(hour=9, minute=00)),
            'end_working_time': str(time(hour=12, minute=00)),
            'phone': '991212334',
            'company_oferta': file  # noqa
        }
        response = client.put(url, encode_multipart(BOUNDARY, data), MULTIPART_CONTENT)
        assert response.status_code == status.HTTP_200_OK

        item = response.json()
        keys = {'name', 'colors', 'start_working_time', 'end_working_time', 'phone'}

        assert len(keys.difference(set(response.json()))) == 0
        # assert time.strftime(data['start_working_time'], '%H:%M:%S')
        # assert time.strftime(data['end_working_time'], '%H:%M:%S')
        for key in keys:
            assert item[key] == data[key]

    def test_delete_company(self, client: Client, company, user):
        client.force_login(user)
        url = reverse('company-detail', args=(company.id,))
        previous_count = Company.objects.count()
        response = client.delete(url)

        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert previous_count - 1 == Company.objects.count()
