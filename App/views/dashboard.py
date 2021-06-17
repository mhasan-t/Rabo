from django.db import connection
from django.http.response import HttpResponseRedirect
from django.shortcuts import render
from django.urls.base import reverse
from django.views.generic import View
from ..forms import CreateUserForm
from ..utils import login_required_user


class HomeView(View):
    @login_required_user
    def get(self, request, user_id):
        return HttpResponseRedirect(reverse('dashboard'))

class DashboardView(View):
    @login_required_user
    def get(self, request, user_id):
        sid = request.COOKIES.get('session_id')

        query = f'''
            SELECT * FROM user
            WHERE id = (
                SELECT user_id FROM sessions 
                WHERE session_id = "{sid}"
            )
        '''

        proj_query = f'''
            SELECT id,name,`desc`,created_at, CASE WHEN wo.role='supervisor' THEN true ELSE false END as isSuper
            FROM project as pr JOIN works_on as wo ON pr.id=wo.project_id 
            WHERE wo.user_id = {user_id}
        '''

        with connection.cursor() as cursor:
            if cursor.execute(query):
                user_data = cursor.fetchone()
                context_data = {
                    'user_data' : user_data
                }
                
                cursor.execute(proj_query)
                proj_data = cursor.fetchall()
                context_data["projects"] = proj_data

                query = f'''
                    SELECT nt.id, nt.data, nt.created_at, nt.type, nt.sent_to, nt.sent_by, nt.project_id ,
                            CASE WHEN type='invite' THEN true ELSE false END as isInvite,
                            pr.name, u.first_name, u.last_name, nt.created_at
                    FROM notification nt JOIN `user` as u ON nt.sent_by=u.id
                                        JOIN project as pr ON pr.id=nt.project_id
                    WHERE sent_to={user_id}
                '''
                # print(query)
                cursor.execute(query)
                noti_data = cursor.fetchall()
                context_data["notifications"] = noti_data
                # print(noti_data)

                return render(template_name='dashboard.html', request=request, context=context_data)

            else:
                return HttpResponseRedirect(reverse('log-in'))