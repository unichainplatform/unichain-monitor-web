from rest_framework.permissions import AllowAny
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
import traceback as tb
from monitor import monitor_result
from django.views.generic import TemplateView


class MonitorResultAPI(APIView):
    """
    监控结果
    ---
    """
    permission_classes = (AllowAny,)
    http_method_names = ['get']

    def get(self, request, *args, **kwargs):
        return Response(monitor_result(), status=status.HTTP_200_OK)


class IndexView(TemplateView):
    template_name = 'index.html'

    def get_context_data(self, **kwargs):
        context = super(IndexView, self).get_context_data(**kwargs)
        context['monitor_data'] = monitor_result()
        context['fake'] = {"a": 1, "b": 2, "c": 3}
        return context