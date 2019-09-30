from rest_framework import generics, permissions, viewsets
from rest_framework.response import Response
from rest_framework.views import APIView
from knox.models import AuthToken
from .serializers import StudentSerializer, RegisterStudentSerializer, LoginStudentSerializer, RegisterTeamSerializer, TeamSerializer, ProjectSerializer

from .models import *

from .signals import students_changed
from django.db.models.signals import m2m_changed

m2m_changed.connect(students_changed, sender=Team.students.through,
                    dispatch_uid='students_changed')


class RegisterStudentAPI(generics.GenericAPIView):
    serializer_class = RegisterStudentSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response({
            "user": StudentSerializer(user, context=self.get_serializer_context()).data,
            "token": AuthToken.objects.create(user)[1]
        })


class LoginStudentAPI(generics.GenericAPIView):
    serializer_class = LoginStudentSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data
        return Response({
            "user": StudentSerializer(user, context=self.get_serializer_context()).data,
            "token": AuthToken.objects.create(user)[1]
        })


class StudentAPI(generics.RetrieveAPIView):
    permission_classes = [
        permissions.IsAuthenticated,
    ]
    serializer_class = StudentSerializer

    def get_object(self):
        return self.request.user


class RegisterTeamAPI(generics.GenericAPIView):
    serializer_class = RegisterTeamSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        team = serializer.save()
        return Response({
            "team": TeamSerializer(team, context=self.get_serializer_context()).data,
        })


class TeamAPI(viewsets.ReadOnlyModelViewSet):
    serializer_class = TeamSerializer

    queryset = Team.objects.all()


class AddStudentAPI(APIView):
    serializer_class = RegisterTeamSerializer
    permission_classes = [
        permissions.IsAuthenticated,
    ]

    def post(self, request, *args, **kwargs):
        data_obj = request.data

        if (len(Team.objects.filter(token=data_obj['team_token'])) == 0):
            return Response({
                'err': 'Team Not Found'
            }, status=400)

        student_obj = Student.objects.get(pk=data_obj['student'])
        team = Team.objects.get(token=data_obj['team_token'])
        team.students.add(student_obj)
        return Response({
            'team': TeamSerializer(team).data
        })


class ProjectAPI(viewsets.ModelViewSet):
    serializer_class = ProjectSerializer
    permission_classes = [
        permissions.IsAuthenticated,
    ]

    queryset = Project.objects.all()

    def get_queryset(self):
        user = self.request.user
        student_team = user.student.all()

        return Project.objects.filter(team__in=student_team)


class StudentTeamAPI(viewsets.ReadOnlyModelViewSet):
    serializer_class = TeamSerializer
    permission_classes = [
        permissions.IsAuthenticated,
    ]

    def get_queryset(self):
        user = self.request.user
        return user.student.all()
