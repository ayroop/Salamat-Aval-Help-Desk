from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.utils import timezone
from django.core.exceptions import ValidationError
#These are related with OTP
from django.utils import timezone
import datetime
from django.contrib.auth.models import User
from .utils import send_sms_via_farazsms  # Import SMS sending utility

# Define the Department model
class Department(models.Model):
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name

# Define the Center model
class Center(models.Model):
    name = models.CharField(max_length=255, unique=True)
    landline_phone = models.CharField(max_length=15, unique=True)

    def __str__(self):
        return self.name

# Define the ProblemType model
class ProblemType(models.Model):
    type_name = models.CharField(max_length=255, unique=True)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.type_name

# Define the Staff model
class Staff(models.Model):
    name = models.CharField(max_length=255)
    surname = models.CharField(max_length=255)
    email = models.EmailField(unique=True, blank=True, null=True)
    phone_number = models.CharField(max_length=15, unique=True, blank=True, null=True)
    landline_phone = models.CharField(max_length=15, blank=True, null=True)
    landline_extension = models.CharField(max_length=10, blank=True, null=True)
    room_address = models.CharField(max_length=255)
    department = models.ForeignKey(Department, on_delete=models.SET_NULL, null=True, blank=True)
    center = models.ForeignKey(Center, on_delete=models.SET_NULL, null=True, blank=True)
    role = models.CharField(max_length=50, choices=[('staff', 'Staff'), ('admin', 'Admin')])
    date_joined = models.DateField(auto_now_add=True)
    current_request = models.ForeignKey('Problem', on_delete=models.SET_NULL, null=True, blank=True, related_name='current_request_staff')

    def __str__(self):
        return f"{self.name} {self.surname}"

# Define the Expert model
class Expert(models.Model):
    name = models.CharField(max_length=255)
    surname = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=15, unique=True, blank=True, null=True)
    specialization = models.CharField(max_length=255)
    department = models.ForeignKey(Department, on_delete=models.SET_NULL, null=True, blank=True)
    problem_type = models.ForeignKey(ProblemType, on_delete=models.SET_NULL, null=True, blank=True)
    status = models.CharField(max_length=50, choices=[('Available', 'Available'), ('Busy', 'Busy'), ('Unavailable', 'Unavailable')], default='Available')
    current_assignment = models.ForeignKey('Problem', on_delete=models.SET_NULL, null=True, blank=True, related_name='current_assignment_expert')

    def __str__(self):
        return f"{self.name} {self.surname}"

# Define the Problem model
class Problem(models.Model):
    OPEN = 'Open'
    CLOSED = 'Closed'
    IN_PROGRESS = 'In Progress'
    STATUS_CHOICES = [
        (OPEN, 'Open'),
        (CLOSED, 'Closed'),
        (IN_PROGRESS, 'In Progress')
    ]

    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default=OPEN)
    submission_date = models.DateField(auto_now_add=True)
    resolution_date = models.DateField(blank=True, null=True)
    staff = models.ForeignKey(Staff, on_delete=models.SET_NULL, null=True, blank=True, related_name='problems')
    expert = models.ForeignKey(Expert, on_delete=models.SET_NULL, null=True, blank=True)
    problem_type = models.ForeignKey(ProblemType, on_delete=models.SET_NULL, null=True, blank=True)
    admin_notified = models.BooleanField(default=False)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        # Check for new problem and unresolved existing problems for the staff
        if self._state.adding and self.staff:
            unresolved_problems = Problem.objects.filter(staff=self.staff, status__in=[self.OPEN, self.IN_PROGRESS]).exclude(id=self.id)
            if unresolved_problems.exists():
                raise ValidationError("Staff member already has an unresolved problem.")

        # Saving the current state
        super().save(*args, **kwargs)

        # Logic for sending notifications and handling expert assignment
        is_new = self._state.adding
        prev_expert_id = None
        if not is_new:
            prev_problem = Problem.objects.get(pk=self.pk)
            prev_expert_id = prev_problem.expert.id if prev_problem.expert else None

        if is_new:
            # Logic for sending SMS to staff about problem creation
            message = f"Problem created: {self.title}"
            # Implement the send_sms_via_farazsms function
            send_sms_via_farazsms(self.staff.phone_number, message)
        elif self.expert_id and self.expert_id != prev_expert_id:
            # Logic for sending SMS to staff about expert assignment
            message = f"Problem '{self.title}' is assigned to expert {self.expert.name} {self.expert.surname}"
            send_sms_via_farazsms(self.staff.phone_number, message)

            # Logic for sending SMS to expert
            if self.problem_type in self.expert.problem_type.all():
                message = f"New problem assigned: {self.title}"
                send_sms_via_farazsms(self.expert.phone_number, message)

        # Check if more than 1 hour has passed since submission without an expert assignment
        time_elapsed = timezone.now() - self.submission_date
        if time_elapsed.total_seconds() > 3600 and not self.expert and not self.admin_notified:
            try:
                admin = Staff.objects.filter(role='admin').first()
                if admin:
                    message = f"Problem '{self.title}' has not been assigned an expert for over an hour."
                    send_sms_via_farazsms(admin.phone_number, message)
                    self.admin_notified = True
                    self.save(update_fields=['admin_notified'])
            except Staff.DoesNotExist:
                pass  # Handle no admin found or multiple admins

# Define the FileAttachment model
class FileAttachment(models.Model):
    problem = models.ForeignKey(Problem, on_delete=models.CASCADE, related_name='attachments')
    staff = models.ForeignKey(Staff, on_delete=models.SET_NULL, null=True, blank=True)
    file_path = models.FileField(upload_to='attachments/')  # Adjust the upload path as needed
    file_type = models.CharField(max_length=50, choices=[('JPG', 'JPG'), ('PNG', 'PNG')])
    file_size = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(4194304)])  # Max 4MB in bytes

    def __str__(self):
        return f"{self.problem.title} - {self.file_path}"

# Define the Notification model
class Notification(models.Model):
    message = models.TextField()
    send_date = models.DateTimeField(auto_now_add=True)
    notification_type = models.CharField(max_length=100, choices=[('SMS', 'SMS'), ('Email', 'Email'), ('App', 'App')])
    notification_status = models.CharField(max_length=50, choices=[('Sent', 'Sent'), ('Failed', 'Failed'), ('Pending', 'Pending')], default='Pending')
    staff = models.ForeignKey(Staff, on_delete=models.SET_NULL, null=True, blank=True)
    expert = models.ForeignKey(Expert, on_delete=models.SET_NULL, null=True, blank=True)
    problem = models.ForeignKey(Problem, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.message

# Define the Comment model
class Comment(models.Model):
    content = models.TextField()
    rating_value = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(10)], blank=True, null=True)
    date = models.DateField(auto_now_add=True)
    problem = models.ForeignKey(Problem, on_delete=models.CASCADE)
    staff = models.ForeignKey(Staff, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.content

#Define OTP Models and verification code time validation
class OTP(models.Model):
    phone_number = models.CharField(max_length=15)
    otp_code = models.CharField(max_length=6)
    created_at = models.DateTimeField(auto_now_add=True)

    def is_valid(self):
        # Assuming OTP is valid for 5 minutes
        return self.created_at >= timezone.now() - datetime.timedelta(minutes=5)