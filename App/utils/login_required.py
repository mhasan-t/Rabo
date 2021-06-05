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

def login_required_project(f):
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
            if(user_role!=None and user_role[0]!="supervisor"):
                return HttpResponse("Unauthorized")

            return f(self, request, user_id, pid)
    return wrapper

