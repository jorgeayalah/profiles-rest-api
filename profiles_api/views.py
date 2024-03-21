from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status #for using the HTTP codes
from rest_framework import viewsets

from profiles_api import serializers

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
        """Handle getting an object by its ID"""
        return Response({'http_method': 'GET'})
    
    def update(self, request, pk=None):
        """Handle updating an object"""
        return Response({'http_method': 'PUT'})
    
    def partial_update(self, request, pk=None):
        """Handle updating part of an update"""
        return Response({'http_method': 'PATCH'})
    
    def destroy(self, request, pk=None):
        """Handle removing an  object"""
        return Response({'http_method': 'DELETE'})
    