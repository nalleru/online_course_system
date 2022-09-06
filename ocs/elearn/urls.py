from django.urls import path
from .import views
from django.contrib.auth import views as auth_views


urlpatterns = [
    path('', views.home, name='home'),
    path('lsign/', views.StudentSignUpView.as_view(), name='lsign'),
    path('isign/', views.InstructorSignUpView.as_view(), name='isign'),
    path('addstudent/', views.AdminStudent.as_view(), name='addstudent'),
    path('login/', views.loginView, name='login'),
    path('logout/', views.logoutView, name='logout'),
    path('login_form/', views.login_form, name='login_form'),

    path('dashboard/', views.dashboard, name='dashboard'),
    path('course/', views.course, name='course'),
    path('apost/', views.AdminCreatePost.as_view(), name='apost'),
    path('alpost/', views.AdminListAnnouncement.as_view(), name='alpost'),
    path('alistposts/', views.ListAllAnnouncements.as_view(), name='alistposts'),





    ]