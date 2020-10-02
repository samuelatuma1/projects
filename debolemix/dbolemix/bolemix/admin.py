from django.contrib import admin

# Register your models here.

#With this, admin(s) can manipulate these tables all they want

from .models import Yam, Potatoe, Plantain


admin.site.register(Yam)
admin.site.register(Plantain)
admin.site.register(Potatoe)

