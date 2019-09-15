from django.urls import path, include
from .api import LoginStudentAPI, RegisterStudentAPI, RegisterTeamAPI, StudentAPI, TeamAPI, ProjectsAPI, AddStudentAPI
from knox import views as knox_views

from .api import TeamAPI
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'api/auth/team', TeamAPI, basename='Team')
router.register(r'api/auth/project', ProjectsAPI, basename='Project')

urlpatterns = [
    path('api/auth/knox/', include('knox.urls')),
    path('api/auth/student', StudentAPI.as_view()),
    path('api/auth/login', LoginStudentAPI.as_view()),
    path('api/auth/logout/', knox_views.LogoutView.as_view(), name='knox_logout'),
    path('api/auth/reg/student', RegisterStudentAPI.as_view()),
    path('api/auth/reg/team', RegisterTeamAPI.as_view()),
    path('api/add/student', AddStudentAPI.as_view())
]

urlpatterns += router.urls
