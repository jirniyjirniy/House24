# -*- coding: utf-8 -*-
import json

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import redirect
from django.utils.decorators import method_decorator
from django.views.generic import View

import House24.settings as settings
from src.admin_panel.models import Personal


class StaffRequiredMixin:
    """
    Mixin which requires that the authenticated user is a staff member.
    """

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_staff:
            messages.error(
                request,
                "Либо вы не вошли в систему"
                " либо у вас нету соответствующих прав для пользования административной панелью.",
            )
            return redirect(settings.LOGIN_URL)
        return super(StaffRequiredMixin, self).dispatch(request, *args, **kwargs)


class GetRoleView(View):
    def get(self, request, pk):
        personal = Personal.objects.get(pk=pk)
        context = {"role": personal.get_role_display()}
        return HttpResponse(json.dumps(context), content_type="application/json")
