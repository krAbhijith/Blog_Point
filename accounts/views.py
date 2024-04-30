from django.forms import BaseModelForm
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import CreateView, RedirectView
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password

class AccountRegisterView(CreateView):
    model = User
    fields = ['first_name', 'last_name', 'email']
    template_name = 'accounts/index.html'
    success_url = reverse_lazy('home')

    def form_valid(self, form: BaseModelForm) -> HttpResponse:
        password = self.request.POST.get('password')
        form.instance.username = self.request.POST.get('email')
        form.instance.password = make_password(password)

        self.object = form.save()
        login(self.request, self.object)
        return HttpResponseRedirect(self.get_success_url())
    

class AccountLoginView(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'accounts/index.html')

    def post(self, request, *args, **kwargs):
        username = self.request.POST.get('email')
        password = self.request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        

class AccountLogoutView(RedirectView):
    query_string = False
    pattern_name = 'login-account'

    def get_redirect_url(self, *args, **kwargs):
        logout(self.request)
        return reverse_lazy(self.pattern_name)