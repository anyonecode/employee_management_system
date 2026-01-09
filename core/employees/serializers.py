from rest_framework import serializers
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from .models import FormTemplate, FormField, Employee, UserProfile


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'first_name', 'last_name')


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ('username', 'password', 'password2', 'email', 'first_name', 'last_name')

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Password fields didn't match."})
        return attrs

    def create(self, validated_data):
        validated_data.pop('password2')
        user = User.objects.create_user(**validated_data)
        UserProfile.objects.create(user=user)
        return user


class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True, validators=[validate_password])
    new_password2 = serializers.CharField(required=True)

    def validate(self, attrs):
        if attrs['new_password'] != attrs['new_password2']:
            raise serializers.ValidationError({"new_password": "Password fields didn't match."})
        return attrs


class UserProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    
    class Meta:
        model = UserProfile
        fields = '__all__'


class FormFieldSerializer(serializers.ModelSerializer):
    class Meta:
        model = FormField
        fields = '__all__'
        read_only_fields = ('form_template',)


class FormTemplateSerializer(serializers.ModelSerializer):
    fields = FormFieldSerializer(many=True, read_only=True)
    created_by = UserSerializer(read_only=True)

    class Meta:
        model = FormTemplate
        fields = '__all__'
        read_only_fields = ('created_by',)


class FormTemplateCreateSerializer(serializers.ModelSerializer):
    fields = FormFieldSerializer(many=True)

    class Meta:
        model = FormTemplate
        fields = ('id', 'name', 'description', 'fields')

    def create(self, validated_data):
        fields_data = validated_data.pop('fields')
        form_template = FormTemplate.objects.create(**validated_data)
        
        for field_data in fields_data:
            FormField.objects.create(form_template=form_template, **field_data)
        
        return form_template

    def update(self, instance, validated_data):
        fields_data = validated_data.pop('fields', None)
        
        instance.name = validated_data.get('name', instance.name)
        instance.description = validated_data.get('description', instance.description)
        instance.save()

        if fields_data is not None:
            # Delete existing fields and create new ones
            instance.fields.all().delete()
            for field_data in fields_data:
                FormField.objects.create(form_template=instance, **field_data)

        return instance


class EmployeeSerializer(serializers.ModelSerializer):
    form_template = FormTemplateSerializer(read_only=True)
    form_template_id = serializers.IntegerField(write_only=True)
    created_by = UserSerializer(read_only=True)

    class Meta:
        model = Employee
        fields = '__all__'
        read_only_fields = ('created_by',)