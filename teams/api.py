from rest_framework import generics, permissions, viewsets, status
from rest_framework.response import Response
from rest_framework.views import APIView
from knox.models import AuthToken

from django.core.mail import EmailMessage
from django.shortcuts import render, redirect
from django.contrib.auth.models import Group
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes, force_text
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode

from .models import *
from .forms import ResetPasswordForm
from .token import account_activation_token, password_reset_token
from .serializers import StudentSerializer, RegisterStudentSerializer, LoginStudentSerializer, RegisterTeamSerializer, TeamSerializer, ProjectSerializer, ChangePasswordSerializer, ResetPasswordSerializer


class RegisterStudentAPI(generics.GenericAPIView):
    """
    API endpoint for registering a new participant and sending confirmation email
    """
    serializer_class = RegisterStudentSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = serializer.save()
        user.is_active = False
        user.save()

        current_site = get_current_site(request)
        mail_subject = 'Activate your DSC-WOW account.'
        message = render_to_string('acc_active_email.html', {
                'user': user.first_name,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': account_activation_token.make_token(user),
            })
        to_email = user.email
        email = EmailMessage(
                        mail_subject, message, to=[to_email]
            )
        email.content_subtype = "html"
        email.send()
        return Response({ 
            "details":"Please Confirm Your Email!"
        })

        # return Response({
        #     "user": StudentSerializer(user, context=self.get_serializer_context()).data,
        #     "token": AuthToken.objects.create(user)[1]
        # })


class LoginStudentAPI(generics.GenericAPIView):
    """
    API endpoint for user login
    """
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
    """
    API endpoint to get current user
    """

    permission_classes = [
        permissions.IsAuthenticated,
    ]
    serializer_class = StudentSerializer

    def get_object(self):
        return self.request.user


class RegisterTeamAPI(generics.GenericAPIView):
    """
    API endpoint to create a new team and add the current user to it
    """
    permission_classes = [
        permissions.IsAuthenticated,
    ]
    serializer_class = RegisterTeamSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        team = serializer.save()
        user = request.user
        team.students.add(user)
        return Response({
            "team": TeamSerializer(team, context=self.get_serializer_context()).data,
        })


class TeamAPI(viewsets.ReadOnlyModelViewSet):
    """
    API endpoint to get all the teams
    """
    serializer_class = TeamSerializer

    queryset = Team.objects.all()


class AddStudentAPI(APIView):
    """
    API endpoint to add a student to a team
    """
    serializer_class = RegisterTeamSerializer
    permission_classes = [
        permissions.IsAuthenticated,
    ]

    def validate_request(self):
        user = self.request.user
        print(user)
        print(user.team.all().exists())
        if user.team.all().exists():
            return Response({"err": "User has already joined a team"}, status=status.HTTP_400_BAD_REQUEST)

    def post(self, request, *args, **kwargs):
        response = self.validate_request()
        if response:
            return response
            
        data_obj = request.data

        if (len(Team.objects.filter(token=data_obj['team_token'])) == 0):
            return Response({
                'err': 'Team Not Found'
            }, status=400)

        student_obj = request.user
        team = Team.objects.get(token=data_obj['team_token'])
        team.students.add(student_obj)
        return Response({
            'team': TeamSerializer(team).data
        })


class ProjectAPI(viewsets.ModelViewSet):
    """
    API endpoint to create and get current user's team's projects
    """
    serializer_class = ProjectSerializer
    permission_classes = [
        permissions.IsAuthenticated,
    ]

    queryset = Project.objects.all()

    def perform_create(self, serializer):
        user = self.request.user
        student_team = user.team.get()

        serializer = serializer.save(team=student_team)


    def get_queryset(self):
        user = self.request.user
        student_team = user.team.all()

        return Project.objects.filter(team__in=student_team)


class StudentTeamAPI(viewsets.ReadOnlyModelViewSet):
    """
    API endpoint to get current user's team and team members
    """
    serializer_class = TeamSerializer
    permission_classes = [
        permissions.IsAuthenticated,
    ]

    def get_queryset(self):
        user = self.request.user
        return user.team.all()


class UpdatePasswordAPI(generics.GenericAPIView):
    """
    API endpoint for changing password.
    """
    permission_classes = (permissions.IsAuthenticated, )
    serializer_class = ChangePasswordSerializer

    def get_object(self, queryset=None):
        return self.request.user

    def put(self, request, *args, **kwargs):
        self.object = self.get_object()
        serializer = ChangePasswordSerializer(data=request.data)

        if serializer.is_valid():
            # Check old password
            old_password = serializer.data.get("old_password")
            if not self.object.check_password(old_password):
                return Response({"details": ["Wrong password."]}, 
                                status=status.HTTP_400_BAD_REQUEST)
            # set_password also hashes the password that the user will get
            self.object.set_password(serializer.data.get("new_password"))
            self.object.save()
            return Response({"details":["Password Changed"]}, status=status.HTTP_204_NO_CONTENT)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ResetPasswordAPI(generics.GenericAPIView):

    serializer_class = ResetPasswordSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = serializer.validated_data

        current_site = get_current_site(request)
        mail_subject = 'Reset your DSC WOW password.'
        message = render_to_string('reset_password_email.html', {
                'user': user.first_name,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': password_reset_token.make_token(user),
            })
        to_email = user.email
        email = EmailMessage(
                        mail_subject, message, to=[to_email]
            )
        email.content_subtype = "html"
        email.send()
        return Response({ 
            "details":"Please Reset Your Password!"
        })

class RegisterOrganizerAPI(generics.GenericAPIView):

    serializer_class = RegisterStudentSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = serializer.save()
        organizer_group = Group.objects.get(name='Organizer') 
        user.groups.add(organizer_group)
        user.is_staff = True
        user.is_active = True
        user.save()

        return Response({
            "user": StudentSerializer(user, context=self.get_serializer_context()).data,
            "token": AuthToken.objects.create(user)[1]
        })


def ActivateAccount(request, uidb64, token):
    """
    API endpoint to activate user's account
    """

    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = Student.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, Student.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        details={}
        details['details'] = 'Your email is confirmed'
        return render(request, 'email_conf.html', details)
    else:
        details={}
        details['details'] = 'Activation Link is Invalid!'
        return render(request, 'email_conf.html', details)


def ResetPassword(request, uidb64, token):
    """
    API endpoint to reset user password
    """

    form = ResetPasswordForm(request.POST)

    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = Student.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, Student.DoesNotExist):
        user = None
    if user is not None and password_reset_token.check_token(user, token):
        if request.method == "POST":
            if form.is_valid():
                new_password = form.cleaned_data['new_password']
                user.set_password(new_password)
                user.save()
                return redirect('login')
        else:
            form = ResetPasswordForm()
        return render(request, 'password_reset.html', {'form': form})

    