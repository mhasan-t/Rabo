
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
from ..utils import *



class SearchUserForInvite(View):
    @login_required_project_admin
    def get(self, request, user_id, pid):
        searchQ = request.GET.get("query")

        query = f'''
            SELECT id, first_name, last_name FROM `user`
            WHERE ( first_name LIKE "%{searchQ}%"
                OR last_name LIKE "%{searchQ}%" )
                AND
                id != ALL (
                    SELECT sent_to FROM notification
                    WHERE type='invite' AND project_id={pid}
                )
                AND
                id != ALL (
                    SELECT user_id FROM works_on WHERE project_id={pid}
                )
        '''


        with connection.cursor() as cursor:
            res = cursor.execute(query)

            desc = cursor.description

            resDict = [dict(zip([col[0] for col in desc], row)) 
                for row in cursor.fetchall() ]

            # print(resDict)

            json_data = json.dumps(resDict)
            print(json_data)

            if res:
                return HttpResponse(json_data, content_type="application/json")
        
        return HttpResponse(status=500)


class ShowUsersToAssign(View):
    @login_required_project_admin
    def get(self, request, user_id, pid):
        searchQ = request.GET.get("query")

        query = f'''
            SELECT id, first_name, last_name FROM `user`
            WHERE ( first_name LIKE "%{searchQ}%"
                OR last_name LIKE "%{searchQ}%" )
                AND id= ANY (
                    SELECT user_id FROM works_on WHERE project_id={pid}
                )
                AND id!={user_id}
                
        '''


        with connection.cursor() as cursor:
            res = cursor.execute(query)

            desc = cursor.description

            resDict = [dict(zip([col[0] for col in desc], row)) 
                for row in cursor.fetchall() ]

            # print(resDict)

            json_data = json.dumps(resDict)

            if res:
                return HttpResponse(json_data, content_type="application/json")
        
        return HttpResponse(status=500)


class ShowManagers(View):
    @login_required_task
    def get(self, request, user_id, pid, taskid):
        searchQ = request.GET.get("query")
        # print(searchQ)

        query = f'''
            SELECT id, first_name, last_name FROM `user`
            WHERE ( first_name LIKE "%{searchQ}%"
                OR last_name LIKE "%{searchQ}%" )
                AND
                id != (
                    SELECT managed_by FROM task
                    WHERE id={taskid}
                )
                AND
                id = ANY (
                    SELECT user_id FROM works_on WHERE project_id={pid}
                )
                AND id!={user_id}
        '''

        # print(query)
        with connection.cursor() as cursor:
            cursor.execute(f'''
                SELECT managed_by FROM task WHERE id={taskid}
            ''')
            if cursor.fetchone()[0] is None:
                query = f'''
                    SELECT id, first_name, last_name FROM `user`
                    WHERE ( first_name LIKE "%{searchQ}%"
                        OR last_name LIKE "%{searchQ}%" )
                '''


            res = cursor.execute(query)

            desc = cursor.description

            resDict = [dict(zip([col[0] for col in desc], row)) 
                for row in cursor.fetchall() ]

            # print(resDict)

            json_data = json.dumps(resDict)

            if res:
                return HttpResponse(json_data, content_type="application/json")
        
        return HttpResponse(status=500)





class ShowCategories(View):
    @login_required_project_admin
    def get(self, request, user_id, pid):
        searchQ = request.GET.get("query")

        query = f'''
            SELECT category FROM task WHERE project_id={pid}
            GROUP BY category
        '''

        print(query)
        with connection.cursor() as cursor:
            res = cursor.execute(query)

            json_data = json.dumps(cursor.fetchall())

            if res:
                return HttpResponse(json_data, content_type="application/json")
        
        return HttpResponse(status=500)


class ShowTasksForDependency(View):
    @login_required_task_manager
    def get(self, request, user_id, pid, taskid):
        searchQ = request.GET.get("query")


        query = f'''
            SELECT id, label,
                CASE WHEN id=ANY (
                    SELECT independent FROM task_dependency WHERE dependent={taskid}
                )
                THEN true ELSE false END as isSuperior

            FROM task
            WHERE project_id = {pid} AND id!={taskid}
                AND label LIKE '%{searchQ}%'

        '''

       

        # print(query)
        with connection.cursor() as cursor:
            res = cursor.execute(query)
            
            json_data = json.dumps(cursor.fetchall())

            if res:
                return HttpResponse(json_data, content_type="application/json")
        
        return HttpResponse(status=500)