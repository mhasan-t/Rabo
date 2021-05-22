from django.db import connection
from django.http.response import HttpResponse
from django.urls import reverse

def login_required(f):
    def wrapper(self, request):
        sid = request.COOKIES.get('session_id')

        if sid is None:
            return HttpResponse('Unauthorized', status=401)

        query = f'''
            SELECT session_id FROM sessions
            WHERE session_id = "{sid}"
        '''
        
        with connection.cursor() as cursor:
            sid_valid  = cursor.execute(query)

            if sid_valid==0:
                return HttpResponse('Unauthorized', status=401)
            
            return f(self, request)
    return wrapper

