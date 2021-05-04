from django.views.generic import View
from django.shortcuts import render
from django.db import connection
from ..forms import CreateUserForm


class CreateUser(View):
    def get(self, request):
        form = CreateUserForm()
        context_data = {
            'form': form
        }
        return render(request=request, template_name="user_signup.html", context=context_data)

    def post(self, request):

        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        email = request.POST.get("email")
        password = request.POST.get("password")

        query = f"""
            INSERT INTO user(first_name, last_name, email, password) VALUES(
                "{str(first_name)}" ,
                "{str(last_name)}" ,
                "{str(email)}",
                "{str(password)}"
            )
        """

        with connection.cursor() as cursor:
            cursor.execute(query)
