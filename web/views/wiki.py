from django.http import HttpResponse
from django.shortcuts import render, redirect

from web import models
from web.forms.wiki import WikiModelForm
from web.utils import check_login


@check_login
def home(request, project_id: int, ):
    try:
        project = models.Project.objects.get(id=project_id)
    except Exception:
        return redirect('project_list')
    if (project in request.tracer.user.joined_project.all()) or (project in request.tracer.user.project_set.all()):
        return render(request, 'web/wiki.html', locals())
    else:
        return redirect('project_list')


@check_login
def add(request, project_id: int):
    try:
        project = models.Project.objects.get(id=project_id)
    except Exception:
        return redirect('project_list')

    if request.method == 'GET':
        form = WikiModelForm()
        return render(request, 'web/wiki_add.html', locals())
    elif request.method == 'POST':
        form = WikiModelForm(request.POST)
        form.instance.project = project
        form.instance.parent = None
        if form.is_valid():
            form.save()
            return redirect('wiki', project_id)
        else:
            return HttpResponse('添加失败')
