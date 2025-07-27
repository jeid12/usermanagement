from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from .models import Product
from .forms import ProductForm
from .decolators import editors_decorator,delete_decorator,add_decorator

@login_required
def product_list(request):
    """Display all products for the current user"""
    # Fetch products for the logged-in user
    if not request.user.role=='seller':
        products = Product.objects.all().order_by('-created_at')

    else:    
         products = Product.objects.filter(user=request.user).order_by('-created_at')
    
    # Pagination
    paginator = Paginator(products, 12)  # Show 12 products per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    return render(request, 'product/product_list.html', {'page_obj': page_obj})

@login_required
@add_decorator
def add_product(request):
    """Add a new product"""
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, user=request.user)
        if form.is_valid():
            product = form.save()
            messages.success(request, f'Product "{product.name}" was added successfully!')
            return redirect('product_list')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = ProductForm(user=request.user)
    
    return render(request, 'product/add_product.html', {'form': form})

@login_required
@editors_decorator
def edit_product(request, product_id):
    """Edit an existing product"""
    product = get_object_or_404(Product, id=product_id, user=request.user)
    
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product, user=request.user)
        if form.is_valid():
            updated_product = form.save()
            messages.success(request, f'Product "{updated_product.name}" was updated successfully!')
            return redirect('product_list')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = ProductForm(instance=product, user=request.user)
    
    return render(request, 'product/edit_product.html', {'form': form, 'product': product})

@login_required
@delete_decorator
def delete_product(request, product_id):
    """Delete a product"""
    product = get_object_or_404(Product, id=product_id, user=request.user)
    
    if request.method == 'POST':
        product_name = product.name
        product.delete()
        messages.success(request, f'Product "{product_name}" was deleted successfully!')
        return redirect('product_list')
    
    return render(request, 'product/delete_product.html', {'product': product})

@login_required
def product_detail(request, product_id):
    """View product details (public view)"""
    product = get_object_or_404(Product, id=product_id)
    return render(request, 'product/product_detail.html', {'product': product})
