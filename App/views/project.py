from App.utils import login_required_project_admin, login_required_user
from django.db import connection
from django.http.response import HttpResponse, HttpResponseRedirect
from django.views.generic import View
from django.shortcuts import render
from django.urls import reverse

import pytz
import datetime





class CreateProject(View):
    @login_required_user
    def get(self, request, user_id):
        return render(request=request, template_name="create_project.html")

    @login_required_user
    def post(self, request, user_id):
        name = request.POST.get("name")
        desc = request.POST.get("desc")


        if name != None and len(name)<31 and desc != None and len(desc)<256 :

            DTZ = pytz.timezone("Asia/Dhaka")
            created_dt = datetime.datetime.now(DTZ)

            query = f"""
                INSERT INTO project(name, `desc`, created_at) VALUES(
                    "{str(name)}" ,
                    "{str(desc)}" ,
                    "{str(created_dt.strftime('%Y:%m:%d %H:%M:%S'))}"
                );
            """

            with connection.cursor() as cursor:
                cursor.execute(query)
                cursor.execute("SELECT LAST_INSERT_ID()")
                new_proj_id = cursor.fetchone()[0]

                cursor.execute(f'''
                    INSERT INTO works_on(project_id, user_id, role)
                    VALUES ( {new_proj_id}, {user_id}, "supervisor" )
                ''')

            
            return HttpResponseRedirect(reverse('dashboard'))
        else:

            context_data = {
                'error_msg': 'Invalid Information'
            }
            return render(request=request, template_name="create_project.html", context=context_data)



class ProjectSettings(View):
    @login_required_project_admin
    def get(self, request, user_id, pid):

        query = f'''
            SELECT id, name, `desc`, created_at FROM project
            WHERE id = {pid}
        '''

        with connection.cursor() as cursor:
                if not cursor.execute(f'''
                    SELECT role FROM works_on WHERE user_id={user_id} AND project_id={pid}
                '''):
                    return HttpResponseRedirect(reverse("dashboard"))
                
                if cursor.fetchone()[0] != "supervisor":
                    return HttpResponseRedirect(reverse("dashboard"))

                cursor.execute(query)
                pj = cursor.fetchone()

                get_user_query = f'''
                    SELECT u.id as id, u.first_name as first_name, u.last_name as last_name, u.picture as picture,
                            CASE WHEN wo.role='supervisor' THEN true ELSE false END as isSuper
                    FROM user as u
                        JOIN works_on as wo ON wo.user_id = u.id 
                    WHERE wo.project_id = {pid}
                '''

                cursor.execute(get_user_query)
                working_users = cursor.fetchall()

                context_data = {
                    'p': pj,
                    'p_users' : working_users
                }
                return render(request, "project_settings.html", context=context_data)

    @login_required_project_admin
    def post(self, request, user_id, pid):
        field = request.POST.get("field")
        data = request.POST.get("data")

        if field!="" and data!="" and field!=None and data!=None:
            if field=="deadline":
                data = datetime.datetime.strptime(data,"%Y-%m-%dT%H:%M").strftime('%Y:%m:%d %H:%M:%S')

            query = f'''
                UPDATE project
                SET `{field}`="{data}"
                WHERE id={pid}
            '''
            with connection.cursor() as cursor:
                cursor.execute(query)
                # print(query)
            return render(request=request, template_name="project_settings.html", context={'success_msg':"Success"})
        else:
            context_data = {
                'error_msg': 'Invalid Information'
            }
            return render(request=request, template_name="project_settings.html", context=context_data)


class ProjectDeleteView(View):
    @login_required_project_admin
    def get(self, request, user_id, pid):
        query = f'''
            DELETE FROM project
            WHERE id={id}
        '''
        with connection.cursor() as cursor:
            cursor.execute(query)
            return HttpResponseRedirect(reverse('projectlist'))


class ProjectActions(View):
    @login_required_project_admin
    def get(self, request, user_id, pid):
        action = request.GET.get('action')
        on_user = request.GET.get('on_user')


        if( action=="invite" ):
            pass

        if( action=="remove" ):
            query = f'''
                DELETE FROM works_on
                WHERE user_id={on_user} AND project_id={pid}
            '''

            with connection.cursor() as cursor:
                if cursor.execute(query):
                    return HttpResponse(status=200)
                else:
                    return HttpResponse(status=400)


        if( action=="makesuper" ):
            query = f'''
                UPDATE works_on
                SET role='supervisor'
                WHERE project_id={pid} AND user_id={on_user}
            '''

            with connection.cursor() as cursor:
                if cursor.execute(query):
                    return HttpResponse(status=200)
                else:
                    return HttpResponse(status=400)

        if( action=="invite" ):
            pass
