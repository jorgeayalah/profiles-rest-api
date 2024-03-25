from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status #for using the HTTP codes
from rest_framework import viewsets
from rest_framework.authentication import TokenAuthentication
from rest_framework import filters
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.settings import api_settings
# from rest_framework.permissions import IsAuthenticatedOrReadOnly #to prevent non owners to edit others items
from rest_framework.permissions import IsAuthenticated #to prevent non registered users to see the app


from profiles_api import serializers
from profiles_api import models
from profiles_api import permissions

# When to use an APIView?
# - Need full control over the logic
# - Processing files and rendering a synchronous response
# - Calling other APIs
# - Working with local files

class HelloApiView(APIView):
    """Test API View"""
    serializer_class = serializers.HelloSerializer

    def get(self, request, format=None):
        """Returns a list of APIView features"""
        an_apiview = [
            'Uses HTTP methods as functions (get, post, patch, put, delete)',
            'Is similar to a traditional Django View',
            'Gives you the most control over your application logic',
            'Is mapped manually to URLs',
        ]

        #   The response is a JSON object that converts from a list or a dictionary
        return Response({'message': 'Hello', 'an_apiview': an_apiview})

    def post(self, request):
        """Create a hello message witho our name"""
        serializer = self.serializer_class(data=request.data)

        #   since django serializer makes sure the inputs are valid we can do the following
        if serializer.is_valid():
            name = serializer.validated_data.get('name')
            message = f'Hello {name}'
            return Response({'message': message})
        else:
            #   it is a good practice to return the codes of what went wrong to debug
            return Response(
                serializer.errors, 
                status=status.HTTP_400_BAD_REQUEST  # instead of just 400 so we can see what the request means
                )
        
    def put(self, request, pk=None):
        """Handle updating (replacing) an entire object"""
        # when using put, you typically do it to a specific url primary key, thats why is in the parameters
        return Response({'method': 'PUT'})

    def patch(self, request, pk=None):
        """Hanfle a partial update of an object"""
        # to only update the fields provided in the request, uses Raw data as input to privide a JSON dict
        return Response({'method': 'PATCH'})

    def delete(self, request, pk=None):
        """Deletes an object"""
        return Response({'method': 'DELETE'})


# When to use ViewSets?
# - A simple CRUD interface to your database
# - A quick and simple API
# - Little to no customizatio on the logic

class HelloViewSet(viewsets.ViewSet):
    """Test API ViewSet"""
    # we add actions that represents actions on a typical API
    serializer_class = serializers.HelloSerializer

    def list(self, request):
        """Return a hello message"""
        a_viewset = [
            'Uses actions (lsit, create, retrieve, update, partial_update)',
            'Automatically maps to URLs using Routers',
            'Provides more functionality with less code',
        ]

        return Response({'message': 'Hello!', 'a_viewset': a_viewset})
    
    def create(self, request):
        """Create a new hello message"""
        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():
            name = serializer.validated_data.get('name')
            message = f'Hello {name}'
            return Response({'message': message})
        else:
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )
        
    def retrieve(self, request, pk=None):
        """Handles getting an object by its ID"""
        return Response({'http_method': 'GET'})
    
    def update(self, request, pk=None):
        """Handles updating an object"""
        return Response({'http_method': 'PUT'})
    
    def partial_update(self, request, pk=None):
        """Handles updating part of an update"""
        return Response({'http_method': 'PATCH'})
    
    def destroy(self, request, pk=None):
        """Handles removing an  object"""
        return Response({'http_method': 'DELETE'})


#   Theres a difference between using ViewSet and ModelViewSet, the second already has many funcionalities for working with models
class UserProfileViewSet(viewsets.ModelViewSet):
    """Handles creating and updating profiles"""
    serializer_class = serializers.UserProfileSerializer
    queryset = models.UserProfile.objects.all()
    authentication_classes = (TokenAuthentication, )    # Must be a tuple
    permission_classes = (permissions.UpdateOwnProfile, )
    filter_backends = (filters.SearchFilter, )
    search_fields = ('name', 'email', )


class UserLoginApiView(ObtainAuthToken):
    """Handles creating user authentication token"""
    renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES


class UserProfileFeedViewSet(viewsets.ModelViewSet):
    """Handles creating, reading and updating profile feed items"""
    authentication_classes = (TokenAuthentication, )
    serializer_class = serializers.ProfileFeedItemSerializer
    queryset = models.ProfileFeedItem.objects.all()
    permission_classes = (
        permissions.UpdateOwnStatus, 
        # IsAuthenticatedOrReadOnly,    # check imports
        IsAuthenticated
    )

    def perform_create(self, serializer):
        """Sets the user profile to the logged in user"""
        # the perform create function is a Django Rest F that allows us to override the behavior for creating objects through a ModelViewSet
        serializer.save(user_profile=self.request.user) # since its already authenticated


