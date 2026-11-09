from django.contrib import admin
from django.urls import path
from sustentabilidad.views import vista_panel_sustentabilidad

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', vista_panel_sustentabilidad, name='panel_sustentabilidad'),
]