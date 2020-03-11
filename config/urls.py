from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls), # 해킹 방지 치원에서 변경하자. PRD 배포 시. apple-admin

    #path('accounts/', include('django.contrib.auth.urls')), # 장고 표준 auth 사용.
    path('accounts/', include('allauth.urls')), #allauth library 사용.

    # local apps
    # path('', include('pages.urls')),
    path('', include('stock.urls')),
    #path('orders/', include('orders.urls')), 그냥 stock 아래에 위치시킴.

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    import debug_toolbar
    urlpatterns = [
        path('__debug__/', include(debug_toolbar.urls)),
    ] + urlpatterns