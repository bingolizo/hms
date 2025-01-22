from django.db import models

class Appointment(models.Model):
    patient_id = models.IntegerField()  # Store the patient's ID
    doctor_name = models.CharField(max_length=100)
    appointment_date = models.DateTimeField()

    def __str__(self):
        return f"Appointment with {self.doctor_name} on {self.appointment_date}"

