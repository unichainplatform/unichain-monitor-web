from rest_framework.permissions import AllowAny
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
import traceback as tb
from monitor import monitor_result
from django.views.generic import TemplateView
from restapi.models import Hosts, Accounts
from web.celery import app
from restapi.tasks import build
from django.shortcuts import render


def update_items(request):
    vs = []
    qs = Hosts.objects.all()

    for q in qs:
        vs.append({
            "step": q.get_status_display(),
            "status": q.status,
            "ip": q.ip
        })
    return render(request, 'table_body.html', {'build_data':vs})


class StartBuild(APIView):
    permission_classes = (AllowAny,)
    http_method_names = ['get']

    def get(self, request, *args, **kwargs):
        account = Accounts.objects.first()
        i = app.control.inspect()

        if not account or not account.public_key or not account.private_key:
            return Response({'code': -1, 'text': '请先于控制中心设置出块帐号'}, status=status.HTTP_200_OK)
        if not Hosts.objects.all():
            return Response({'code': -1, 'text': '请先于控制中心设置机器信息'}, status=status.HTTP_200_OK)
        if i.active()[list(i.active().keys())[0]]:
            return Response({'code': -1, 'text': '请勿重复点击'}, status=status.HTTP_200_OK)
        else:
            build.delay()
            return Response({'code': 1, 'text': '部署中..............'}, status=status.HTTP_200_OK)


class IndexView(TemplateView):
    template_name = 'index.html'

    def get_context_data(self, **kwargs):
        context = super(IndexView, self).get_context_data(**kwargs)
        context['monitor_data'] = monitor_result()
        return context


class BuilderView(TemplateView):
    template_name = 'builder.html'

    # def get_context_data(self, **kwargs):
    #     context = super(BuilderView, self).get_context_data(**kwargs)
    #
    #     vs = []
    #     qs = Hosts.objects.all()
    #
    #     for q in qs:
    #         vs.append({
    #             "step": q.get_status_display(),
    #             "status": q.status,
    #             "ip": q.ip
    #         })
    #     context['build_data'] = vs
    #     return context