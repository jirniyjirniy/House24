# -*- coding: utf-8 -*-
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.http import HttpResponseRedirect
from django.shortcuts import redirect, render
from django.views.generic import View

from src.accounts.forms import LoginForm
from src.admin_panel.models import Role


class LoginView(View):
    template_name = "login.html"
    form_class = LoginForm

    def get(self, request):
        form = self.form_class()
        message = ""
        return render(request, self.template_name, context={"form": form, "message": message})

    def post(self, request):
        form = self.form_class(data=request.POST)

        if form.is_valid():
            user = authenticate(
                username=form.cleaned_data["username"],
                password=form.cleaned_data["password"],
            )
            if user is not None:
                login(request, user)
                if not form.cleaned_data["remember_me"]:
                    self.request.session.set_expiry(0)
                if user.is_staff:
                    user_permission = Role.objects.get(name=user.personal.role)
                    if user_permission.statistics:
                        return redirect("personals")
                    else:
                        url = f"/admin/personals/update/{self.request.user.id}"
                        return HttpResponseRedirect(url)

                else:
                    return redirect("tariffs")
        messages.error(request, "Неправильно указана почта или пароль")
        return render(request, self.template_name, context={"form": form})
