# Debug script to test image upload functionality
# Run this script from the Django shell to verify image uploads work

from accounts.models import User
from accounts.forms import UserRegistrationForm
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import RequestFactory
import os

def test_image_upload():
    """Test image upload functionality"""
    
    # Create a simple test image file
    image_content = b'\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x01\x00\x00\x00\x01\x08\x02\x00\x00\x00\x90wS\xde\x00\x00\x00\tpHYs\x00\x00\x0b\x13\x00\x00\x0b\x13\x01\x00\x9a\x9c\x18\x00\x00\x00\nIDATx\x9cc\xf8\x0f\x00\x00\x01\x00\x01\x00\x18\xdd\x8d\xb4\x1c\x00\x00\x00\x00IEND\xaeB`\x82'
    
    test_image = SimpleUploadedFile(
        name='test_profile.png',
        content=image_content,
        content_type='image/png'
    )
    
    # Create form data
    form_data = {
        'username': 'testuser_debug',
        'email': 'test@example.com',
        'password': 'testpassword123',
        'password_confirm': 'testpassword123',
        'first_name': 'Test',
        'last_name': 'User',
        'phone_number': '1234567890',
        'role': 'customer',
        'is_active': True
    }
    
    # Test form with file
    form = UserRegistrationForm(data=form_data, files={'profile_picture': test_image})
    
    if form.is_valid():
        user = form.save()
        print(f"✅ User created successfully: {user.username}")
        print(f"✅ Profile picture path: {user.profile_picture}")
        print(f"✅ Full file path: {user.profile_picture.path if user.profile_picture else 'No image'}")
        
        # Check if file exists
        if user.profile_picture and os.path.exists(user.profile_picture.path):
            print(f"✅ Image file exists at: {user.profile_picture.path}")
        else:
            print("❌ Image file not found on disk")
            
        return user
    else:
        print("❌ Form validation failed:")
        for field, errors in form.errors.items():
            print(f"  {field}: {errors}")
        return None

# Instructions to run this test:
# 1. Open Django shell: python manage.py shell
# 2. exec(open('debug_image_upload.py').read())
# 3. test_image_upload()
