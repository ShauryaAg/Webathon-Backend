from rest_framework import serializers
from django.contrib.auth import authenticate

from teams.models import Student, Team, Project


class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = ('id', 'first_name', 'last_name', 'email', 'college',
                  'phone_no', 'is_leader',)


class RegisterStudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = ('first_name', 'last_name', 'email', 'college',
                  'phone_no', 'is_leader', 'password',)
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):

        username = validated_data['first_name'] + validated_data['email']

        user = Student.objects.create_user(
            email=validated_data['email'], password=validated_data['password'], first_name=validated_data['first_name'], last_name=validated_data['last_name'], college=validated_data['college'], phone_no=validated_data['phone_no'], username=username, is_leader=validated_data['is_leader'])

        return user


class LoginStudentSerializer(serializers.Serializer):
    email = serializers.CharField()
    password = serializers.CharField()

    def validate(self, data):
        user = authenticate(**data)
        if user and user.is_active:
            return user
        raise serializers.ValidationError("Incorrect Credentials")


class RegisterTeamSerializer(serializers.ModelSerializer):

    class Meta:
        model = Team
        fields = ('team_name', 'idea',)

    def create(self, data):
        team = Team.objects.create(
            team_name=data['team_name'], idea=data['idea'])

        return team


class TeamSerializer(serializers.ModelSerializer):
    class Meta:
        model = Team
        fields = ('id', 'team_name', 'idea', 'token', 'students',)


class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = ('id', 'project_name', 'git_url', 'deploy_link', 'team',)
