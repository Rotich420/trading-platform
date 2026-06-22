from django.contrib import admin
from django.urls import path, include
from django.views.generic import RedirectView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', RedirectView.as_view(url='/trading/', permanent=False)),
    path('accounts/', include('accounts.urls')),
    path('trading/', include('trading.urls')),
    path('wallet/', include('wallet.urls')),
]
