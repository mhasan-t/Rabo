
from App.utils.login_required import login_required_project_employee
from django.urls.base import reverse_lazy
from App.utils import login_required_project_admin, login_required_user, login_required_task, login_required_project_employee, login_required_task_manager
from django.db import connection
from django.http.response import HttpResponse, HttpResponseRedirect
from django.views.generic import View
from django.shortcuts import render
from django.urls import reverse

import json
import pytz
import datetime


class ShowTask(View):
    @login_required_project_employee
    def get(self, request, user_id, pid):


        query = f'''
            SELECT * FROM user
            WHERE id = {user_id}
        '''

        proj_query = f'''
            SELECT id,name,`desc`,created_at, CASE WHEN wo.role='supervisor' THEN true ELSE false END as isSuper
            FROM project as pr JOIN works_on as wo ON pr.id=wo.project_id 
            WHERE wo.user_id = {user_id}
        '''

        with connection.cursor() as cursor:
            context_data = {}
            if cursor.execute(query):
                user_data = cursor.fetchone()
                context_data = {
                    'user_data' : user_data
                }
                
                cursor.execute(proj_query)
                proj_data = cursor.fetchall()
                context_data["projects"] = proj_data

                cursor.execute(f'''
                    SELECT nt.id, nt.data, nt.created_at, nt.type, nt.sent_to, nt.sent_by, nt.project_id ,
                            CASE WHEN type='invite' THEN true ELSE false END as isInvite,
                            pr.name, u.first_name, u.last_name, nt.created_at
                    FROM notification nt JOIN `user` as u ON nt.sent_by=u.id
                                        JOIN project as pr ON pr.id=nt.project_id
                    WHERE sent_to={user_id}
                ''')
                noti_data = cursor.fetchall()
                context_data["notifications"] = noti_data

                cursor.execute(f'''
                    SELECT *, CASE WHEN assigned_to={user_id} or managed_by={user_id} THEN true ELSE false END AS isAssigned 
                    FROM task
                    WHERE project_id={pid}
                ''')
                tasks_res = cursor.fetchall()
                cats = list(set([row[7] for row in tasks_res]))
                tasks = []

                for cat in cats:
                    t = [row for row in tasks_res if row[7]==cat]
                    tasks.append([cat,t])
                
                cursor.execute(f'''
                    SELECT role FROM works_on WHERE user_id={user_id} AND project_id={pid}
                ''')
                context_data["isSuper"] = cursor.fetchone()[0]=='supervisor'

                context_data["tasks"] = tasks
                context_data['pid'] = pid;
                




        return render(request=request, template_name='tasks.html', context=context_data)


class CreateTask(View):

    @login_required_project_admin
    def get(self, request, user_id, pid):


        query = f'''
            SELECT * FROM user
            WHERE id = {user_id}
        '''

        proj_query = f'''
            SELECT id,name,`desc`,created_at, CASE WHEN wo.role='supervisor' THEN true ELSE false END as isSuper
            FROM project as pr JOIN works_on as wo ON pr.id=wo.project_id 
            WHERE wo.user_id = {user_id}
        '''

        with connection.cursor() as cursor:
            context_data = {}
            if cursor.execute(query):
                user_data = cursor.fetchone()
                context_data = {
                    'user_data' : user_data
                }
                
                cursor.execute(proj_query)
                proj_data = cursor.fetchall()
                context_data["projects"] = proj_data

                cursor.execute(f'''
                    SELECT nt.id, nt.data, nt.created_at, nt.type, nt.sent_to, nt.sent_by, nt.project_id ,
                            CASE WHEN type='invite' THEN true ELSE false END as isInvite,
                            pr.name, u.first_name, u.last_name, nt.created_at
                    FROM notification nt JOIN `user` as u ON nt.sent_by=u.id
                                        JOIN project as pr ON pr.id=nt.project_id
                    WHERE sent_to={user_id}
                ''')
                noti_data = cursor.fetchall()
                context_data["notifications"] = noti_data
                context_data['pid'] = pid

                return render(request=request, template_name='create_task.html', context=context_data)

    @login_required_project_admin
    def post(self, request, user_id, pid):
        label = request.POST.get("label")
        desc = request.POST.get("desc")
        deadline = request.POST.get("deadline")
        urgency = request.POST.get("urgency")
        category = request.POST.get("category")
        assigned_to = request.POST.get('assigned_to')

        DTZ = pytz.timezone("Asia/Dhaka")
        created_dt = datetime.datetime.now(DTZ).strftime('%Y:%m:%d %H:%M:%S')

        deadline_dt = datetime.datetime.strptime(deadline,"%Y-%m-%dT%H:%M").strftime('%Y:%m:%d %H:%M:%S')

        with connection.cursor() as cursor:
            cursor.execute(f'''
                INSERT INTO task(label, `desc`, deadline, urgency, created_at, category, project_id, created_by, assigned_to)
                VALUES( '{label}', '{desc}', '{deadline_dt}', '{urgency}', '{created_dt}', '{category}', '{pid}', '{user_id}', {assigned_to})
            ''')
            return HttpResponseRedirect(reverse('showtasks', args=[pid]))



