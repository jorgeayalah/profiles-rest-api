from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status #for using the HTTP codes

from profiles_api import serializers

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

