from django.shortcuts import render, redirect, get_object_or_404 
from django.contrib import messages
from django.core.exceptions import PermissionDenied

from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from django.contrib.auth.models import User

from .forms import UserRegisterForm
from .serializer import UserSerializer

# Create your views here.

def register(request):
    # TODO https://docs.djangoproject.com/en/4.0/ref/views/#the-403-http-forbidden-view
    raise PermissionDenied # temporarily suspending sign ups as the system is still on the internet even during development

    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Your account has been created! You can now login... ')
            return redirect('user:login')
    else:
        form = UserRegisterForm()
    return render(request, 'registration/login.html' , {'f_register': form} )

# USERS

def users(request):
    return render( request, 'user/restapi.html')

def users_form(request, user_id=None):
    try:
        user = User.objects.get(pk=user_id)
    except User.DoesNotExist:
        user = None

    return render( request, 'user/update.html', {'system_user': user})

def users_create(request, user_id=None):
    if request.method == 'POST':
        f = UserRegisterForm(request.POST)
        if f.is_valid():
            f.save()
            return redirect('user:users')
    else:
        f = UserRegisterForm()
    return render( request, 'user/create.html',{'form':f})

    

def users_update(request, user_id=None):
    user = get_object_or_404(User, pk=user_id)

    if request.method == 'POST':
        # https://docs.djangoproject.com/en/4.0/topics/forms/modelforms/#the-save-method
        # Create a form to edit an existing Article, but use
        # POST data to populate the form.
        f = UserRegisterForm(request.POST, instance=user)
        if f.is_valid():
            f.save()
    else:
        f = UserRegisterForm(instance=user)

    return render( request, 'user/update.html', {'user': user, 'form':f})

def users_delete(request, user_id):
    user = get_object_or_404(User, pk=user_id)
    if request.method == 'POST':
        user.delete()
        return redirect('user:users')

    return render( request, 'user/confirm.html')

@api_view(['GET', 'POST'])
def user_list(request, format=None):
    """
    List all users, or create a new user.
    """
    if request.method == 'GET':
        users = User.objects.all()
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'PUT', 'DELETE'])
def user_detail(request, pk, format=None):
    """
    Retrieve, update or delete a user.
    """
    try:
        user = User.objects.get(pk=pk)
    except User.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = UserSerializer(user)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = UserSerializer(user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
    
