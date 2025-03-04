from rest_framework.exceptions import ValidationError

class Serializer:
    """Class to handle serialization
    """
    @staticmethod
    def validate_serializer(serializer):
        """Validate the serializer"""
        if not serializer:
            raise ValidationError({"error": "Serializer is missing or empty"})

        serializer.is_valid(raise_exception=True)
        return serializer
    @staticmethod
    def serialize_data(serializer_class, request):
        """Serialize the data and validate it"""
        serializer = serializer_class(data=request.data)
        return serializer
    

