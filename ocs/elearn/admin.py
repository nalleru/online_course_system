from django.contrib import admin
from .models import User, Profile, Course, Tutorial, Subscription, Course_instructor, Announcement, Student, Instructor

# Register your models here.
admin.site.register(User)
admin.site.register(Profile)
admin.site.register(Course)
admin.site.register(Tutorial)
admin.site.register(Subscription)
admin.site.register(Course_instructor)
admin.site.register(Announcement)
admin.site.register(Student)
admin.site.register(Instructor)