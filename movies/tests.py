from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from .models import Movie


class MovieTests(APITestCase):
    @classmethod
    def setUpTestData(cls):
        testuser1 = get_user_model().objects.create_user(
            username="testuser1", password="pass"
        )
        testuser1.save()

        test_movie = Movie.objects.create(
            name="inception",
            owner=testuser1,
            description="",
        )
        test_movie.save()

    def test_movies_model(self):
        movie = Movie.objects.get(id=1)
        actual_owner = str(movie.owner)
        actual_name = str(movie.name)
        actual_description = str(movie.description)
        self.assertEqual(actual_owner, "testuser1")
        self.assertEqual(actual_name, "inception")
        self.assertEqual(
            actual_description, ""
        )

    def test_get_movie_list(self):
        url = reverse("movie_list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        movies = response.data
        self.assertEqual(len(movies), 1)
        self.assertEqual(movies[0]["name"], "inception")

    def test_get_movie_by_id(self):
        url = reverse("movie_detail", args=(1,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        movie = response.data
        self.assertEqual(movie["name"], "inception")

    def test_create_movie(self):
        url = reverse("movie_list")
        data = {"owner": 1, "name": "inception2", "description": "awesome", "created_at": "2022-05-26T22:51:34.624349Z", "updated_at": "2022-05-26T22:51:34.624349Z"}
      
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        movies = Movie.objects.all()
        self.assertEqual(len(movies), 2)
        self.assertEqual(Movie.objects.get(id=1).name, "inception")

    def test_update_movie(self):
        url = reverse("movie_detail", args=(1,))
        data = {
            "owner": 1,
            "name": "inception",
            "description": "mind bending",
            "created_at": "2022-05-26T22:51:34.624349Z", "updated_at": "2022-05-26T22:51:34.624349Z"
        }
        response = self.client.put(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        movie = Movie.objects.get(id=1)
        self.assertEqual(movie.name, data["name"])
        self.assertEqual(movie.owner.id, data["owner"])
        self.assertEqual(movie.description, data["description"])

    def test_delete_movie(self):
        url = reverse("movie_detail", args=(1,))
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        movies = Movie.objects.all()
        self.assertEqual(len(movies), 0)
