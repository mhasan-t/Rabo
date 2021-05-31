from django.db import connection
from django.http.response import HttpResponseRedirect
from django.shortcuts import render
from django.urls.base import reverse
from django.views.generic import View
from ..forms import CreateUserForm
from ..utils import login_required


class HomeView(View):
    @login_required
    def get(self, request, user_id):
        return HttpResponseRedirect(reverse('dashboard'))

class DashboardView(View):
    @login_required
    def get(self, request, user_id):
        sid = request.COOKIES.get('session_id')

        query = f'''
            SELECT * FROM user
            WHERE id = (
                SELECT user_id FROM sessions 
                WHERE session_id = "{sid}"
            )
        '''
        with connection.cursor() as cursor:
            if cursor.execute(query):
                user_data = cursor.fetchone()
                context_data = {
                    'user_data' : user_data
                }
                return render(template_name='dashboard.html', request=request, context=context_data)

            else:
                return HttpResponseRedirect(reverse('log-in'))