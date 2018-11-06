from django.contrib import admin
from django.urls import include, path
from django.conf.urls import url
from votes import urls

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('comments.urls')),
    path('api-auth/', include('rest_framework.urls')),
    url(r'^', include(urls)),
]
