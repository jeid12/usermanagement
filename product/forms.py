from django import forms
from .models import Product

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'description', 'price', 'image']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'w-full px-4 py-3 rounded-lg border border-gray-300 focus:ring-2 focus:ring-green-500 focus:border-transparent transition duration-300 ease-in-out bg-white text-gray-900 placeholder-gray-500 shadow-sm hover:border-gray-400',
                'placeholder': 'Enter product name'
            }),
            'description': forms.Textarea(attrs={
                'class': 'w-full px-4 py-3 rounded-lg border border-gray-300 focus:ring-2 focus:ring-green-500 focus:border-transparent transition duration-300 ease-in-out bg-white text-gray-900 placeholder-gray-500 shadow-sm hover:border-gray-400 resize-vertical',
                'placeholder': 'Describe your product...',
                'rows': 4
            }),
            'price': forms.NumberInput(attrs={
                'class': 'w-full px-4 py-3 rounded-lg border border-gray-300 focus:ring-2 focus:ring-green-500 focus:border-transparent transition duration-300 ease-in-out bg-white text-gray-900 placeholder-gray-500 shadow-sm hover:border-gray-400',
                'placeholder': '0.00',
                'step': '0.01',
                'min': '0'
            }),
            'image': forms.ClearableFileInput(attrs={
                'class': 'w-full px-4 py-3 rounded-lg border border-gray-300 focus:ring-2 focus:ring-green-500 focus:border-transparent transition duration-300 ease-in-out bg-white text-gray-900 file:mr-4 file:py-2 file:px-4 file:rounded-full file:border-0 file:text-sm file:font-semibold file:bg-green-50 file:text-green-700 hover:file:bg-green-100 cursor-pointer shadow-sm hover:border-gray-400',
                'multiple': False,
                'accept': 'image/*'
            })
        }
        labels = {
            'name': 'Product Name',
            'description': 'Product Description',
            'price': 'Price ($)',
            'image': 'Product Image'
        }
        help_texts = {
            'name': 'Enter a unique and descriptive name for your product',
            'description': 'Provide detailed information about your product',
            'price': 'Set the price in USD (e.g., 29.99)',
            'image': 'Upload a high-quality image of your product (JPG, PNG, etc.)'
        }
    
    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        
        # Add required field indicators
        for field_name, field in self.fields.items():
            if field.required:
                field.widget.attrs['required'] = True
    
    def clean_price(self):
        price = self.cleaned_data.get('price')
        if price is not None and price <= 0:
            raise forms.ValidationError("Price must be greater than zero.")
        return price
    
    def clean_image(self):
        image = self.cleaned_data.get('image')
        if image:
            # Check file size (limit to 5MB)
            if image.size > 5 * 1024 * 1024:
                raise forms.ValidationError("Image file size must be less than 5MB.")
            
            # Check file type
            allowed_types = ['image/jpeg', 'image/jpg', 'image/png', 'image/webp']
            if hasattr(image, 'content_type') and image.content_type not in allowed_types:
                raise forms.ValidationError("Only JPEG, PNG, and WebP images are allowed.")
        
        return image
    
    def save(self, commit=True):
        product = super().save(commit=False)
        if self.user:
            product.user = self.user
        if commit:
            product.save()
        return product