import datetime
import json

from django.db import connection
from django.test import override_settings
import six
from rest_framework.test import APITestCase

from tests.models import Cat, Group, Location, Permission, Profile, User
from tests.serializers import NestedEphemeralSerializer, PermissionSerializer
from tests.setup import create_fixture

UNICODE_STRING = six.unichr(9629)  # unicode heart
# UNICODE_URL_STRING = urllib.quote(UNICODE_STRING.encode('utf-8'))
UNICODE_URL_STRING = '%E2%96%9D'


@override_settings(
    DYNAMIC_REST={
        'ENABLE_LINKS': False
    }
)
class Tests(APITestCase):
    
    def setUp(self):
        self.fixture = create_fixture()
        home_id = self.fixture.locations[0].id
        backup_home_id = self.fixture.locations[1].id
        parent = Cat.objects.create(
            name='Parent 1',
            home_id=home_id,
            backup_home_id=backup_home_id
        )
        self.kitten = Cat.objects.create(
            name='Kitten 1',
            home_id=home_id,
            backup_home_id=backup_home_id,
            parent=parent
        )

    def test_put(self):
        parent_id = self.kitten.parent_id
        kitten_name = 'Kitten 1'
        data = {
            'name': kitten_name,
            'home': self.kitten.home_id,
            'backup_home': self.kitten.backup_home_id,
            'parent': parent_id
        }
        response = self.client.put(
            f'/cats2/{self.kitten.id}',
            json.dumps(data),
            content_type='application/json'
        )
        self.assertEqual(200, response.status_code)
        data = json.loads(response.content.decode('utf-8'))
        self.assertEqual(data['cat']['parent']['id'], parent_id)
        self.assertEqual(data['cat']['name'], kitten_name)
