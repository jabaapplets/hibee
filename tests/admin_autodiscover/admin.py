from hibeecontrib import admin

from .models import Story

admin.site.register(Story)
raise Exception("Bad admin module")
