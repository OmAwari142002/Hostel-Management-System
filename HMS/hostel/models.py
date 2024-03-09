from django.db import models
from django.contrib.auth.models import User
from django.contrib.postgres.fields import ArrayField
import uuid
class Rooms(models.Model):
    roomNo = models.IntegerField()
    floorNo = models.IntegerField()
    Availability = models.BooleanField(default=True)
    NoOfOccupents = models.IntegerField(default=0)
    occupants = models.ManyToManyField(User, related_name='rooms', blank=True)
    occupants_uuid = ArrayField(models.UUIDField(), default=list)
    @property
    def AvailableSpace(self):
        return 3 - self.NoOfOccupents
    

# Script to populate rooms in the database

class Attendance(models.Model):
    attendance_choices = [
        ('P', 'Present'),
        ('A', 'Absent'),
        ('L', 'Leave'),
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='attendance_records')
    date = models.DateField(auto_now_add=True)
    attendance = models.CharField(max_length=10, choices=attendance_choices)

    def __str__(self):
        return f"{self.user.username} {self.date} {self.attendance}"
class Complaint(models.Model):
    
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    roomNo = models.IntegerField()
    complaint = models.TextField(blank=True, null=True)
    uploaded_image = models.TextField(blank=True, null=True)
    issue_type = models.CharField(max_length=255)
    selected_option = models.CharField(max_length=255)
    submitted_at = models.DateTimeField(auto_now_add=True)
    forwared_to = models.CharField(max_length=255)
    status = models.CharField(max_length=255)
    def __str__(self):
        return f"{self.name}'s Complaint"
class StudentDetails(models.Model):
    GENDER_CHOICES = [
        ('male', 'Male'),
        ('female', 'Female'),
        ('non', 'Non Binary'),
        ('na', 'Prefer Not To Say'),
    ]

    YEAR_CHOICES = [
        ('FE', 'FE'),
        ('SE', 'SE'),
        ('TE', 'TE'),
        ('BE', 'BE'),
    ]

    COLLEGE_CHOICES = [
        ('TAE', 'Trinity Academy of Engineering'),
        ('TCOER', 'Trinity College of Engineering and Research'),
        ('KJCOER', 'KJ College of Engineering and Research'),
      
    ]

    BRANCH_CHOICES = [
        ('CSE', 'Computer Engineering'),
        ('IT', 'Information Technology'),
        ('EnTC', 'EnTC'),
        ('CE', 'Civil Engineering'),
        ('ME', 'Mechanical Engineering'),
       
    ]
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='student_details')
    uuid = models.UUIDField()
    roomNo = models.IntegerField(default=0)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField()
    branch = models.CharField(max_length=50, choices=BRANCH_CHOICES)
    year = models.CharField(max_length=2, choices=YEAR_CHOICES)
    college = models.CharField(max_length=50, choices=COLLEGE_CHOICES)
    student_mobile = models.CharField(max_length=10)
    parent_mobile = models.CharField(max_length=10)
    address = models.TextField()
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES)
    parent_name = models.CharField(max_length=100)
    

    def __str__(self):
        return f"{self.first_name} {self.last_name}"
