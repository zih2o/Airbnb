from rest_framework.test import APITestCase
from . import models
from users.models import User


class TestAmenities(APITestCase):
    URL = "/api/v1/rooms/amenities/"
    NAME = "Amenity name"
    DESC = "Amenity desc"

    def setUp(self):
        models.Amenity.objects.create(
            name=self.NAME,
            description=self.DESC,
        )

        user = User.objects.create(username="test")
        self.user = user

    def test_get_amenities(self):
        response = self.client.get(self.URL)
        data = response.json()
        self.assertEqual(
            response.status_code,
            200,
            "The status code isn't 200.",
        )
        self.assertIsInstance(
            data,
            list,
            "The data isn't list.",
        )
        self.assertEqual(
            data[0]["name"],
            self.NAME,
            "Amenity name is wrong.",
        )
        self.assertEqual(
            data[0]["description"],
            self.DESC,
            "Amenity desc is wrong.",
        )

    def test_post_amenity(self):
        NEW_AMENITY_NAME = "New Amenity name"
        NEW_AMENITY_DESC = "New Amenity desc"
        response = self.client.post(self.URL)

        self.assertEqual(
            response.status_code,
            403,
            "The status code isn't 403.",
        )

        self.client.force_login(self.user)
        response = self.client.post(
            self.URL,
            data={
                "name": NEW_AMENITY_NAME,
                "description": NEW_AMENITY_DESC,
            },
        )
        data = response.json()
        self.assertEqual(
            response.status_code,
            200,
            "The status code isn't 200.",
        )
        self.assertEqual(
            data["name"],
            NEW_AMENITY_NAME,
            "Amenity name is different.",
        )
        self.assertEqual(
            data["description"],
            NEW_AMENITY_DESC,
            "Amenity description is different.",
        )

        response = self.client.post(self.URL)
        self.assertEqual(
            response.status_code,
            400,
            "The status code isn't 400.",
        )
        self.assertIn("name", response.json())

        response = self.client.post(
            self.URL,
            data={
                "name": """Lorem ipsum dolor sit amet,
                consectetur adipiscing elit. Aenean placerat
                consequat volutpat. Suspendisse tellus est, pharetra
                et dui vel, lobortis laoreet duis."""
            },
        )
        self.assertEqual(
            response.status_code,
            400,
            "The status code isn't 400.",
        )
        self.assertIn("name", response.json())


class TestAmenity(APITestCase):
    URL = "/api/v1/rooms/amenities/"
    NAME = "Amenity name"
    DESC = "Amenity desc"

    def setUp(self):
        models.Amenity.objects.create(
            name=self.NAME,
            description=self.DESC,
        )

        user = User.objects.create(username="test")
        self.user = user

    def test_amenity_not_found(self):
        response = self.client.get(self.URL + "2")
        self.assertEqual(
            response.status_code,
            404,
            "NotFound is malfunctioning.",
        )

    def test_get_amenity(self):
        response = self.client.get(self.URL + "1")
        data = response.json()

        self.assertEqual(
            response.status_code,
            200,
            "The status code isn't 200.",
        )
        self.assertEqual(
            data["name"],
            self.NAME,
            "Amenity name is not equal.",
        )
        self.assertEqual(
            data["description"],
            self.DESC,
            "Amenity desc is not equal.",
        )

    def test_put_amenity(self):
        NEW_NAME = "New amenity name"
        NEW_DESC = "New amenity desc"

        response = self.client.post(self.URL + "1")

        self.assertEqual(
            response.status_code,
            403,
            "The status code isn't 403.",
        )

        self.client.force_login(self.user)

        response = self.client.put(
            self.URL + "1",
            data={
                "name": NEW_NAME,
                "description": NEW_DESC,
            },
        )
        data = response.json()

        self.assertEqual(
            response.status_code,
            200,
            "The status code isn't 200.",
        )
        self.assertEqual(
            data["name"],
            NEW_NAME,
            "Changed name isn't equal.",
        )
        self.assertEqual(
            data["description"],
            NEW_DESC,
            "Changed desc isn't equal.",
        )

        response = self.client.put(
            self.URL + "1",
            data={
                "name": """Lorem ipsum dolor sit amet, consectetur adipiscing
                elit. Aenean placerat consequat volutpat. Suspendisse tellus
                est, pharetra et dui vel, lobortis laoreet duis.""",
                "description": """Lorem ipsum dolor sit amet,
                consectetur adipiscing elit.
                Aenean placerat consequat volutpat. Suspendisse tellus est,
                pharetra et dui vel, lobortis laoreet duis.""",
            },
        )
        data = response.json()

        self.assertEqual(
            response.status_code,
            400,
            "The status code isn't 400.",
        )
        self.assertIn("name", data)
        self.assertIn("description", data)

    def test_delete_amenity(self):
        response = self.client.post(self.URL + "1")

        self.assertEqual(
            response.status_code,
            403,
            "The status code isn't 403.",
        )

        self.client.force_login(self.user)
        response = self.client.delete(self.URL + "1")
        self.assertEqual(
            response.status_code,
            204,
            "The status code isn't 204.",
        )
