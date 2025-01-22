from django.shortcuts import render

from rest_framework import viewsets, status
from rest_framework.response import Response
from .models import Appointment
from .serializers import AppointmentSerializer
import pika
import json
import jwt  # For token verification
from django.conf import settings

class AppointmentViewSet(viewsets.ModelViewSet):
    queryset = Appointment.objects.all()
    serializer_class = AppointmentSerializer

    def create(self, request):
        token = request.META.get('HTTP_AUTHORIZATION')
        if not self.verify_token(token):
            return Response({'error': 'Invalid token'}, status=status.HTTP_401_UNAUTHORIZED)

        serializer = AppointmentSerializer(data=request.data)
        if serializer.is_valid():
            appointment = serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk=None):
        token = request.META.get('HTTP_AUTHORIZATION')
        if not self.verify_token(token):
            return Response({'error': 'Invalid token'}, status=status.HTTP_401_UNAUTHORIZED)

        try:
            appointment = self.get_object()
            appointment.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Appointment.DoesNotExist:
            return Response({'error': 'Appointment not found'}, status=status.HTTP_404_NOT_FOUND)

    def verify_token(self, token):
        if not token:
            return False
        try:
            # Assuming you have a secret key for JWT
            payload = jwt.decode(token.split()[1], settings.SECRET_KEY, algorithms=["HS256"])
            return True
        except (jwt.ExpiredSignatureError, jwt.InvalidTokenError):
            return False
