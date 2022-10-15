from django.contrib import admin
from django.contrib.auth.models import Group

from test_app.models import Url


admin.site.register(Url)
