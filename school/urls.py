from django.contrib import admin
from django.urls import path, include
from courses.urls import router

urlpatterns = [
    #API V1
    path('api/v1/', include('courses.urls')),
    path('admin/', admin.site.urls),
    path('auth/', include('rest_framework.urls')),

    #API V2
    path('api/v2/', include(router.urls)),
]
