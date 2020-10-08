from django.urls import path, re_path, include
from knox import views as knox_views
from django.conf.urls import url

from .api import LoginStudentAPI, RegisterStudentAPI, RegisterTeamAPI, StudentAPI, TeamAPI, AddStudentAPI, ProjectAPI, StudentTeamAPI, UpdatePasswordAPI, ResetPasswordAPI, RegisterOrganizerAPI, ActivateAccount, ResetPassword

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
router.register(r'api/team', TeamAPI, basename='Team')
router.register(r'api/auth/project', ProjectAPI, basename='Project')
router.register(r'api/auth/student/team',
                StudentTeamAPI, basename='student_team')

urlpatterns = [
    url(r'^swagger(?P<format>\.json|\.yaml)$',
        schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path('swagger/', schema_view.with_ui('swagger',
                                         cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc',
                                       cache_timeout=0), name='schema-redoc'),


    path('api/auth/reg/org', RegisterOrganizerAPI.as_view()),

    path('api/auth', include('knox.urls')),
    path('api/auth/student', StudentAPI.as_view()),
    path('api/auth/login', LoginStudentAPI.as_view(), name='login'),
    path('api/auth/logout/', knox_views.LogoutView.as_view(), name='knox_logout'),
    path('api/auth/reg/student', RegisterStudentAPI.as_view()),
    path('api/auth/reg/team', RegisterTeamAPI.as_view()),
    path('api/auth/add/student', AddStudentAPI.as_view()),
    path('api/auth/changepassword', UpdatePasswordAPI.as_view()),

    path('api/resetpassword', ResetPasswordAPI.as_view()),

    re_path('activate/(?P<uidb64>[0-9A-Za-z_\\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/',
        ActivateAccount, name='activate'),
    re_path('resetpassword/(?P<uidb64>[0-9A-Za-z_\\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/',
        ResetPassword, name='resetpassword'),

    url(r'^api/password/',
        include('django_rest_passwordreset.urls', namespace='password_reset')),
]

urlpatterns += router.urls
