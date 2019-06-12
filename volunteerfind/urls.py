from django.contrib import admin
from django.conf.urls import url, include
from django.urls import path
from projects import views as projects_views

urlpatterns = [
    path('admin/', admin.site.urls),
    url(r'^$', projects_views.homepage),
    url(r'^projects/', include('projects.urls')),
    url(r'^users/', include('users.urls'))
]
