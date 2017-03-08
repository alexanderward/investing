from rest_framework import mixins

from app.models import Definition, Financial, SymbolHistory, Symbol
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.views import View
from django.views.generic import TemplateView
from rest_framework import status, viewsets
from rest_framework.exceptions import ValidationError
from rest_framework.status import HTTP_201_CREATED
from django.http import HttpResponse, Http404, HttpResponseBadRequest
from rest_framework.renderers import JSONRenderer
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import authenticate, login, logout

from app.serializers import DictionarySerializer, FinancialsSerializer, SymbolHistorySerializer, SymbolSerializer


class PartialGroupView(TemplateView):
    def get_context_data(self, **kwargs):
        context = super(PartialGroupView, self).get_context_data(**kwargs)
        # update the context
        return context


class GenericViewSet(viewsets.ModelViewSet):
    def list(self, request, **kwargs):
        queryset = self.get_queryset()
        if queryset:
            serializer = self.get_serializer(self.paginate_queryset(queryset), many=True)
            return JSONResponse(serializer.data)
        else:
            return JSONResponse([])

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


class Login(View):
    def get(self, request):
        logout(request)
        return render(request, 'login.html')

    def post(self, request):
        email = request.POST['email']
        password = request.POST['password']
        user = authenticate(email=email, password=password)
        if user is not None:
            login(request, user)
            return redirect('/')
        else:
            return render(request, 'login.html', context={'error': 'Invalid Email/Password'})


class CurrentFinancials(LoginRequiredMixin, View):
    login_url = 'login.html'
    redirect_field_name = 'redirect_to'

    def get(self, request):
        queryset = Financial.objects.filter(user=request.user).latest('timestamp')
        serializer = FinancialsSerializer(queryset)
        return JsonResponse(serializer.data)


class Index(LoginRequiredMixin, View):
    login_url = 'login.html'
    redirect_field_name = 'redirect_to'

    def get(self, request):
        context = dict(user={})
        context['user']['email'] = request.user.email
        context['user']['fullname'] = request.user.get_full_name()
        try:
            context['user']['avatar'] = "static" + "/".join(request.user.avatar.url.split('static')[1:])
        except ValueError:
            context['user']['avatar'] = "static" + "/img/avatars/male.png"
        return render(request, 'index.html', context=context)


class DefinitionsViewset(GenericViewSet):
    serializer_class = DictionarySerializer
    queryset = Definition.objects.all().order_by('title')

    def __init__(self, **kwargs):
        super(DefinitionsViewset, self).__init__(**kwargs)


class UserFinancialsViewset(mixins.ListModelMixin, viewsets.GenericViewSet):
    serializer_class = FinancialsSerializer

    def list(self, request, *args, **kwargs):
        queryset = Financial.objects.filter(user__id=request.user.id)
        serializer = self.serializer_class(queryset, many=True)
        return JSONResponse(serializer.data)


class SymbolViewset(GenericViewSet):
    serializer_class = SymbolSerializer
    queryset = Symbol.objects.all().order_by('symbol')

    def get_queryset(self):
        pk = self.kwargs.get('pk')
        queryset = self.queryset
        if pk:
            if not pk.isdigit():
                queryset = queryset.filter(symbol=pk)
            else:
                queryset = queryset.filter(pk=pk)
        return queryset

    def retrieve(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        if not queryset:
            raise Http404

        serializer = self.serializer_class(self.paginate_queryset(queryset))
        return JSONResponse(serializer.data)


class SymbolHistoryViewset(mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    serializer_class = SymbolHistorySerializer

    def get_queryset(self):
        pk = self.kwargs.get('pk')
        queryset = SymbolHistory.objects.all()
        if not pk.isdigit():
            queryset = queryset.filter(symbol__symbol=pk)
        else:
            queryset = queryset.filter(pk=pk)
        return queryset.order_by('-date')

    def retrieve(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        if not queryset:
            raise Http404

        serializer = self.serializer_class(self.paginate_queryset(queryset), many=True)
        return JSONResponse(serializer.data)
