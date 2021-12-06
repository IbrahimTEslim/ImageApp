import os
from django.http.response import HttpResponseNotFound, JsonResponse
# from django.shortcuts import render
from .models import Images,User
from django.http import HttpResponse,FileResponse
from django.db.utils import IntegrityError
from django.contrib.auth import login as log_in, logout as log_out

import mimetypes
import hashlib
import os
import zipfile

# Create your views here.


def register(request):
    if request.method == 'POST':
        if 'username' in request.headers:
            usern = request.headers['username']
            if not usern:
                return HttpResponse("Not Allowed Null Values for users names")
        else:
            return HttpResponse("Can't see a username")
        if 'password' in request.headers:
            pasw = request.headers['password']
        else:
            return HttpResponse("can't see a password")
        if 'email' in request.headers:
            email = request.headers['email']
        else:
            email = None

        m= hashlib.sha256()
        m.update(pasw.encode('utf-8'))
        pasw = m.hexdigest()

        try:
            user = User.objects.create(username=usern,password=pasw,email=email,is_staff=False)
        except IntegrityError:
            return HttpResponse("This username is already used\nchange username")
        print("\n\nuser Created: ",user,"\n\n")
        log_in(request,user)
        return HttpResponse("Registerd OK")
    else:
        return HttpResponse('send your info to register ^_^')


def login(request):
    if request.method == 'POST':
        if 'username' not in request.headers or 'password' not in request.headers:
            return HttpResponse('Bad request for logging in')
        usern = request.headers['username']
        pasw = request.headers['password']
        # print("\n",usern,"\n",pasw)
        m = hashlib.sha256()
        m.update(pasw.encode())
        pasw = m.hexdigest()
        try:
            user = User.objects.get(username=usern,password=pasw)
        except:
            user = None
        if user is not None:
            log_in(request,user)
            request.session.modified = True
            return HttpResponse("Logged In :}")
        else:
            return HttpResponse("Can't log in :{")
    else:
        return HttpResponse("Send your Login Credentials")


def logout(request):
    log_out(request)
    return HttpResponse("Logged Out nn")



def add_image(request):
    if request.method == "POST":
        mimetypes.init()
        user = User.objects.get(pk=request.session['_auth_user_id'])
        image = request.FILES['image']
        for file in request.FILES.getlist('image'):
            Images.objects.create(user = user,image = file)
        return HttpResponse("Added Successfully")


def test(request):
    if request.method == "GET":
        try:
            entry = Images.objects.get(pk=25)
            print("\n\n",entry.image,"\n\n")
            path = os.path.join(os.path.dirname(os.path.dirname(__file__)),f'Image/{entry.image}')

            f = open(path,'rb')

            file_name = os.path.basename(path)
            mime_type = mimetypes.guess_type(file_name)

            if mime_type is not None:
                response = HttpResponse(f.read())
            response['Content-Disposition'] = 'inline; filename=' + file_name
            response['Content-Type'] = mime_type[0]
        except IOError:
            response = HttpResponseNotFound()
    return response


def show(request,image_id):
    # user = User.objects.get(pk=request.session['_auth_user_id'])
    image = Images.objects.get(pk = image_id)
    try:
        
        path = os.path.join(os.path.dirname(os.path.dirname(__file__)),f'Image/{image.image}')
        print("\n\n",path,"\n")
        f = open(path,'rb')
        
        file_name = os.path.basename(path)
        mime_type = mimetypes.guess_type(file_name)

        if mime_type is not None:
            response = HttpResponse(f.read())
        response['Content-Disposition'] = 'inline; filename=' + file_name
        response['Content-Type'] = mime_type[0]
    except IOError:
        response = HttpResponseNotFound()
    return response


def get_all(request):
    user = User.objects.get(pk=request.session['_auth_user_id'])
    images_names_db = list(Images.objects.all().filter(user = user,is_deleted=0).values('image').order_by('added_at'))
    images_names = []
    for entry in images_names_db:
        images_names.append("Image/"+entry['image'])
    with zipfile.ZipFile('zzip.zip','w') as zip:
        for filename in images_names:
            zip.write(filename)
    f = open('zzip.zip','rb')
    mime_type = mimetypes.guess_type('zzip.zip')
    response = HttpResponse(f.read())
    response['Content-Disposition'] = 'inline; filename=' + 'zzip.zip'
    response['Content-Type'] = mime_type[0]
    return response


def delete(request,image_id):
    user = User.objects.get(pk=request.session['_auth_user_id'])
    try:
        image = Images.objects.get(user = user,pk = image_id)
        image.is_deleted = 1
        image.save()
    except Images.DoesNotExist:
        return HttpResponse("Thats illegal (:>")


def delete_all(request):
    user = User.objects.get(pk = request.session['_auth_user_id'])
    Images.objects.filter(user = user, is_deleted = 0).update(is_deleted = 1)
    return HttpResponse("Deleted All Successfully")
    















































