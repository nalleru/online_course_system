from django.contrib.auth.models import AbstractUser
from django.db import models


# Create your models here.
class User(AbstractUser):
    is_student = models.BooleanField(default=False)
    is_instructor = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)



class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=255, default='')
    last_name = models.CharField(max_length=255, default='')
    email = models.EmailField(default='none@email.com')

    def __str__(self):
        return self.user.username


class Announcement(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    posted_at = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return str(self.content)


class Course(models.Model):
    name = models.CharField(max_length=30)

    def __str__(self):
        return self.name


class Tutorial(models.Model):
    title = models.CharField(max_length=50)
    content = models.TextField()
    course = models.ForeignKey(Course, on_delete=models.CASCADE, default='')
    created_at = models.DateTimeField(auto_now_add=True)
    price = models.IntegerField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)


class Subscription(models.Model):
    course_id = models.ForeignKey(Course, on_delete=models.CASCADE)
    course_topic = models.CharField(max_length=255)
    subsciption_date = models.DateTimeField(auto_now_add=True)
    course_price = models.IntegerField()
    subscribed_students = models.IntegerField()

    class Meta:
        verbose_name_plural = 'Subscriptions'

    def __str__(self):
        return self.course_topic


class Course_instructor(models.Model):
    course_id = models.ForeignKey(Course, on_delete=models.CASCADE)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)


class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    interests = models.ManyToManyField(Course, related_name='interested_learners')


    def __str__(self):
        return self.user.username


class Instructor(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    interest = models.ManyToManyField(Course, related_name="more_locations")





