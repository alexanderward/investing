from app.views import PartialGroupView
from django.conf.urls import include, url
from . import views

partial_patterns = [
    url(r'^profile.html$', PartialGroupView.as_view(template_name='partials/profile.html'),
        name='profile'),
    url(r'^dashboard-overview.html$', PartialGroupView.as_view(template_name='partials/dashboard-overview.html'),
        name='home'),
    url(r'^research.html$', PartialGroupView.as_view(template_name='partials/research.html'),
        name='research_method1'),
    url(r'^analysis.html$', PartialGroupView.as_view(template_name='partials/analysis.html'),
        name='analytics_strategy1'),
    url(r'^dictionary.html$', PartialGroupView.as_view(template_name='partials/dictionary.html'), name='dictionary'),
    url(r'^links.html$', PartialGroupView.as_view(template_name='partials/links.html'), name='links'),
    url(r'^notes.html$', PartialGroupView.as_view(template_name='partials/notes.html'), name='notes'),
    url(r'^directives/graph-table.html$', PartialGroupView.as_view(template_name='partials/directives/graph-table.html')),
]

urlpatterns = [
    # url(r'test-alarm/(?P<alarm_id>\d+)/$', views.test_alarm, name='test_alarm'),
    url(r'^partials/', include(partial_patterns, namespace='partials')),
    url(r'^login.html$', views.Login.as_view(), name='login'),
    url(r'^api/current-financials/$', views.CurrentFinancials.as_view(), name='CurrentFinancials'),
    url(r'^', views.Index.as_view(), name='index'),
]
