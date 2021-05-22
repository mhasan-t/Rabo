from django.shortcuts import render
from django.views.generic import View
from ..forms import CreateUserForm
from ..utils import login_required

class DashboardView(View):
    @login_required
    def get(self, request):
        form = CreateUserForm()
        context_data = {
            'userform': form
        }
        return render(template_name='dashboard.html', request=request, context=context_data)
