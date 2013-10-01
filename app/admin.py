# -*- coding: utf-8 -*-
from django.contrib import admin
from app.forms import JSONModelAdminForm
from app.models import JSONModel


class JSONModelAdmin(admin.ModelAdmin):

    form = JSONModelAdminForm


admin.site.register(JSONModel, JSONModelAdmin)
