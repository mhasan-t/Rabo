from django.http.response import HttpResponse, HttpResponseRedirect
from django.urls.base import reverse
from App.forms.UserForms import LoginUserForm
from django.db import connection

def login_required_user(f):
    def wrapper(self, request):
        sid = request.COOKIES.get('session_id')
        if sid is None:
            return HttpResponseRedirect(reverse('log-in'))


        query = f'''
            SELECT user_id FROM sessions
            WHERE session_id = "{sid}"
        '''
        
        with connection.cursor() as cursor:
            sid_valid  = cursor.execute(query)

            if sid_valid==0:
                return HttpResponseRedirect(reverse('log-in'))

            user_id = cursor.fetchone()[0]
            return f(self, request, user_id)
    return wrapper

def login_required_project_admin(f):
    def wrapper(self, request, pid):
        sid = request.COOKIES.get('session_id')
        if sid is None:
            return HttpResponseRedirect(reverse('log-in'))


        query = f'''
            SELECT user_id FROM sessions
            WHERE session_id = "{sid}"
        '''
        
        with connection.cursor() as cursor:
            sid_valid  = cursor.execute(query)

            if sid_valid==0:
                return HttpResponseRedirect(reverse('log-in'))

            user_id = cursor.fetchone()[0]

            cursor.execute(f'''
                SELECT role from works_on
                WHERE project_id={pid} AND user_id={user_id}
            ''')
            user_role = cursor.fetchone()
            if(user_role==None or user_role[0]!="supervisor"):
                return HttpResponse("Unauthorized")

            return f(self, request, user_id, pid)
    return wrapper



def login_required_project_employee(f):
    def wrapper(self, request, pid):
        sid = request.COOKIES.get('session_id')
        if sid is None:
            return HttpResponseRedirect(reverse('log-in'))


        query = f'''
            SELECT user_id FROM sessions
            WHERE session_id = "{sid}"
        '''
        
        with connection.cursor() as cursor:
            sid_valid  = cursor.execute(query)

            if sid_valid==0:
                return HttpResponseRedirect(reverse('log-in'))

            user_id = cursor.fetchone()[0]

            cursor.execute(f'''
                SELECT role from works_on
                WHERE project_id={pid} AND user_id={user_id}
            ''')
            user_role = cursor.fetchone()
            if(user_role==None):
                return HttpResponse("Unauthorized")

            return f(self, request, user_id, pid)
    return wrapper


def login_required_task(f):
    def wrapper(self, request, pid, taskid):
        sid = request.COOKIES.get('session_id')
        if sid is None:
            return HttpResponseRedirect(reverse('log-in'))


        query = f'''
            SELECT user_id FROM sessions
            WHERE session_id = "{sid}"
        '''
        
        with connection.cursor() as cursor:
            sid_valid  = cursor.execute(query)

            if sid_valid==0:
                return HttpResponseRedirect(reverse('log-in'))

            user_id = cursor.fetchone()[0]
            cursor.execute(f'''
                SELECT role from works_on
                WHERE project_id={pid} AND user_id={user_id}
            ''')
            user_role = cursor.fetchone()
            # print(user_role)
            if(user_role==None):
                return HttpResponse("Unauthorized")

            if user_role[0]=='employee':
                cursor.execute(f"SELECT assigned_to, managed_by FROM task WHERE id={taskid}")
                res = cursor.fetchone()
                if user_id != res[0] and user_id != res[1]:
                    return HttpResponse("Unauthorized")

            return f(self, request, user_id, pid, taskid)
    return wrapper


def login_required_task_manager(f):
    def wrapper(self, request, pid, taskid):
        sid = request.COOKIES.get('session_id')
        if sid is None:
            return HttpResponseRedirect(reverse('log-in'))


        query = f'''
            SELECT user_id FROM sessions
            WHERE session_id = "{sid}"
        '''

        with connection.cursor() as cursor:
            sid_valid  = cursor.execute(query)

            if sid_valid==0:
                return HttpResponseRedirect(reverse('log-in'))

            user_id = cursor.fetchone()[0]
            cursor.execute(f'''
                SELECT role from works_on
                WHERE project_id={pid} AND user_id={user_id}
            ''')
            user_role = cursor.fetchone()[0]

            cursor.execute(f'''
                    SELECT managed_by FROM task WHERE id={taskid}
                ''')
            manager = cursor.fetchone()[0]

            if(user_role==None or (user_role!='supervisor' and manager!=user_id)):
                return HttpResponseRedirect("Unauthorized")


            return f(self, request, user_id, pid, taskid)
    return wrapper