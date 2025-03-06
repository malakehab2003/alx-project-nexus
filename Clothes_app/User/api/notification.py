from rest_framework import viewsets, mixins
from rest_framework.permissions import IsAuthenticated
from ..models import Notification
from ..serialzers import NotificationSerializer
from ..utils.authentication import get_user_from_request


class NotificationViewSet(mixins.ListModelMixin,
                       mixins.RetrieveModelMixin,
                       viewsets.GenericViewSet):
    """ ViewSet for the Notification model """
    serializer_class = NotificationSerializer
    lookup_field = "id"
    queryset = Notification.objects.all()
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """ Returns Notifications belonging to the authenticated user """
        user_id = get_user_from_request(self.request).get("id")
        if not user_id:
            return Notification.objects.none()
        return Notification.objects.filter(user=user_id)  
