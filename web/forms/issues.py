from django import forms
from django.db.models import QuerySet

from web import models
from web.forms.bootstrap import BootstrapForm
from web.models import Issues


class IssuesModelForm(BootstrapForm, forms.ModelForm):
    class Meta:
        model = Issues
        exclude = ['project', 'creator', ]
        # fields = '__all__'
        widgets = {
            'assign': forms.Select(
                attrs={
                    'class': 'selectpicker',
                    'data-live-search': 'true',
                    'data-action-box': 'true',
                }),
            'attention': forms.SelectMultiple(
                attrs={
                    'class': 'selectpicker',
                    'data-live-search': 'true',
                    'data-action-box': 'true',
                }),
            'parent': forms.Select(
                attrs={
                    'class': 'selectpicker',
                    'data-live-search': 'true',
                    'data-action-box': 'true',
                })
        }

    def __init__(self, project, method, *args, **kwargs):
        select_set = {'assign', 'priority'}
        forms.ModelForm.__init__(self, *args, **kwargs)
        BootstrapForm.__init__(self, select_set=select_set)
        # 部分可选字段需要进行限制
        # assign被指派人应该参加/创建了这个项目
        if method == 'GET':
            # 获取当前项目的参与者
            total_users = [(project.creator.id, project.creator.username), ]
            joiners = models.User.objects.filter(joined_project=project).values_list('id', 'username')
            total_users.extend(joiners)
            self.fields['assign'].choices = [('', '---------')] + list(total_users)
            self.fields['attention'].choices = [('', '---------')] + list(total_users)
            # 获取当前project的issue type
            issue_types = models.IssuesType.objects.filter(project=project).values_list('id', 'title')
            self.fields['issues_type'].choices = list(issue_types)
            # 获取当前project的issues
            issues = models.Issues.objects.filter(project=project).values_list('id', 'subject')
            self.fields['parent'].choices = [('', '---------')] + list(issues)
            # 获取当前项目的module
            modules = models.Module.objects.filter(project=project).values_list('id', 'title')
            self.fields['module'].choices = list(modules)
        # self.fields['parent'].required = False
