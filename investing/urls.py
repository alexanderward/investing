"""alarm_clock URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin
from rest_framework import routers

from app.views import DefinitionsViewset, UserFinancialsViewset, SymbolHistoryViewset, SymbolViewset, UserProfileViewset

router = routers.DefaultRouter()
router.register(r'definitions', DefinitionsViewset, base_name='Definition')
router.register(r'symbols', SymbolViewset, base_name='Symbol')

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^api/', include(router.urls)),
    url(r'^api/profile/', UserProfileViewset.as_view({'get': 'get_profile', 'put': 'update'})),
    url(r'^api/financials/', UserFinancialsViewset.as_view({'get': 'list'})),
    url(r'^api/symbols/(?P<pk>\w+)/history/$', SymbolHistoryViewset.as_view({'get': 'retrieve'})),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^', include('app.urls', namespace='app')),
]
