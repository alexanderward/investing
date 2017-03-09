from django.conf import settings
from rest_framework.pagination import PageNumberPagination


class CountPagination(PageNumberPagination):
    def get_page_size(self, request):
        return request.query_params.get('count', settings.REST_FRAMEWORK.get('PAGE_SIZE'))
