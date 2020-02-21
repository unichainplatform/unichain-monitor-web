from rest_framework.permissions import AllowAny
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
import traceback as tb
from monitor import monitor_result
from django.views.generic import TemplateView
from restapi.models import Hosts


class StartBuild(APIView):
    permission_classes = (AllowAny,)
    http_method_names = ['get']

    def get(self, request, *args, **kwargs):
        return Response('Ok', status=status.HTTP_200_OK)


class IndexView(TemplateView):
    template_name = 'index.html'

    def get_context_data(self, **kwargs):
        context = super(IndexView, self).get_context_data(**kwargs)
        context['monitor_data'] = monitor_result()
        return context


class BuilderView(TemplateView):
    template_name = 'builder.html'

    def get_context_data(self, **kwargs):
        context = super(BuilderView, self).get_context_data(**kwargs)

        vs = []
        qs = Hosts.objects.all()

        for q in qs:
            vs.append({
                "step": q.get_status_display(),
                "status": q.status,
                "ip": q.ip
            })
        context['build_data'] = vs
        return context