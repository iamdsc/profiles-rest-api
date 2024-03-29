from django.shortcuts import render
from rest_framework import viewsets, status, filters
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authentication import TokenAuthentication
from . import serializers, models, permissions
from rest_framework.authtoken.serializers import AuthTokenSerializer
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.permissions import IsAuthenticated

# Create your views here.

class HelloApiView(APIView):
    "Test API View."

    serializer_class=serializers.HelloSerializer

    def get(self, request, format=None):
        """Returns a list of APIView features."""
        an_apiview=[
            'Uses HTTP methods as functions (get,post,put,patch, delete)',
            'It is similar to the traditional django view',
            'It gives you most control over your logic',
            'It is mapped manually to URLs'
        ]

        return Response({'message':'Hello!','an_apiview':an_apiview})

    def post(self, request):
        """Create a hello message with our name."""
        serializer=serializers.HelloSerializer(data=request.data)
        if serializer.is_valid():
            name=serializer.data.get('name')
            message='Hello {0}'.format(name)
            return Response({'message':message})
        else:
            return Response(
            serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk=None):
        """Handles updating an object"""
        return Response({'method':'put'})

    def patch(self, request, pk=None):
        """Only updates fields provided in the request"""
        return Response({'method':'patch'})

    def delete(self, request, pk=None):
        """Delete an object"""
        return Response({'method':'delete'})

class HelloViewSet(viewsets.ViewSet):
    """Test API ViewSet."""
    serializer_class=serializers.HelloSerializer
    def list(self, request):
        """Return a hello message."""
        a_viewset=[
            'Uses actions (list,create,update,partial_update,destroy)',
            'Automatically maps to URLs using Routers.',
            'Provides more functionality with less code.'
        ]

        return Response({'message':'Hello!','a_viewset':a_viewset})

    def create(self, request):
        """Create a new Hello message."""
        serializer=serializers.HelloSerializer(data=request.data)
        if serializer.is_valid():
            name=serializer.data.get('name')
            message='Hello {0}'.format(name)
            return Response({'message':message})
        else:
            return Response(
            serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, pk=None):
        """Handles getting an objecct by its id"""
        return Response({'http_method':'GET'})

    def update(self, request, pk=None):
        """Handles updating an object"""
        return Response({'http_method':'PUT'})

    def partial_update(self, request, pk=None):
        """Handles updating part of an object"""
        return Response({'http_method':'PATCH'})

    def destroy(self, request, pk=None):
        """Handles removing an object."""
        return Response({'http_method':'DELETE'})

class UserProfileViewSet(viewsets.ModelViewSet):
    """Handles creating and updating profiles."""
    serializer_class=serializers.UserProfileSerializer
    # tells viewset how to retrieve object from db
    queryset=models.UserProfile.objects.all()
    # contains tuple of authentication types used in API
    authentication_classes = (TokenAuthentication,)
    permission_classes = (permissions.UpdateOwnProfile,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name', 'email',)  # fields to apply filter on

class LoginViewSet(viewsets.ViewSet):
    """Checks email and password and returns an auth token."""
    serializer_class=AuthTokenSerializer

    def create(self, request):
        """Uses the ObtainAuthToken APIView to validate and create a token."""
        return ObtainAuthToken().post(request)

class UserProfileFeedViewSet(viewsets.ModelViewSet):
    """Handles creating, reading and updating profile feed item."""
    authentication_classes=(TokenAuthentication,)
    serializer_class=serializers.ProfileFeedItemSerializer
    queryset=models.ProfileFeedItem.objects.all()
    permission_classes=(permissions.PostOwnStatus, IsAuthenticated,)

    def perform_create(self, serializer):
        """Sets the user profile to the logged in user."""
        serializer.save(user_profile=self.request.user)
