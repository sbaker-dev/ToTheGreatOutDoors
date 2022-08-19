from django.contrib import admin

from.models import TravelLocation, Boundary, RasterMap

# Register your models here.

admin.site.register(Boundary)
admin.site.register(TravelLocation)
admin.site.register(RasterMap)
