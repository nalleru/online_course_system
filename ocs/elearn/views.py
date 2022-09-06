from django.shortcuts import get_object_or_404, redirect, render
from django.views.generic import TemplateView
from django.contrib import auth
from django.contrib.auth import authenticate
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib.auth import logout
from django.urls import reverse_lazy
from django.views import generic
#from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.http import HttpResponse, Http404
#from .models import Customer, Profile
from .forms import StudentSignUpForm, InstructorSignUpForm, StudentInterestsForm, StudentCourse, UserForm, ProfileForm, PostForm
from django.http import HttpResponseRedirect, HttpResponse
from django.template import loader
from django.urls import reverse
from django.utils import timezone
from django.core import serializers
from django.conf import settings
import os
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib import auth
from datetime import datetime, date
from django.core.exceptions import ValidationError
from . import models
import operator
import itertools
from django.db.models import Avg, Count, Sum
from django.forms import inlineformset_factory
from .models import User, Profile, Course, Tutorial, Subscription, Course_instructor, Announcement, Student, Instructor
from django.db import transaction
from django.contrib.auth.hashers import make_password
from django.core.files.storage import FileSystemStorage
from django.contrib.auth.forms import (AuthenticationForm, UserCreationForm,
                                       PasswordChangeForm)

from django.contrib.auth import update_session_auth_hash


from bootstrap_modal_forms.generic import (
    BSModalLoginView,
    BSModalFormView,
    BSModalCreateView,
    BSModalUpdateView,
    BSModalReadView,
    BSModalDeleteView
)


#Shared views
def home(request):
    return render(request, 'home.html')

def logoutView(request):
    logout(request)
    return redirect('home')

def login_form(request):
    return render(request, 'login.html')

def loginView(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None and user.is_active:
            auth.login(request, user)
            if user.is_admin or user.is_superuser:
                return redirect('dashboard')
            elif user.is_instructor:
                return redirect('instructor')
            elif user.is_student:
                return redirect('student')
            else:
                return redirect('login_form')

        else:
            messages.info(request, 'Invalid Username or Password')
            return redirect('login_form')


# Student views

class StudentSignUpView(CreateView):
    model = User
    form_class = StudentSignUpForm
    template_name = 'signup_form.html'

    def get_context_data(self, **kwargs):
        kwargs['user_type'] = 'student'
        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('home')


#Admin views
def dashboard(request):
    student = User.objects.filter(is_student=True).count()
    instructor = User.objects.filter(is_instructor=True).count()
    course = Course.objects.all().count()
    users = User.objects.all().count()
    context = {'student':student, 'course':course, 'instructor':instructor, 'users': users}

    return render(request, 'dashboard/admin/home.html', context)


class InstructorSignUpView(CreateView):
    model = User
    form_class = InstructorSignUpForm
    template_name = 'dashboard/admin/signup_form.html'

    def get_context_data(self, **kwargs):
        kwargs['user_type'] = 'instructor'
        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        user = form.save()
        messages.success(self.request, 'Instructor Added successfully')
        return redirect('isign')


class AdminStudent(CreateView):
    model = User
    form_class = StudentSignUpForm
    template_name = 'dashboard/admin/student_signup_form.html'

    def get_context_data(self, **kwargs):
        kwargs['user_type'] = 'student'
        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        user = form.save()
        messages.success(self.request, 'Student Added successfully')
        return redirect('addstudent')


def course(request):
    if request.method == 'POST':
        name = request.POST['name']

        a = Course(name=name)
        a.save()
        messages.success(request, 'New Course Registered successfully!')
        return redirect('course')
    else:
        return render(request, 'dashboard/admin/course.html')


class AdminCreatePost(CreateView):
    model = Announcement
    form_class = PostForm
    template_name = 'dashboard/admin/post_form.html'
    success_url = reverse_lazy('alpost')

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.user = self.request.user
        self.object.save()
        return super().form_valid(form)


class AdminListAnnouncement(LoginRequiredMixin, ListView):
    model = Announcement
    template_name = 'dashboard/admin/announcement_list.html'

    def get_queryset(self):
        return Announcement.objects.filter(posted_at=timezone.now()).order_by('posted_at')


class ListAllAnnouncements(LoginRequiredMixin, ListView):
    model = Announcement
    template_name = 'dashboard/admin/list_announcements.html'
    context_object_name = 'announcements'
    paginate_by = 10

    def get_queryset(self):
        return Announcement.objects.order_by('-id')




