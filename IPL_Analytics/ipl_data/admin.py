# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from .models import Season,Match,Delivery

# Register your models here.
admin.site.register(Season)
admin.site.register(Match)
admin.site.register(Delivery)