from app.views import PartialGroupView
from django.conf.urls import include, url
from . import views

partial_patterns = [
    url(r'^dashboard-overview.html$', PartialGroupView.as_view(template_name='partials/dashboard-overview.html'),
        name='home'),
    url(r'^dashboard-transactions.html$',
        PartialGroupView.as_view(template_name='partials/dashboard-transactions.html'), name='dashboard_transactions'),
    url(r'^research-method1.html$', PartialGroupView.as_view(template_name='partials/research-method1.html'),
        name='research_method1'),
    url(r'^analytics-strategy1.html$', PartialGroupView.as_view(template_name='partials/analytics-strategy1.html'),
        name='analytics_strategy1'),
    url(r'^dictionary.html$', PartialGroupView.as_view(template_name='partials/dictionary.html'),
        name='dictionary'),
]

urlpatterns = [
    # url(r'test-alarm/(?P<alarm_id>\d+)/$', views.test_alarm, name='test_alarm'),
    url(r'^partials/', include(partial_patterns, namespace='partials')),
    url(r'^login.html$', views.Login.as_view(), name='login'),
    url(r'^api/current-financials/$', views.CurrentFinancials.as_view(), name='CurrentFinancials'),
    url(r'^', views.Index.as_view(), name='index'),
]