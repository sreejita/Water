# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin

# Register your models here.

from .models import Waterbodies

class WaterbodiesAdmin(admin.ModelAdmin):
	list_display = ['sno', 'nhd_lake_id', 'gnis_name']

admin.site.register(Waterbodies, WaterbodiesAdmin)
