from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.models import User
from django.db.models import Q

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken

from .models import (
    FormTemplate, FormField, Employee, UserProfile
)
from .serializers import (
    RegisterSerializer, UserSerializer, ChangePasswordSerializer,
    UserProfileSerializer, FormTemplateSerializer,
    FormTemplateCreateSerializer, EmployeeSerializer
)


def login_view(request):
    # If user is already logged in, redirect to dashboard
    if request.user.is_authenticated:
        return redirect('dashboard')

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('dashboard')
        else:
            messages.error(request, 'Invalid username or password')

    # Render login page
    return render(request, 'employees/login.html')


def register_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard')

    if request.method == 'POST':
        password = request.POST.get('password')
        password2 = request.POST.get('password2')

        if password != password2:
            messages.error(request, 'Passwords do not match')
        else:
            user = User.objects.create_user(
                username=request.POST.get('username'),
                email=request.POST.get('email'),
                password=password,
                first_name=request.POST.get('first_name', ''),
                last_name=request.POST.get('last_name', '')
            )
            UserProfile.objects.create(user=user)
            messages.success(request, 'Account created successfully')
            return redirect('login')

    return render(request, 'employees/register.html')


@login_required
def logout_view(request):
    logout(request)
    return redirect('login')


@login_required
def dashboard_view(request):
    return render(request, 'employees/dashboard.html', {
        'form_templates_count': FormTemplate.objects.count(),
        'employees_count': Employee.objects.count()
    })


@login_required
def profile_view(request):
    return render(request, 'employees/profile.html')


@login_required
def change_password_view(request):
    return render(request, 'employees/change_password.html')


@login_required
def form_list_view(request):
    return render(request, 'employees/form_list.html')


@login_required
def form_create_view(request):
    return render(request, 'employees/form_create.html')


@login_required
def form_edit_view(request, pk):
    return render(request, 'employees/form_edit.html', {'form_id': pk})


@login_required
def employee_list_view(request):
    return render(request, 'employees/employee_list.html')


@login_required
def employee_create_view(request):
    return render(request, 'employees/employee_create.html')


@login_required
def employee_edit_view(request, pk):
    return render(request, 'employees/employee_edit.html', {'employee_id': pk})

class RegisterAPIView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        refresh = RefreshToken.for_user(user)
        return Response({
            'user': UserSerializer(user).data,
            'refresh': str(refresh),
            'access': str(refresh.access_token)
        }, status=status.HTTP_201_CREATED)


class LoginAPIView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        user = authenticate(
            username=request.data.get('username'),
            password=request.data.get('password')
        )

        if not user:
            return Response(
                {'error': 'Invalid credentials'},
                status=status.HTTP_401_UNAUTHORIZED
            )

        refresh = RefreshToken.for_user(user)
        return Response({
            'user': UserSerializer(user).data,
            'refresh': str(refresh),
            'access': str(refresh.access_token)
        })


class ChangePasswordAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = ChangePasswordSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        if not request.user.check_password(serializer.validated_data['old_password']):
            return Response(
                {'old_password': 'Wrong password'},
                status=status.HTTP_400_BAD_REQUEST
            )

        request.user.set_password(serializer.validated_data['new_password'])
        request.user.save()
        return Response({'message': 'Password updated successfully'})


class UserProfileAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        serializer = UserProfileSerializer(request.user.profile)
        return Response(serializer.data)

    def put(self, request):
        serializer = UserProfileSerializer(
            request.user.profile,
            data=request.data,
            partial=True
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)


class FormTemplateAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        templates = FormTemplate.objects.all()
        return Response(FormTemplateSerializer(templates, many=True).data)

    def post(self, request):
        serializer = FormTemplateCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(created_by=request.user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class FormTemplateDetailAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get_object(self, pk):
        return FormTemplate.objects.get(pk=pk)

    def get(self, request, pk):
        return Response(
            FormTemplateSerializer(self.get_object(pk)).data
        )

    def put(self, request, pk):
        serializer = FormTemplateCreateSerializer(
            self.get_object(pk),
            data=request.data,
            partial=True
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    def delete(self, request, pk):
        self.get_object(pk).delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class EmployeeAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        queryset = Employee.objects.all()
        search = request.query_params.get('search')

        if search:
            ids = []
            for emp in queryset:
                for value in emp.data.values():
                    if search.lower() in str(value).lower():
                        ids.append(emp.id)
            queryset = queryset.filter(id__in=ids)

        return Response(EmployeeSerializer(queryset, many=True).data)

    def post(self, request):
        serializer = EmployeeSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(created_by=request.user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class EmployeeDetailAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get_object(self, pk):
        return Employee.objects.get(pk=pk)

    def get(self, request, pk):
        return Response(
            EmployeeSerializer(self.get_object(pk)).data
        )

    def put(self, request, pk):
        serializer = EmployeeSerializer(
            self.get_object(pk),
            data=request.data,
            partial=True
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    def delete(self, request, pk):
        self.get_object(pk).delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
