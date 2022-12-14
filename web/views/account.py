import datetime
import uuid

from django.http import JsonResponse, HttpResponseRedirect
from django.shortcuts import render

from web import models
from web.utils import check_login
from web.forms.account import RegisterModelForm, EmailForm, LoginForm
from web.utils import login_cookie_session, logout_cookie_session


def register(request):
    # return render(request)

    if request.method == 'GET':
        form = RegisterModelForm()
        return render(request, 'web/register.html', locals())
    elif request.method == 'POST':
        form = RegisterModelForm(data=request.POST)
        # return JsonResponse({'status': True, 'href': '/web/login/'})
        # 注释掉这些 测试跳转
        if form.is_valid():
            # save中在数据库添加了对应的用户
            form.save()

            # 注册用户时 默认创建一个免费版订单
            # models.Transaction.objects.create(
            #     status=2,
            #     order=str(uuid.uuid4()),
            #     user=form.user,
            #     price_policy=models.PricePolicy.objects.get(category=1),
            #     count=0,
            #     price=0,
            #     start_datetime=datetime.datetime.now()
            # )

            if form.user is None:
                return JsonResponse({'status': False, 'error': form.errors})
            else:
                response = JsonResponse({'status': True, 'href': '/index/'})
                return login_cookie_session(request, response, user=form.user, max_age=3600 * 24)
        else:
            return JsonResponse({'status': False, 'error': form.errors})


def send_mail(request):
    # 这个路由存在的意义:当要求发送邮箱时做的操作
    if request.method == 'GET':
        email_form = EmailForm(data=request.GET)
        # 调用is_valid 会 自动清理所有字段
        if email_form.is_valid():  # 验证通过则 发邮箱(同时存redis)
            return JsonResponse({'status': True})
        else:
            return JsonResponse({'status': False, 'error': email_form.errors})
    else:
        pass


def login_view(request):
    if request.method == 'GET':
        form = LoginForm()
        return render(request, 'web/login.html', locals())
    elif request.method == 'POST':
        form = LoginForm(data=request.POST)
        if form.is_valid():
            if form.user is not None:
                response = JsonResponse({'status': True, 'href': '/index/'})
                return login_cookie_session(request, response, user=form.user, max_age=3600 * 24)
            else:  # 极端情况下的并发请求
                return JsonResponse({'status': False, 'error': form.errors})
        else:
            return JsonResponse({'status': False, 'error': form.errors})


@check_login
def logout(request):
    response = HttpResponseRedirect('/index/')
    return logout_cookie_session(request, response)
