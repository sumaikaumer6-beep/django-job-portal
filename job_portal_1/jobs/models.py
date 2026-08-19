from django.db import models
from django.contrib.auth.models import User
class UserProfile(models.Model):
    USER_TYPE_CHOICES = (
    ('student', 'Student'),
    ('employer', 'Employer'),
    )
    user=models.OneToOneField(User,on_delete=models.CASCADE,related_name='jobs_profile')
    user_type = models.CharField(max_length=20, choices=USER_TYPE_CHOICES, default='student')
    phone= models.CharField(max_length=15,blank=True,null=True)
    def __str__(self):
        return self.user.username
# Create your models here.
class Company(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    company_name = models.CharField(max_length=200)
    description = models.TextField()
    def __str__(self):
        return self.company_name
class Job(models.Model):
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    description = models.TextField()
    location = models.CharField(max_length=100)
    salary = models.CharField(max_length=100)
    posted_on = models.DateField(auto_now_add=True)
    def __str__(self):
        return self.title
class Applicant(models.Model):
    job = models.ForeignKey(Job, on_delete=models.CASCADE)
    student = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    resume = models.FileField(upload_to='resume/')
    applied_on = models.DateField(auto_now_add=True)
    def __str__(self):
        return f"{self.student.user.username}-{self.job.title}"