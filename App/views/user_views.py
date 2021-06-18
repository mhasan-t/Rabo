
from App.utils.login_required import login_required_project_admin
from django.http.response import HttpResponse, HttpResponseRedirect
from django.views.generic import View
from django.shortcuts import render, redirect
from django.db import connection
from django.urls import reverse
from django.core.files.storage import default_storage
from django.conf import settings
from django.core.files.base import ContentFile
from django.db import IntegrityError

import os
import pathlib
import json
import uuid
import datetime
import pytz
import bcrypt

from ..forms import CreateUserForm, LoginUserForm
from ..utils import login_required_user


class CreateUser(View):
    def get(self, request):
        sid = request.COOKIES.get('session_id')
        if sid:
            query = f'''
                SELECT user_id FROM sessions
                WHERE session_id = "{sid}"
            '''
        
            with connection.cursor() as cursor:
                sid_valid  = cursor.execute(query)

                if sid_valid==1:
                    return HttpResponseRedirect(reverse('dashboard'))
                else:
                    resp = HttpResponseRedirect(reverse('sign-up'))
                    resp.delete_cookie("session_id")
                    return resp;

        form = CreateUserForm()
        context_data = {
            'form': form
        }
        return render(request=request, template_name="user_signup.html", context=context_data)

    def post(self, request):

        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        email = request.POST.get("email")
        password = request.POST.get("password").encode('utf-8')
        hashed_pass = bcrypt.hashpw(password, bcrypt.gensalt())
        form = CreateUserForm(request.POST)
        if form.is_valid():

            DTZ = pytz.timezone("Asia/Dhaka")
            created_dt = datetime.datetime.now(DTZ)

            query = f"""
                INSERT INTO user(first_name, last_name, email, password, picture , created_at) VALUES(
                    "{str(first_name)}" ,
                    "{str(last_name)}" ,
                    "{str(email)}",
                    "{hashed_pass.decode('utf-8')}",
                    "default.png",
                    "{str(created_dt.strftime('%Y:%m:%d %H:%M:%S'))}"
                )
            """
            with connection.cursor() as cursor:
                try:
                    res = cursor.execute(query)
                except IntegrityError as e:
                    context_data = {
                        'form': form,
                        'error_msg': "E-mail already exists!"
                    }
                    return render(request=request, template_name="user_signup.html", context=context_data)
                return redirect('log-in')


        else:
            form = CreateUserForm()
            context_data = {
                'error_msg': 'Password does not match.',
                'form': form
            }
            return render(request=request, template_name="user_signup.html", context=context_data)


class LoginUser(View):
    def get(self, request):
        sid = request.COOKIES.get('session_id')
        if sid:
            query = f'''
                SELECT user_id FROM sessions
                WHERE session_id = "{sid}"
            '''
        
            with connection.cursor() as cursor:
                sid_valid  = cursor.execute(query)

                if sid_valid==1:
                    return HttpResponseRedirect(reverse('dashboard'))
                else:
                    resp = HttpResponseRedirect(reverse('log-in'))
                    resp.delete_cookie("session_id")
                    return resp;

        form = LoginUserForm()
        context_data = {
            'form': form
        }
        return render(request=request, template_name="user_login.html", context=context_data)

    def post(self, request):
        email = request.POST.get("email")
        password = request.POST.get("password").encode('utf-8')
        form = LoginUserForm(request.POST)

        if form.is_valid():
            with connection.cursor() as cursor:
                user_exists = cursor.execute(f'''
                    SELECT id,password FROM `user`
                    WHERE email = "{email}"
                ''')

                res = cursor.fetchone()
                hashedpass_from_db = str(res[1]).encode(
                    "utf-8") if user_exists == 1 else ""

                if user_exists == 0 or not bcrypt.checkpw(password=password,
                                                          hashed_password=hashedpass_from_db):
                    form = LoginUserForm()
                    context_data = {
                        'form': form,
                        'error_msg': "Wrong E-mail or password"
                    }
                    return render(request=request, template_name="user_login.html", context=context_data)
                else:
                    user_id = res[0]
                    sid = uuid.uuid1()
                    DTZ = pytz.timezone("Asia/Dhaka")
                    created_dt = datetime.datetime.now(DTZ)
                    cursor.execute(f'''
                        INSERT INTO sessions(session_id, created_at, user_id) VALUES(
                            "{sid}",
                            "{created_dt}",
                            "{user_id}"
                        )
                    ''')

                    resp = HttpResponseRedirect(reverse('dashboard'))
                    resp.set_cookie("session_id", sid, max_age=9999)
                    return resp;


class EditUser(View):
    @login_required_user
    def post(self, request, user_id):
        # post_data = json.loads(request.body.decode("utf-8"))
        # field = post_data.get('field')
        # data = post_data.get('data')

        field = request.POST.get('field')
        data = request.POST.get('data')

        if(data==""):
            return HttpResponse()
        
        if field=="picture":
            image_file = request.FILES.get("pic")
            path = default_storage.save("profile_pics/picture.jpeg", ContentFile(image_file.read()))
            tmp_file = os.path.join(settings.MEDIA_ROOT, path)
            data = tmp_file.split("/")[1]


        if field=="password":
            data = bcrypt.hashpw(data.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')


        query = f'''
            UPDATE user
            SET {field}="{data}"
            WHERE id={user_id}
        '''
        
        with connection.cursor() as cursor:
            res = cursor.execute(query)
            if res and field=="picture":
                return HttpResponse(reverse("dashboard"))
            if res:
                return HttpResponse(status=200)
        
        return HttpResponse(status=500)


class DeleteUser(View):
    @login_required_user
    def post(self, request, user_id):
        query = f'''
            DELETE FROM user
            WHERE id = {user_id}
        '''

        with connection.cursor() as cursor:
            res = cursor.execute(query)
            if res:
                return HttpResponse(status=200)
        
        return HttpResponse(status=500)

