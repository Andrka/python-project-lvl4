from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views.generic import CreateView
from django.views.generic.base import TemplateView
from django.views.generic.list import ListView


class LoginView(TemplateView):
    template_name = 'task_manager/login.html'

    def dispatch(self, request, *args, **kwargs):
        context = {}
        if request.method == 'POST':
            username = request.POST['username']
            password = request.POST['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('/')
            else:
                context['error'] = 'Логин или пароль неверные.'
        return render(request, self.template_name, context)


class RegisterView(CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'task_manager/register.html'


class UsersView(ListView):
    model = User
    template_name = 'task_manager/users.html'

    def get_queryset(self):
        return User.objects.all()
