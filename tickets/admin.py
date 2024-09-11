from django.contrib import admin
from .models import Movie, Guest, Resrvation,Post

# Register your models here.
admin.site.register(Movie)
admin.site.register(Guest)
admin.site.register(Resrvation)
admin.site.register(Post)