class ManageTask(View):
    @login_required_task
    def get(self, request, user_id, pid, taskid, **kwargs):


        query = f'''
            SELECT * FROM user
            WHERE id = {user_id}
        '''

        proj_query = f'''
            SELECT id,name,`desc`,created_at, CASE WHEN wo.role='supervisor' THEN true ELSE false END as isSuper
            FROM project as pr JOIN works_on as wo ON pr.id=wo.project_id 
            WHERE wo.user_id = {user_id}
        '''

        with connection.cursor() as cursor:
            context_data = {}
            if cursor.execute(query):
                user_data = cursor.fetchone()
                context_data = {
                    'user_data' : user_data
                }
                
                cursor.execute(proj_query)
                proj_data = cursor.fetchall()
                context_data["projects"] = proj_data

                cursor.execute(f'''
                    SELECT nt.id, nt.data, nt.created_at, nt.type, nt.sent_to, nt.sent_by, nt.project_id ,
                            CASE WHEN type='invite' THEN true ELSE false END as isInvite,
                            pr.name, u.first_name, u.last_name, nt.created_at
                    FROM notification nt JOIN `user` as u ON nt.sent_by=u.id
                                        JOIN project as pr ON pr.id=nt.project_id
                    WHERE sent_to={user_id}
                ''')
                noti_data = cursor.fetchall()
                context_data["notifications"] = noti_data

                cursor.execute(f'''
                    SELECT *, CASE WHEN completed_at IS NULL THEN false ELSE true END AS ended
                    FROM task WHERE id={taskid}
                ''')
                task = cursor.fetchone()
                context_data['task'] = task

                cursor.execute(f'''
                    SELECT * FROM user
                    WHERE id = (
                        SELECT created_by FROM task
                        WHERE id={taskid}
                    )
                ''')
                context_data['created_by']=cursor.fetchone()
                context_data['pid']=pid

                cursor.execute(f'''
                    SELECT role FROM works_on WHERE user_id={user_id} AND project_id={pid}
                ''')
                role = cursor.fetchone()[0]
                context_data['isSuper'] = role=='supervisor'

                manager = task[8]
                context_data['isManager'] = manager==user_id
                context_data['isEmployee'] = True if (manager!=user_id) and (role!='supervisor') else False


                cursor.execute(f'''
                    SELECT independent FROM task_dependency WHERE dependent={taskid}
                ''')
                context_data['dependencies'] = cursor.fetchall()

                cursor.execute(f'''
                    SELECT dependent FROM task_dependency WHERE independent={taskid}
                ''')
                context_data['superior_to'] = cursor.fetchall()


                cursor.execute(f'''
                SELECT name FROM project WHERE id={pid}
                ''')
                context_data["project_name"]=cursor.fetchone()[0]


                cursor.execute(f'''
                    SELECT u.first_name, u.last_name, fd.data, fd.given_at
                        FROM feedback as fd
                            JOIN user as u ON u.id=fd.given_by
                    WHERE given_to={taskid}
                ''')
                context_data['feedbacks'] = cursor.fetchall()


                return render(request=request, template_name='manage_task.html', context=context_data)


    @login_required_task_manager
    def post(self, request, user_id, pid, taskid):
        data = list(request.POST.items())
        field = data[1][0]
        value = data[1][1]

        if value == "":
            return HttpResponseRedirect(reverse('managetask', args=[pid, taskid]))

        query = f'''
            UPDATE task
            SET `{field}`="{value}"
            WHERE id={taskid}
        '''
        
        with connection.cursor() as cursor:
            res = cursor.execute(query)
            if res:
                return HttpResponseRedirect(reverse('managetask', args=[pid, taskid]))




class AddDependency(View):
    @login_required_task_manager
    def get(self, request, user_id, pid, taskid, **kwargs):
        with connection.cursor() as cursor:
            independent = int(request.GET.get("independent"))
            cursor.execute(f'''
                INSERT INTO task_dependency(independent, dependent)
                VALUES( {independent}, {taskid} )
            ''')
            return HttpResponse()


class RemoveDependency(View):
    @login_required_task_manager
    def get(self, request, user_id, pid, taskid, **kwargs):
        with connection.cursor() as cursor:
            independent = int(request.GET.get("independent"))
            cursor.execute(f'''
                DELETE FROM task_dependency
                WHERE independent={independent} AND dependent={taskid}
            ''')
            return HttpResponse()


