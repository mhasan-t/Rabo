from django.views.generic import View
from django.shortcuts import render
from django.db import connection

import uuid
import datetime
import pytz
import bcrypt

from ..forms import CreateUserForm, LoginUserForm
from ..utils import login_required


class CreateUser(View):
    def get(self, request):
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
                INSERT INTO user(first_name, last_name, email, password, created_at) VALUES(
                    "{str(first_name)}" ,
                    "{str(last_name)}" ,
                    "{str(email)}",
                    "{hashed_pass.decode('utf-8')}",
                    "{str(created_dt.strftime('%Y:%m:%d %H:%M:%S'))}"
                )
            """
            print(query)
            with connection.cursor() as cursor:
                cursor.execute(query)
        else:
            form = CreateUserForm()
            context_data = {
                'error_msg': 'Password does not match.',
                'form': form
            }
            return render(request=request, template_name="user_signup.html", context=context_data)


class LoginUser(View):
    def get(self, request):
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
