# Employee Management System (EMS)

A comprehensive Django-based Employee Management System with dynamic form creation, drag-and-drop field ordering, and RESTful API with JWT authentication.

## Features

### Authentication & Profile Management

- User Registration with email validation
- Login with JWT token authentication
- Password change functionality
- User profile management with additional fields (phone, address, date of birth)

### Dynamic Form Builder

- Create custom forms with multiple field types:
  - Text, Number, Email, Date, Password
  - Text Area, Select, Checkbox, Radio
- Drag-and-drop functionality to reorder form fields
- Add/remove fields dynamically
- Set required fields and placeholders
- Edit existing forms

### Employee Management

- Create employee records using pre-designed forms
- Dynamic form rendering based on selected template
- List all employees with search functionality
- Edit and delete employee records
- Filter employees by dynamic field values

### RESTful API

- JWT-based authentication (access & refresh tokens)
- Complete CRUD operations for forms and employees
- Search and filter capabilities
- Postman collection included for testing

## Technology Stack

- **Backend**: Django 4.2.7, Django REST Framework
- **Authentication**: JWT (djangorestframework-simplejwt)
- **Frontend**: HTML, CSS, JavaScript (Vanilla JS with AJAX/Fetch API)
- **Database**: SQLite (default, can be changed to PostgreSQL/MySQL)
- **API Documentation**: Postman Collection

## Project Structure

```
ems_project/
├── ems_project/
│   ├── __init__.py
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── employees/
│   ├── migrations/
│   ├── __init__.py
│   ├── admin.py
│   ├── api_views.py
│   ├── models.py
│   ├── serializers.py
│   ├── views.py
├── templates/
│   ├── base.html
│   └── employees/
│       ├── login.html
│       ├── register.html
│       ├── dashboard.html
│       ├── profile.html
│       ├── change_password.html
│       ├── form_list.html
│       ├── form_create.html
│       ├── form_edit.html
│       ├── employee_list.html
│       ├── employee_create.html
│       └── employee_edit.html
├── static/
├── media/
├── requirements.txt
└── README.md
```

## Installation & Setup

### 1. Clone or Create Project Directory

```bash
mkdir ems_project
cd ems_project
```

### 2. Create Virtual Environment

```bash
python -m venv venv

# Windows
venv\Scripts\activate

# Linux/Mac
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Create Django Project Structure

```bash
django-admin startproject ems_project .
python manage.py startapp employees
```

### 5. Create Directory Structure

```bash
mkdir templates
mkdir templates/employees
mkdir static
mkdir media
```

### 6. Update settings.py

Replace the content of `ems_project/settings.py` with the provided `settings.py` file.

### 7. Add Models

Add the provided code to `employees/models.py`

### 8. Add Serializers

Create `employees/serializers.py` and add the provided code.

### 9. Add Views

Replace `employees/views.py` with the provided code and create `employees/api_views.py` with the API views.

### 10. Add Admin Configuration

Replace `employees/admin.py` with the provided code.

### 11. Configure URLs

Replace `ems_project/urls.py` with the provided URL configuration.

### 12. Add Templates

Create all HTML template files in `templates/employees/` directory with the provided code.

### 13. Run Migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

### 14. Create Superuser

```bash
python manage.py createsuperuser
```

### 15. Run Development Server

```bash
python manage.py runserver
```

Visit `http://localhost:8000` to access the application.

## Usage Guide

### Web Interface

1. **Register/Login**: Create an account or login at `http://localhost:8000`
2. **Dashboard**: View statistics and quick actions
3. **Create Form**:
   - Navigate to Forms → Create New Form
   - Add fields with drag-and-drop ordering
   - Configure field types, labels, and validation
4. **Create Employee**:
   - Navigate to Employees → Add Employee
   - Select a form template
   - Fill in dynamic fields
   - Submit to create employee record
5. **Search & Filter**: Use the search bar to filter employees by any field value
6. **Edit/Delete**: Manage forms and employee records with edit/delete options

### API Endpoints

#### Authentication

