from django.urls import include, path, re_path
from django.contrib import admin
from django.conf import settings

urlpatterns = [

    # django admin site
    path(r'admin/', admin.site.urls),

    # our installed apps
    path('', include('pages.urls')),
    path('sms/', include('sms.urls')),
    path('users/', include('users.urls')),

    # django-allauth account urls
    path('accounts/', include('allauth.urls')),
]

# django-debug-toolbar, useful for debugging
if settings.DEBUG:
    import debug_toolbar
    urlpatterns += [
        path(r'__debug__/', include(debug_toolbar.urls)),
    ]
