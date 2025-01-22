from rest_framework import viewsets, status
from rest_framework.response import Response
from .models import Patient
from .serializers import PatientSerializer, LoginSerializer
import pika
import json
from django.contrib.auth.hashers import check_password
import uuid

class PatientViewSet(viewsets.ModelViewSet):
    queryset = Patient.objects.all()
    serializer_class = PatientSerializer

    def perform_create(self, serializer):
        patient = serializer.save()
        self.send_patient_data(patient)

    def send_patient_data(self, patient):
        connection = pika.BlockingConnection(pika.ConnectionParameters('rabbitmq'))
        channel = connection.channel()
        channel.queue_declare(queue='appointment_queue')

        patient_data = {
            'id': patient.id,
            'name': patient.name,
            'email': patient.email,
            'phone': patient.phone
        }
        channel.basic_publish(exchange='', routing_key='appointment_queue', body=json.dumps(patient_data))
        connection.close()

class LoginViewSet(viewsets.ViewSet):
    def create(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            name = serializer.validated_data['name']
            password = serializer.validated_data['password']
            try:
                patient = Patient.objects.get(name=name)
                if check_password(password, patient.password):
                    token = str(uuid.uuid4())  # Generate a token
                    return Response({'token': token}, status=status.HTTP_200_OK)
                return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
            except Patient.DoesNotExist:
                return Response({'error': 'Patient not found'}, status=status.HTTP_404_NOT_FOUND)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
