from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from . import views

urlpatterns = [

    path('', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    path('logout/', views.logout_view, name='logout'),
    path('dashboard/', views.dashboard_view, name='dashboard'),
    path('profile/', views.profile_view, name='profile'),
    path('change-password/', views.change_password_view, name='change_password'),

    # Form Template Views
    path('forms/', views.form_list_view, name='form_list'),
    path('forms/create/', views.form_create_view, name='form_create'),
    path('forms/<int:pk>/edit/', views.form_edit_view, name='form_edit'),

    # Employee Views
    path('employees/', views.employee_list_view, name='employee_list'),
    path('employees/create/', views.employee_create_view, name='employee_create'),
    path('employees/<int:pk>/edit/', views.employee_edit_view, name='employee_edit'),

    path('api/auth/register/', views.RegisterAPIView.as_view(), name='api_register'),
    path('api/auth/login/', views.LoginAPIView.as_view(), name='api_login'),
    path('api/auth/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/auth/change-password/', views.ChangePasswordAPIView.as_view(), name='api_change_password'),
    path('api/auth/profile/', views.UserProfileAPIView.as_view(), name='api_profile'),

    # Form Template API
    path('api/forms/', views.FormTemplateAPIView.as_view(), name='api_form_list'),
    path('api/forms/<int:pk>/', views.FormTemplateDetailAPIView.as_view(), name='api_form_detail'),

    # Employee API
    path('api/employees/', views.EmployeeAPIView.as_view(), name='api_employee_list'),
    path('api/employees/<int:pk>/', views.EmployeeDetailAPIView.as_view(), name='api_employee_detail'),
]
