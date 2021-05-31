from django.http.response import HttpResponseRedirect
from django.urls.base import reverse
from App.forms.UserForms import LoginUserForm
from django.db import connection

def login_required(f):
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

