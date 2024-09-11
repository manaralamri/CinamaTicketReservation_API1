#interpreter between views and models 
from rest_framework import serializers
from tickets.models import Guest, Movie, Resrvation, Post

class MovieSerializers(serializers.ModelSerializer):
   class Meta:
      model = Movie
      fields= '__all__'

class ResrvationSerializers(serializers.ModelSerializer) :
   class Meta:
      model = Resrvation
      fields= '__all__'   


class GuestSerializers(serializers.ModelSerializer):
   class Meta:
      model = Guest
      fields = ['pk','resrvation', 'name','mobile'] #pk لو نستخدم مشروع الحقيقي نستخدم هذة بدل من uuid or slug 

class PostSerializers(serializers.ModelSerializer):
   class Meta:
     model = Post
     fields =' __all__'