- **POST** `/api/auth/register/` - Register new user
- **POST** `/api/auth/login/` - Login and get JWT tokens
- **POST** `/api/auth/token/refresh/` - Refresh access token
- **POST** `/api/auth/change-password/` - Change password
- **GET** `/api/auth/profile/` - Get user profile
- **PATCH** `/api/auth/profile/` - Update user profile

#### Form Templates

- **GET** `/api/forms/` - List all form templates
- **POST** `/api/forms/` - Create new form template
- **GET** `/api/forms/{id}/` - Get form template details
- **PUT** `/api/forms/{id}/` - Update form template
- **DELETE** `/api/forms/{id}/` - Delete form template

#### Employees

- **GET** `/api/employees/` - List all employees
- **GET** `/api/employees/?search={term}` - Search employees
- **POST** `/api/employees/` - Create new employee
- **GET** `/api/employees/{id}/` - Get employee details
- **PUT** `/api/employees/{id}/` - Update employee
- **DELETE** `/api/employees/{id}/` - Delete employee

## API Testing with Postman

1. Import the provided `Employee_Management_System.postman_collection.json` into Postman
2. Update the `base_url` variable if needed (default: `http://localhost:8000`)
3. Run the "Register" or "Login" request to get JWT tokens
4. Tokens are automatically saved to collection variables
5. All other requests will use the saved access token

### Sample API Requests

#### Create Form Template

```json
POST /api/forms/
{
    "name": "Employee Registration Form",
    "description": "Standard employee registration form",
    "fields": [
        {
            "label": "Full Name",
            "field_type": "text",
            "is_required": true,
            "placeholder": "Enter full name",
            "order": 0
        },
        {
            "label": "Email",
            "field_type": "email",
            "is_required": true,
            "placeholder": "Enter email address",
            "order": 1
        },
        {
            "label": "Department",
            "field_type": "select",
            "is_required": true,
            "options": ["IT", "HR", "Finance", "Marketing"],
            "order": 2
        }
    ]
}
```

#### Create Employee

```json
POST /api/employees/
{
    "form_template_id": 1,
    "data": {
        "Full Name": "John Doe",
        "Email": "john.doe@example.com",
        "Department": "IT"
    }
}
```

## Key Features Explained

### Dynamic Form Creation

Forms are created with customizable fields that can include:

- Multiple input types (text, number, email, date, etc.)
- Validation rules (required/optional)
- Custom placeholders
- Options for select, checkbox, and radio fields

### Drag-and-Drop Field Ordering

Fields can be reordered by dragging them up or down in the form builder. The order is maintained when creating or editing employees.

### AJAX-Based Operations

All form submissions use Axios/Fetch API instead of traditional Django form actions, providing a modern single-page application experience.

### Search Functionality

The employee list includes search functionality that filters across all dynamic fields, making it easy to find specific employees.

### JWT Authentication

API uses JWT tokens with access and refresh token mechanism:

- Access tokens expire after 1 hour
- Refresh tokens expire after 7 days
- Tokens are securely stored and transmitted

## Security Features

- CSRF protection for all state-changing operations
- Password validation with Django's built-in validators
- JWT token authentication for API
- User-specific data access
- SQL injection protection through Django ORM

## Admin Panel

Access the Django admin panel at `http://localhost:8000/admin/` to:

- Manage users and profiles
- View and edit form templates
- Manage employee records
- Monitor system activity

## Troubleshooting

### Migration Issues

```bash
python manage.py makemigrations employees
python manage.py migrate
```

### Static Files Not Loading

```bash
python manage.py collectstatic
```

### CORS Issues (if using separate frontend)

Install and configure django-cors-headers in settings.py

### JWT Token Expired

Use the refresh token endpoint to get a new access token

## Future Enhancements

- File upload support for employee documents
- Export employee data to CSV/Excel
- Advanced filtering and sorting options
- Role-based access control
- Email notifications
- Audit logs for all operations
- Multi-language support
- Dark mode theme

## Contributing

Feel free to submit issues and enhancement requests!

## License

This project is open-source and available for educational and commercial use.

## Support

For questions and support, please open an issue in the repository.
