from django.contrib import admin
from django.http import HttpResponse
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', lambda request: HttpResponse('EasyStock Backend Running', content_type='text/plain')),
    path('api/', include('stock.urls')),
]


