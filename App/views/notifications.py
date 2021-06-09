from App.utils import login_required_project_admin, login_required_user
from django.db import connection
from django.http.response import HttpResponse, HttpResponseRedirect
from django.views.generic import View
from django.shortcuts import render
from django.urls import reverse

import json
import pytz
import datetime


class SendNotification(View):
    @login_required_project_admin
    def post(self, request, user_id, pid):
        post_data = json.loads(request.body.decode("utf-8"))
        type = post_data.get("type")
        sent_to = post_data.get("sent_to")
        data = post_data.get("data")
        
        DTZ = pytz.timezone("Asia/Dhaka")
        created_dt = datetime.datetime.now(DTZ)

        if type=='invite':
            query = f'''
                INSERT INTO notification(data, created_at, type, sent_to, sent_by, project_id)
                VALUES( 
                    "",
                    '{created_dt.strftime('%Y:%m:%d %H:%M:%S')}',
                    '{type}',
                    '{sent_to}',
                    '{user_id}',
                    '{pid}'
                 )
            '''
            # print(query)
            with connection.cursor() as cursor:
                cursor.execute(query)
                return HttpResponse()


class AcceptInvitation(View):
    @login_required_user
    def get(self, request, user_id):
        noti_id = request.GET.get("noti_id")

        with connection.cursor() as cursor:
            cursor.execute(f'''
                SELECT sent_to, project_id FROM notification WHERE id={noti_id}
            ''')

            res = cursor.fetchone()

            sent_to = res[0]
            if sent_to != user_id:
                return HttpResponse("Unauthorized")

            cursor.execute(f'''
                INSERT INTO works_on(project_id, user_id, role)
                VALUES(
                    '{res[1]}',
                    '{res[0]}',
                    'employee'
                )
            ''')

            cursor.execute(f'''
                DELETE FROM notification WHERE id={noti_id}
            ''')

            return HttpResponse()

class RejectInvitation(View):
    @login_required_user
    def get(self, request, user_id):
        noti_id = request.GET.get("noti_id")

        with connection.cursor() as cursor:
            cursor.execute(f'''
                SELECT sent_by, project_id, sent_to FROM notification WHERE id={noti_id}
            ''')
            res = cursor.fetchone()
            sent_by = res[0]
            project_id = res[1]
            sent_to = res[2]

            if sent_to != user_id:
                return HttpResponse("Unauthorized")

            cursor.execute(f'''
                SELECT first_name, last_name FROM user WHERE id={sent_to}
            ''')
            res = cursor.fetchone()
            sent_to_name = res[0]+ " " + res[1]

            cursor.execute(f'''
                SELECT name FROM project WHERE id={project_id}
            ''')
            proj_name = cursor.fetchone()[0]


            DTZ = pytz.timezone("Asia/Dhaka")
            created_dt = datetime.datetime.now(DTZ)

            query = f'''
                INSERT INTO notification(data, created_at, type, sent_to, sent_by, project_id)
                VALUES( 
                    "{str(sent_to_name)} has rejected your invitaion to {str(proj_name)}",
                    '{created_dt.strftime('%Y:%m:%d %H:%M:%S')}',
                    'info',
                    '{sent_by}',
                    '{user_id}',
                    '{project_id}'
                 )
            '''
            # print(query)
            cursor.execute(query)

            query=f'''
                DELETE FROM notification WHERE id={noti_id}
            '''
            # print(query)
            cursor.execute(query)

            return HttpResponse()


