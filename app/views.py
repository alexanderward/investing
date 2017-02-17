from django.http import JsonResponse
from django.shortcuts import render
from django.views.generic import TemplateView
from rest_framework import status, viewsets
from rest_framework.exceptions import ValidationError
from rest_framework.status import HTTP_201_CREATED
from django.http import HttpResponse, Http404, HttpResponseBadRequest
from rest_framework.renderers import JSONRenderer


class PartialGroupView(TemplateView):
    def get_context_data(self, **kwargs):
        context = super(PartialGroupView, self).get_context_data(**kwargs)
        # update the context
        return context


class GenericViewSet(viewsets.ModelViewSet):
    def list(self, request, **kwargs):
        queryset = self.queryset
        serializer = self.get_serializer(self.paginate_queryset(queryset), many=True)
        return JSONResponse(serializer.data)

    def create(self, request, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            instance = serializer.create(serializer.data)
            response_serializer = self.get_serializer(instance)
            return JSONResponse(response_serializer.data, status=HTTP_201_CREATED)
        else:
            raise ValidationError(serializer.errors)

    def retrieve(self, request, pk=None, **kwargs):
        instance = self.get_object()
        if instance:
            serializer = self.get_serializer(instance)
            return JSONResponse(serializer.data)
        else:
            return JSONResponse(None)

    def update(self, request, pk=None, **kwargs):
        instance = self.get_object()
        if instance:
            serializer = self.get_serializer(data=request.data)
            if serializer.is_valid():
                instance = serializer.update(instance, serializer.data)
                serializer = self.get_serializer(instance)
                return JSONResponse(serializer.data)
            else:
                raise ValidationError(serializer.errors)

    def destroy(self, request, pk=None, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return JSONResponse({'status': 'success'})


class JSONResponse(HttpResponse):
    """
    An HttpResponse that renders its content into JSON.
    """

    def __init__(self, data, **kwargs):
        if data is None:
            data = {'error': 'No records found.'}
        content = JSONRenderer().render(data)
        kwargs['content_type'] = 'application/json'
        super(JSONResponse, self).__init__(content, **kwargs)


def index(request):
    return render(request, 'index.html')
