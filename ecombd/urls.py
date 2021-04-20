from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('app_shop.urls')),
    path('card/', include('app_order.urls')),
    path('app_payment/', include('app_payment.urls')),
    path('loginapp/', include('loginapp.urls')),

]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
