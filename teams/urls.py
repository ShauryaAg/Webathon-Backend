from django.urls import path, include
from django.contrib.auth.views import PasswordResetView, PasswordResetDoneView, PasswordResetConfirmView, PasswordResetCompleteView
from knox import views as knox_views

from .api import LoginStudentAPI, RegisterStudentAPI, RegisterTeamAPI, StudentAPI, TeamAPI, AddStudentAPI, ProjectAPI, StudentTeamAPI

from rest_framework.routers import DefaultRouter


from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

schema_view = get_schema_view(
    openapi.Info(
        title="Webathon API",
        default_version='v1',
        description="Test description",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="contact@snippets.local"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)


router = DefaultRouter()
router.register(r'api/auth/team', TeamAPI, basename='Team')
router.register(r'api/auth/project', ProjectAPI, basename='Project')
router.register(r'api/auth/student/team',
                StudentTeamAPI, basename='student_team')

urlpatterns = [
    path(r'^swagger(?P<format>\.json|\.yaml)$',
         schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path('swagger/', schema_view.with_ui('swagger',
                                         cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc',
                                       cache_timeout=0), name='schema-redoc'),

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
