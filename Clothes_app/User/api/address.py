from ..models import Address
from ..serialzers import AddressSerializer
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status
from ..utils.authentication import get_user_from_request
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model
from rest_framework.exceptions import ValidationError
from ..utils.serializer import Serializer

User = get_user_model()

class AddressViewSet(viewsets.ModelViewSet):
    """ ViewSet for the Address model """
    serializer_class = AddressSerializer
    lookup_field = "id"
    queryset = Address.objects.all()
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        """ Returns addresses belonging to the authenticated user """
        user_id = get_user_from_request(self.request).get("id")
        if not user_id:
            return Address.objects.none()
        return Address.objects.filter(user_id=user_id)

    def get_object(self):
        """ Ensure user can only access their own address """
        obj = get_object_or_404(Address, id=self.kwargs["id"])
        if obj.user.id != get_user_from_request(self.request).get("id"):
            raise ValidationError({"error": "You do not have permission to access this address"})
        return obj

    def create(self, request, *args, **kwargs):
        """ add address to the user """
        user_id = get_user_from_request(request)["id"]

        if not user_id:
            return Response({"error": "no token added"}, status=status.HTTP_400_BAD_REQUEST)
        
        user_from_database = get_object_or_404(User, id=user_id)

        serializer = Serializer.serialize_data(AddressSerializer, request)

        if Serializer.validate_serializer(serializer):
            serializer.save(user=user_from_database)
            return Response({"message": "Address added successfully", "address": serializer.data}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, *args, **kwargs):
        """ update an address taking the id of it """
        address = self.get_object()

        serializer = self.get_serializer(address, data=request.data, partial=False)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Address updated successfully", "address": serializer.data}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def destroy(self, request, *args, **kwargs):
        """ delete an address using the id """
        address = self.get_object()
        
        address.delete()
        return Response({"message": "Address deleted successfully"}, status=status.HTTP_204_NO_CONTENT)
# fix id
