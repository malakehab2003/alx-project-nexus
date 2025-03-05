from ..models import Address
from ..serialzers import AddressSerializer
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status
from ..permissions import isOwnerOrForbidden
from ..utils.authentication import get_user_from_request
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model
from ..utils.validate import validate_args_not_none
from rest_framework.exceptions import ValidationError
from ..utils.serializer import Serializer

User = get_user_model()

class AddressViewSet(viewsets.ModelViewSet):
    """ ViewSet for the Address model """
    serializer_class = AddressSerializer
    queryset = Address.objects.all()
    lookup_field = "id"
    no_auth_actions = []  

    def get_permissions(self):
        """ Allow public access for create, require authentication for others """
        if self.action in self.no_auth_actions:
            return []
        return [IsAuthenticated(), isOwnerOrForbidden]
    

    def create(self, request, *args, **kwargs):
        """Disable POST /api/address/"""
        return Response({"error": "Creating addresses is not allowed"}, status=status.HTTP_403_FORBIDDEN)
    
    def list(self, request, *args, **kwargs):
        """Disable Get /api/address/"""
        return Response({"error": "Listing addresses is not allowed"}, status=status.HTTP_403_FORBIDDEN)
    
    def retrieve(self, request, *args, **kwargs):
        """ list all addresses of the user with id in url """
        user_id = kwargs.get("id")

        addresses = Address.objects.filter(user=user_id)

        user_from_database = get_object_or_404(User, id=user_id)

        self.check_object_permissions(request, user_from_database)

        serializer = self.get_serializer(addresses, many=True)

        return Response(serializer.data)

    @action(detail=True, methods=["post"], url_path="add_address")
    def add_address(self, request, *args, **kwargs):
        """ add address to the user """
        user_id = kwargs.get("id")
        
        user_from_database = get_object_or_404(User, id=user_id)

        self.check_object_permissions(request, user_from_database)

        serializer = Serializer.serialize_data(AddressSerializer, request)

        if Serializer.validate_serializer(serializer):
            serializer.save(user=user_from_database)
            return Response({"message": "Address added successfully", "address": serializer.data}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def check_address_owner_same_token(self, request, **kwargs):
        """
        take the id of the user from the token
        and the id of the user own the address
        check if the same
        """
        address_id = kwargs.get("id")
        user_got_from_token = get_user_from_request(request)["id"]

        try:
            validate_args_not_none(user_got_from_token)
        except ValidationError:
            return None

        address = get_object_or_404(Address, id=address_id)
        user_id_owns_address = address.user.id

        if user_id_owns_address != user_got_from_token:
            return None
        return address

    def update(self, request, *args, **kwargs):
        """ update an address taking the id of it """
        address = self.check_address_owner_same_token(request, **kwargs)

        if not address:
            return Response({"error": "No token"}, status=status.HTTP_400_BAD_REQUEST)

        serializer = self.get_serializer(address, data=request.data, partial=False)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Address updated successfully", "address": serializer.data}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def destroy(self, request, *args, **kwargs):
        """ delete an address using the id """
        address = self.check_address_owner_same_token(request, **kwargs)

        if not address:
            return Response({"error": "No token"}, status=status.HTTP_400_BAD_REQUEST)
        
        address.delete()
        return Response({"message": "Address deleted successfully"}, status=status.HTTP_204_NO_CONTENT)


# fix create
# fix id
# check code
