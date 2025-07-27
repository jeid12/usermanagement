from django import forms
from django.contrib.auth.hashers import make_password
from .models import User

class UserRegistrationForm(forms.ModelForm):
    password_confirm = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'w-full px-4 py-3 rounded-lg border border-gray-300 focus:ring-2 focus:ring-blue-500 focus:border-transparent transition duration-300 ease-in-out bg-white text-gray-900 placeholder-gray-500 shadow-sm hover:border-gray-400',
            'placeholder': 'Confirm your password'
        }),
        label='Confirm Password'
    )
    
    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'password_confirm', 'first_name', 'last_name', 'phone_number', 'profile_picture', 'role', 'is_active']
        widgets = {
            'username': forms.TextInput(attrs={
                'class': 'w-full px-4 py-3 rounded-lg border border-gray-300 focus:ring-2 focus:ring-blue-500 focus:border-transparent transition duration-300 ease-in-out bg-white text-gray-900 placeholder-gray-500 shadow-sm hover:border-gray-400',
                'placeholder': 'Enter your username'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'w-full px-4 py-3 rounded-lg border border-gray-300 focus:ring-2 focus:ring-blue-500 focus:border-transparent transition duration-300 ease-in-out bg-white text-gray-900 placeholder-gray-500 shadow-sm hover:border-gray-400',
                'placeholder': 'Enter your email address'
            }),
            'password': forms.PasswordInput(attrs={
                'class': 'w-full px-4 py-3 rounded-lg border border-gray-300 focus:ring-2 focus:ring-blue-500 focus:border-transparent transition duration-300 ease-in-out bg-white text-gray-900 placeholder-gray-500 shadow-sm hover:border-gray-400',
                'placeholder': 'Create a strong password'
            }),
            'first_name': forms.TextInput(attrs={
                'class': 'w-full px-4 py-3 rounded-lg border border-gray-300 focus:ring-2 focus:ring-blue-500 focus:border-transparent transition duration-300 ease-in-out bg-white text-gray-900 placeholder-gray-500 shadow-sm hover:border-gray-400',
                'placeholder': 'Enter your first name'
            }),
            'last_name': forms.TextInput(attrs={
                'class': 'w-full px-4 py-3 rounded-lg border border-gray-300 focus:ring-2 focus:ring-blue-500 focus:border-transparent transition duration-300 ease-in-out bg-white text-gray-900 placeholder-gray-500 shadow-sm hover:border-gray-400',
                'placeholder': 'Enter your last name'
            }),
            'phone_number': forms.TextInput(attrs={
                'class': 'w-full px-4 py-3 rounded-lg border border-gray-300 focus:ring-2 focus:ring-blue-500 focus:border-transparent transition duration-300 ease-in-out bg-white text-gray-900 placeholder-gray-500 shadow-sm hover:border-gray-400',
                'placeholder': 'Enter your phone number'
            }),
            'profile_picture': forms.ClearableFileInput(attrs={
                'class': 'w-full px-4 py-3 rounded-lg border border-gray-300 focus:ring-2 focus:ring-blue-500 focus:border-transparent transition duration-300 ease-in-out bg-white text-gray-900 file:mr-4 file:py-2 file:px-4 file:rounded-full file:border-0 file:text-sm file:font-semibold file:bg-blue-50 file:text-blue-700 hover:file:bg-blue-100 cursor-pointer shadow-sm hover:border-gray-400',
                'multiple': False,
                'accept': 'image/*'
            }),
            'role': forms.Select(attrs={
                'class': 'w-full px-4 py-3 rounded-lg border border-gray-300 focus:ring-2 focus:ring-blue-500 focus:border-transparent transition duration-300 ease-in-out bg-white text-gray-900 shadow-sm hover:border-gray-400 cursor-pointer'
            }),
            'is_active': forms.CheckboxInput(attrs={
                'class': 'w-4 h-4 text-blue-600 border-gray-300 rounded focus:ring-blue-500 dark:focus:ring-blue-600 dark:ring-offset-gray-800',
            })
        }
    
    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        password_confirm = cleaned_data.get('password_confirm')
        
        if password and password_confirm:
            if password != password_confirm:
                raise forms.ValidationError("Passwords don't match.")
        
        return cleaned_data
    
    def save(self, commit=True):
        user = super().save(commit=False)
        # Hash the password properly
        user.password = make_password(self.cleaned_data['password'])
        if commit:
            user.save()
        return user

class UserLoginForm(forms.Form):
    username = forms.CharField(
        max_length=150, 
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'w-full px-4 py-3 rounded-lg border border-gray-300 focus:ring-2 focus:ring-blue-500 focus:border-transparent transition duration-300 ease-in-out bg-white text-gray-900 placeholder-gray-500 shadow-sm hover:border-gray-400',
            'placeholder': 'Enter your username'
        })
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'w-full px-4 py-3 rounded-lg border border-gray-300 focus:ring-2 focus:ring-blue-500 focus:border-transparent transition duration-300 ease-in-out bg-white text-gray-900 placeholder-gray-500 shadow-sm hover:border-gray-400',
            'placeholder': 'Enter your password'
        }), 
        required=True
    )