from django.db import connection


def login_required(f, sid):
    query = f'''
        SELECT COUNT(*)
        FROM sessions
        WHERE session_id = "{sid}""
    '''
    with connection.cursor() as cursor:
        res = cursor.execute(query)
        print(res)
