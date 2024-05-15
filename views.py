from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.views.decorators.http import require_POST
import json

from django.http import JsonResponse
from django.conf import settings
import os

from django.contrib import messages


from .models import adfs
from .models import AdminUser
from .models import teachers

from django.core.files.uploadedfile import UploadedFile
from PIL import Image
from io import BytesIO

import logging
logger = logging.getLogger(__name__)

# Create your views here.

def home(request):
    return render(request, 'home.html')

def signup(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        
        # Assuming the user is an admin if their email contains '@fsadmin.com'
        is_admin = '@fsadmin.com' in email
        is_teacher = '@fsteacher.com' in email
        
        # Save user to the appropriate model based on admin status
        if is_admin:
            AdminUser.objects.create(username=username, password=password)
        elif is_teacher:
            adfs.objects.create(username=username, email=email, password=password)
        else:
            # Save to regular user model
            adfs.objects.create(username=username, email=email, password=password)
            
        
        return redirect('home')  
    return render(request, 'signup.html')

def login(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        
        # Check if the user exists and if the email contains '@fsadmin.com'
        user_exists = adfs.objects.filter(email=email, password=password).exists()
        if user_exists:
            if '@fsadmin.com' in email:  # Check if the email is for admin
                return redirect('manageadmins')  # Redirect admin to manageadmins page
            elif '@fsteacher.com' in email: 
                return redirect('manageteachers') #Redirect teacher to manageteachers page
            else:
                return redirect('home')  # Redirect normal user to home page
        else:
            return render(request, 'login.html', {'error': 'Invalid email or password'})
    return render(request, 'login.html')

# Manage admins,students,teachers page - only accessible by users who are admins
def manageadmins(request):
    admin_users = AdminUser.objects.all()  # Retrieve all admin users
    return render(request, 'manageadmins.html', {'admin_users': admin_users})

def manageusers(request):
    childdata = adfs.objects.all()  # Retrieve all student users
    print(childdata)  # Check if childdata contains data
    return render(request, 'manageusers.html', {'childdata': childdata})


#manage teacher content 
def manageteachers(request):
    carddata = teachers.objects.all()
    return render (request,  'manageteachers.html', {'carddata': carddata})

#-------

#delete teacher/character cards
@require_POST
def delete_teacher(request, teacher_id):
    teacher = get_object_or_404(teachers, id=teacher_id)
    try:
        if teacher.image:
            teacher.image.delete(save=True)
        teacher.delete()
        return JsonResponse({'success': True})
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=400)

#delete user

def delete_user(request, user_id):
    if adfs.objects.filter(id=user_id).exists():
        user = get_object_or_404(adfs, id=user_id)
        user.delete()
  
    return redirect('manageusers')  # Redirect to appropriate page after deletion

#delete admin
def delete_admin(request, user_id):
    if AdminUser.objects.filter(id=user_id).exists():
        admin_user = get_object_or_404(AdminUser, id=user_id)
        admin_user.delete()
    return redirect('manageadmins')

#edit account

def edit_user(request, user_id):
    user = get_object_or_404(adfs, id=user_id)  # Get the specific user by ID
    return render(request, 'editusers.html', {'child_data': user})
def edit_admin(request, admin_id):
    admin = get_object_or_404(AdminUser, id=admin_id)  # Get the specific admin by ID
    return render(request, 'editadmin.html', {'admin_user': admin})


#update user

@require_POST
def update_user(request, user_id):
    try:
        user = adfs.objects.get(id=user_id)  # Simplify for one model for clarity
        user.username = request.POST.get('username')
        user.password = request.POST.get('password')
        user.email = request.POST.get('email')
        user.save()
        return JsonResponse({'success': True, 'redirect_url': '/manageusers/'})
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=400)
    
#update admin
@require_POST
def update_admin(request, user_id):
    try:
        user = AdminUser.objects.get(id=user_id)  # Simplify for one model for clarity
        user.username = request.POST.get('username')
        user.password = request.POST.get('password')
        user.save()
        return JsonResponse({'success': True, 'redirect_url': '/manageadmins/'})
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=400)


#content

#i hope to god this works

def add_teacher(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        image = request.FILES.get('image')
        if name and image:
            try:
                img = Image.open(image)
                if img.width < 200 or img.height <= 200:
                    messages.error(request, "Error: Image must be at least 200x200 pixels.")
                else:
                    new_teacher = teachers(name=name, image=image)
                    new_teacher.save()
                    messages.success(request, "Teacher added successfully!")
            except Exception as e:
                messages.error(request, f"Error: {e}")
        else:
            messages.error(request, "Error: Name and image are required.")
        return redirect('manageteachers')
    return redirect('home')

#update teacher card




def edit_tcards(request, cardid):
    card = teachers.objects.get(id=cardid)
    return render(request, 'teachercards.html', {'carddata': card})
    


@require_POST
def update_tcards(request, cardid):
    try:
        card = teachers.objects.get(id=cardid)
        card.name = request.POST.get('name')
        
        # Check if a new image is provided
        new_image = request.FILES.get('image')
        if new_image:
            # Open the image file using PIL
            pil_image = Image.open(BytesIO(new_image.read()))
            
            # Get the dimensions of the image
            image_width, image_height = pil_image.size
            
            # Check if the image meets the size requirement
            if image_width < 200 or image_height < 200:
                return JsonResponse({'success': False, 'error': 'Image must be at least 200x200 pixels.'}, status=400)
            else:
                # Update the image if it meets the requirements
                card.image = new_image
        
        card.save()
        return JsonResponse({'success': True, 'redirect_url': '/manageteachers/'})
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=400)