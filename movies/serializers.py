from rest_framework import serializers
from .models import Movie

class MovieSerializer(serializers.ModelSerializer):
  class Meta:
    fields = ("id", "owner", "name", "description", "created_at")
    model = Movie