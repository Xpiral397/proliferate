import json
import uuid
from django.db import models
from django.contrib.auth.models import User
from django.db.models import JSONField
from django.utils.text import slugify
from rest_framework_simplejwt.tokens import RefreshToken
# Create your models here.


class Subject(models.Model):
    name = models.CharField(max_length=255)
    level = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.name

class Profile(models.Model):
    user =models.OneToOneField(User,on_delete=models.CASCADE )
    full_name = models.CharField(max_length =255, blank=True, null=True)
    first_name =  models.CharField(max_length =255, blank=True, null=True)
    last_name =  models.CharField(max_length =255, blank=True, null=True)
    email = models.EmailField(max_length=255, blank=True, null=True)
    image = models.ImageField(blank=True, null=True)
    user_type = models.CharField(max_length=50, blank=True, null=True)
    bio =  models.TextField(blank=True, null=True)
    phone =models.CharField(max_length=50, blank=True, null=True)
    createdAt = models.DateTimeField(auto_now_add=True)
    _id = models.AutoField(primary_key=True, editable=False)
    is_verified = models.BooleanField(default = False, null=True, blank=True)
    token = models.CharField(max_length=10, null =True, blank = True)

    def __str__(self):
        return self.email

    def tokens(self):
        refresh = RefreshToken.for_user(self)
        return({
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        })


class TutorProfile(models.Model):
    DAYS_OF_WEEK = [
        ('monday', 'Monday'),
        ('tuesday', 'Tuesday'),
        ('wednesday', 'Wednesday'),
        ('thursday', 'Thursday'),
        ('friday', 'Friday'),
        ('saturday', 'Saturday'),
    ]

    AVAILABLE_TIME = [
        (i, f"{i:02}:00 AM") for i in range(0, 12)
    ] + [
        (i, f"{i:02}:00 PM") for i in range(12, 24)
    ]

    profile = models.OneToOneField(Profile, on_delete=models.CASCADE)
    subjects = models.ManyToManyField(Subject)
    grades = models.TextField(blank=True, null=True)
    sessionRate = models.DecimalField(default=0.00,max_digits=10, decimal_places=2)
    availability_days = JSONField(default=list, blank=True, null=True)
    available_time = JSONField(default=list, blank=True, null=True)
    createdAt = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    _id = models.AutoField(primary_key=True, editable=False, blank=True)

    def set_availability_days(self, data):
        self.availability_days = json.dumps(data)

    def set_available_time(self, data):
        self.available_time = json.dumps(data)

    def get_availability_days(self):
        return json.loads(self.availability_days) if self.availability_days else []

    def get_available_time(self):
        return json.loads(self.available_time) if self.available_time else []

    def __str__(self):
        return self.profile.email


class TutorVerifictions(models.Model):
    profile = models.OneToOneField(Profile,on_delete=models.CASCADE)
    means_of_identity = models.CharField(max_length=255, blank=True, null=True)
    document= models.FileField()

    def __str__(self) -> str:
        return self.profile.full_name


class StudentProfile(models.Model):
    profile = models.OneToOneField(Profile,on_delete=models.CASCADE)
    grade_level = models.CharField(max_length=255, blank=True, null=True)
    preferred_subjects = models.CharField(max_length=255, blank=True, null=True)
    learning_goal = models.CharField(max_length=255, blank=True, null=True)
    timezone = models.CharField(max_length=255, blank=True, null=True)
    country = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return self.profile.full_name



class Blog(models.Model):
    title = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, unique=True, blank=True)
    content = models.TextField()
    author = models.ForeignKey(Profile, on_delete=models.CASCADE)
    published = models.BooleanField(default=False)
    publish_date = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated_date = models.DateTimeField(auto_now=True)
    featured_image = models.ImageField(null=True, blank=True)
    
    class Meta:
        ordering = ['-publish_date']
        
    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        # Generate a unique slug based on the title and a UUID
        if not self.slug:
            unique_slug = slugify(self.title) + '-' + str(uuid.uuid4())[:8]
            self.slug = unique_slug
        super(Blog, self).save(*args, **kwargs)



class Comment(models.Model):
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE, related_name='comments')
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'Comment by {self.profile.user.username} on {self.blog.title}'
    





class Class(models.Model):
    tutor = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='teacher')
    students = models.ManyToManyField(Profile, related_name='enrolled_students')
    name = models.CharField(max_length=255, blank=True, null=True)
    grade = models.CharField(max_length=255, blank=True, null=True)
    status = models.CharField(max_length=255, default="pending", blank=True, null=True)
    start_time = models.TimeField(blank=True, null=True)
    end_time = models.TimeField(blank=True, null=True)  
    createdAt = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
    

class Assignment(models.Model):
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE,  blank=True, null=True)
    tutor = models.ForeignKey(Profile, on_delete=models.CASCADE, blank=True, null=True)
    student = models.ForeignKey(StudentProfile, on_delete=models.CASCADE, blank=True, null=True)
    submission_date = models.DateField(blank=True, null=True)
    title = models.CharField(max_length=300, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    grade_level = models.CharField(max_length=300, blank=True, null=True)
    start_date =models.DateField(blank=True, null=True)
    end_date = models.DateField(blank=True, null=True)
    createdAt = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
    

class AssignmentSubmission(models.Model):
    pass
    

class classSchedule(models.Model):
    student = models.ForeignKey(StudentProfile, on_delete=models.CASCADE)
    tutor = models.ForeignKey(TutorProfile, on_delete=models.CASCADE)
    name = models.CharField(max_length=300, blank=True, null=True)
    accepted= models.BooleanField(default=False)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    is_paid=models.BooleanField(default=False)

    def __str__(self):
        return self.name




class ClassMessage(models.Model):
    sender = models.ForeignKey(Profile, on_delete=models.CASCADE)
    group = models.ForeignKey(Class, on_delete=models.CASCADE)
    content = models.TextField()
  
    file = models.FileField(upload_to='message_files/', null=True, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __Str__(self):
        return self.content