from django.urls import path, include
from django.contrib.auth.views import PasswordResetView, PasswordResetDoneView, PasswordResetConfirmView, PasswordResetCompleteView
from knox import views as knox_views

from .api import LoginStudentAPI, RegisterStudentAPI, RegisterTeamAPI, StudentAPI, TeamAPI, AddStudentAPI, ProjectAPI, StudentTeamAPI

from rest_framework.routers import DefaultRouter

from rest_framework_swagger.views import get_swagger_view

schema_view = get_swagger_view(title='Webathon API')

router = DefaultRouter()
router.register(r'api/auth/team', TeamAPI, basename='Team')
router.register(r'api/auth/project', ProjectAPI, basename='Project')
router.register(r'api/auth/student/team',
                StudentTeamAPI, basename='student_team')

urlpatterns = [
    path('api/doc', schema_view, name='documentation'),
    path('api/auth', include('knox.urls')),
    path('api/auth/student', StudentAPI.as_view()),
    path('api/auth/login', LoginStudentAPI.as_view()),
    path('api/auth/logout/', knox_views.LogoutView.as_view(), name='knox_logout'),
    path('api/auth/reg/student', RegisterStudentAPI.as_view()),
    path('api/auth/reg/team', RegisterTeamAPI.as_view()),
    path('api/add/student', AddStudentAPI.as_view()),
    path('api/auth/password/reset/',
         PasswordResetView.as_view(), name='password_reset'),
    path('api/auth/password/reset/done/',
         PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('api/auth/password/reset/confirm/<uidb64>-<token>',
         PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('api/auth/password/reset/complete/',
         PasswordResetCompleteView.as_view(), name='password_reset_complete')
]

urlpatterns += router.urls
