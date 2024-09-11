from django.shortcuts import render
from django.http.response import JsonResponse
from .models import Guest, Movie, Resrvation, Post
from rest_framework.decorators import api_view
from .serializers import GuestSerializers, MovieSerializers, ResrvationSerializers, PostSerializers
from rest_framework import status, filters
from rest_framework.response import Response
from rest_framework.views import APIView
from django.http import Http404
from rest_framework import generics, mixins, viewsets
from rest_framework.authentication import BasicAuthentication, TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from .permissions import  IsAuthorOrReadOnly

# Create your views here.
#1 without REST and no model query FBV

def no_rest_no_model(request):

    guests = [
      {
        'id':1,
        'Name': 'omar',
        'mobile': 32456,

      },
      {
        'id': 2,
        'name': 'yessan',
        'mobile': 9876,
      }
    ]
    return JsonResponse(guests, safe=False)

 #2 model data default django without rest ///لو بطلع البيانات من قاعدة البيانات
def no_rest_from_model(request):
     data = Guest.objects.all()
     response= {
         'guests': list(data.values('name','mobile'))
     }
     return JsonResponse(response)

# List==GET 
# Create==POST
# pk query = GET 
# updata == PUT
# Delete destroy == Delete

#3 function based views
#3.1 GET  POST
@api_view(['GET', 'POST'])
def FBV_List(request):

    # GET
    if request.method == 'GET':
        guests = Guest.objects.all()
        serializers = GuestSerializers(guests, many= True)#serializers access GuestSerializers from database pocket كواير لست الموجودة فوقها 
        return Response(serializers.data)
    # POST 
    elif request.method == 'POST':
        serializers = GuestSerializers(data= request.data)
        if serializers.is_valid():
            serializers.save()
            return Response(serializers.data, status= status.HTTP_201_CREATED)   
        return Response(serializers.data,status= status.HTTP_400_BAD_REQUEST )    

#3.1 GET  PUT Delete
@api_view(['GET','PUT','DELETE'])
def FBV_pk(request, pk):
    try:
       guest = Guest.objects.get(pk=pk)
    except Guest.DoesNotExitsts:
        return Response(status=status.HTTP_404_NOT_FOUND)   
    # GET
    if request.method == 'GET':
        serializers = GuestSerializers(guest)#serializers access GuestSerializers from databas
        return Response(serializers.data)
    # PUT
    elif request.method == 'PUT':
        serializers = GuestSerializers(guest, data= request.data)
        if serializers.is_valid():
            serializers.save()
            return Response(serializers.data)   
        return Response(serializers.errors,status= status.HTTP_400_BAD_REQUEST )    
        # DELETE
    if request.method == 'DELETE':
        guest.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
  
# CBV Class based views
# 4.1 list and create == GET and POST
class CBV_List(APIView):
    def get(self, request):
        guests = Guest.objects.all()
        serializers = GuestSerializers(guests, many= True)
        return Response(serializers.data)


    def post(self, request):
        serializers = GuestSerializers(data = request.data)
        if serializers.is_valid():
            serializers.save()
            return Response(
                serializers.data,
                status= status.HTTP_201_CREATED
            )
        return Response(
            serializers.data,
            status = status.HTTP_400_BAD_REQUEST
        )       


#   
class CBV_pk(APIView):
    def get_objects(self, pk):
        try:
            return Guest.objects.get(pk=pk)
        except Guest.DoesNotExitsts:
            raise Http404

    def get(self,request, pk):
        guest = self.get_objects(pk)
        serializers = GuestSerializers(guest)
        return Response(serializers.data)

    def put(self,request,pk):
        guest = self.get_objects(pk)
        serializers = GuestSerializers(guest,data= request.data)  
        if serializers.is_valid():
            serializers.save()
            return Response(serializers.data)
        return Response(serializers.errors, status=status.HTTP_400_BAD_REQUEST) 

    def delete(self, request, pk): 
         guest = self.get_objects(pk)
         guest.delete()
         return Response(status=status.HTTP_204_NO_CONTENT) 
             

# Mixins
# 5.1 mixins list 
class mixins_list(mixins.ListModelMixin,mixins.CreateModelMixin,generics.GenericAPIView):
    queryset = Guest.objects.all()
    serializer_class = GuestSerializers
    authentication_classes = [TokenAuthentication]
    #permission_classes = [IsAuthenticated]


    def get(self,request):
        return self.list(request)

    def post(self,request):
        return self.create(request)    
  
# 5.2 mixins get put delete
class mixins_pk(mixins.RetrieveModelMixin, mixins.UpdateModelMixin, mixins.DestroyModelMixin, generics.GenericAPIView):
    queryset= Guest.objects.all()
    serializer_class = GuestSerializers
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    
    def get(self,request,pk):
        return self.retrieve(request)

    def put(self,request,pk):
        return self.updata(request) 
    
    def delete(self,request):
        return self,destroy(request)

# 6 Generics
# 6.1 get and post
class generics_list(generics.ListCreateAPIView):#مايحتاج اسوي فانكشن get , post لانة راح يفهم
    queryset= Guest.objects.all()
    serializer_class = GuestSerializers
    authentication_classes = [TokenAuthentication]
    #permission_classes = [IsAuthenticated]

# 6.2 get put delete
class generics_pk(generics.RetrieveUpdateDestroyAPIView):
    queryset= Guest.objects.all()
    serializer_class = GuestSerializers
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

#7 Viewsets
class viewsets_guest(viewsets.ModelViewSet):
     queryset= Guest.objects.all()
     serializer_class = GuestSerializers

class viewsets_movie(viewsets.ModelViewSet):
      queryset= Movie.objects.all()
      serializer_class = MovieSerializers
      filter_backend = [filters.SearchFilter]
      search_fields = ['movie']

class viewsets_reservation(viewsets.ModelViewSet):
      queryset= Resrvation.objects.all()
      serializer_class = ResrvationSerializers
     
#8 find movie
@api_view(['GET'])# فانكشن نوعها get 
def find_movie(request):#indepont data from request
    movies = Movie.objects.filter(#queray set 
        hall = request.data['hall'],#acss request from data يجيب لي hall
        movie = request.data['movie'],
        

    )
    serializers = MovieSerializers(movies, many= True)# ممكن تكون صح many= True  moviesتخزن فيها قيمة  MovieSerializersتسمح لي بالمرور علىserializersيجيب لي من خلال 
    return Response(serializers.data)


#9 create new reservation
@api_view(['POST'])
def new_reservation(request):
    movie = Movie.objects.get(
         hall = request.data['hall'],#acss request from data يجيب لي hall
         movie = request.data['movie'],
 

    )
    guest = Guest()
    guest.name = request.data['name']
    guest.mobile = request.data['mobile']
    guest.save()

    reservation = Resrvation()#وحدة فاضية للحجز
    reservation.guest = guest
    reservation.movie = movie
    reservation.save()
    
    return Response(status= status.HTTP_201_CREATED)
      
#10 post author editor
class Post_pk(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthorOrReadOnly]
    queryset = Post.objects.all()
    serializer_class = PostSerializers

  

  
  


     