class GiveFeedback(View):
    @login_required_task_manager
    def post(self, request, user_id, pid, taskid):
        data = request.POST.get("feedback")
        DTZ = pytz.timezone("Asia/Dhaka")
        given_at = datetime.datetime.now(DTZ).strftime('%Y:%m:%d %H:%M:%S')

        with connection.cursor() as cursor:

            cursor.execute(f'''
                INSERT INTO feedback(given_by, given_to, data, given_at)
                VALUES({user_id}, {taskid}, '{data}', '{given_at}')
            ''')

            return HttpResponseRedirect(reverse('managetask',args=[pid, taskid]))


class SubmitTask(View):
    @login_required_task
    def get(self, request, user_id, pid, taskid):
        with connection.cursor() as cursor:
            cursor.execute(f"SELECT label, managed_by, assigned_to FROM task WHERE id={taskid}")
            res = cursor.fetchone()
            taskname = res[0]
            send_to = res[1]
            assigned_to = res[2]

            if assigned_to != user_id:
                return HttpResponse("Unauthorized")

            if send_to is None:
                cursor.execute(f"SELECT created_by FROM task WHERE id={taskid}")
                send_to = cursor.fetchone()[0]

            cursor.execute(f"SELECT first_name, last_name FROM user WHERE id={user_id}")
            res = cursor.fetchone()
            fn = res[0]
            ln = res[1]


            cursor.execute(f"SELECT name FROM project WHERE id={pid}")
            res = cursor.fetchone()
            pn = res[0]


            DTZ = pytz.timezone("Asia/Dhaka")
            created_dt = datetime.datetime.now(DTZ)

            query = f'''
                INSERT INTO notification(data, created_at, type, sent_to, sent_by, project_id)
                VALUES( 
                    "{str(fn)} {str(ln)} has submitted task {taskname} for board {str(pn)}",
                    '{created_dt.strftime('%Y:%m:%d %H:%M:%S')}',
                    'submit',
                    '{send_to}',
                    '{user_id}',
                    '{pid}'
                 )
            '''

            cursor.execute(query)

            return HttpResponseRedirect(reverse('managetask', args=[pid, taskid]))


class EndTask(View):
    @login_required_task_manager
    def get(self, request, user_id, pid, taskid):
        DTZ = pytz.timezone("Asia/Dhaka")
        now_dt = datetime.datetime.now(DTZ).strftime('%Y:%m:%d %H:%M:%S')

        with connection.cursor() as cursor:
            cursor.execute(f'''
                UPDATE task
                SET completed_at = '{now_dt}'
                WHERE id={taskid}
            ''')

            cursor.execute(f"SELECT label, assigned_to FROM task WHERE id={taskid}")
            res = cursor.fetchone()
            label =  res[0]
            assigned_to =  res[1]


            cursor.execute(f"SELECT name FROM project WHERE id={pid}")
            pname = cursor.fetchone()[0]

            cursor.execute(f'''
                SELECT id FROM user
                WHERE id = ANY (
                        SELECT assigned_to FROM task
                        WHERE id = (
                            SELECT dependent FROM task_dependency
                            WHERE independent = {taskid}
                        )
                    )
            ''')
            res = cursor.fetchall()



            
            for r in res:
                reciever = r[0]
                query = f'''
                INSERT INTO notification(data, created_at, type, sent_to, sent_by, project_id)
                VALUES( 
                    "Task {str(label)} from {str(pname)} has ended",
                    '{now_dt}',
                    'info',
                    '{reciever}',
                    '{user_id}',
                    '{pid}'
                 )
                '''
                cursor.execute(query)

            cursor.execute(f'''
                INSERT INTO notification(data, created_at, type, sent_to, sent_by, project_id)
                VALUES( 
                    "Task {str(label)} from {str(pname)} has ended",
                    '{now_dt}',
                    'info',
                    '{assigned_to}',
                    '{user_id}',
                    '{pid}'
                 )
            ''')

            return HttpResponseRedirect(reverse('managetask', args=[pid, taskid]))



class SendReminder(View):
    @login_required_task_manager
    def get(self, request, user_id, pid, taskid):
        DTZ = pytz.timezone("Asia/Dhaka")
        now_dt = datetime.datetime.now(DTZ).strftime('%Y:%m:%d %H:%M:%S')

        with connection.cursor() as cursor:
            cursor.execute(f'''SELECT id FROM user
                                WHERE id = (SELECT assigned_to FROM task WHERE id={taskid})
                            ''')
            assigned_to = cursor.fetchone()[0]


            cursor.execute(f"SELECT label, deadline FROM task WHERE id={taskid}")
            res = cursor.fetchone()
            label = res[0]
            deadline = res[1]

            cursor.execute(f"SELECT name FROM project WHERE id={pid}")
            pname = cursor.fetchone()[0]

            query = f'''
                INSERT INTO notification(data, created_at, type, sent_to, sent_by, project_id)
                VALUES( 
                    "Remember to finish the task {label} for {pname}. DEADLINE: {deadline}",
                    '{now_dt}',
                    'reminder',
                    '{assigned_to}',
                    '{user_id}',
                    '{pid}'
                 )
                '''
            cursor.execute(query)

            return HttpResponse()



