from django.db import models
from django.contrib.auth.models import User


class UserProfile(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='profile'
    )
    phone = models.CharField(max_length=20, blank=True)
    address = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username

class FormTemplate(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    created_by = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='created_forms'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

class FormField(models.Model):
    FIELD_TYPE_CHOICES = (
        ('text', 'Text'),
        ('number', 'Number'),
        ('date', 'Date'),
        ('password', 'Password'),
        ('email', 'Email'),
        ('textarea', 'Textarea'),
        ('select', 'Select'),
        ('checkbox', 'Checkbox'),
        ('radio', 'Radio'),
    )

    form_template = models.ForeignKey(
        FormTemplate,
        on_delete=models.CASCADE,
        related_name='fields'
    )
    label = models.CharField(max_length=255)
    field_type = models.CharField(
        max_length=50,
        choices=FIELD_TYPE_CHOICES
    )
    required = models.BooleanField(default=False)
    options = models.JSONField(
        blank=True,
        null=True,
        help_text="Used for select, checkbox, radio fields"
    )
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return f"{self.label} ({self.field_type})"

class Employee(models.Model):
    form_template = models.ForeignKey(
        FormTemplate,
        on_delete=models.PROTECT,
        related_name='employees'
    )
    data = models.JSONField(
        help_text="Stores dynamic employee form data"
    )
    created_by = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='employees'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Employee #{self.id}"
