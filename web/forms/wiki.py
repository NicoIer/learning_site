from web import models
from django import forms
from web.forms.bootstrap import BootstrapForm


# ToDo 所有的form都有一个问题 get 和 post 时的 __init__ 不需要一样  优化它
class WikiModelForm(forms.ModelForm, BootstrapForm):
    def __init__(self, project, method, *args, **kwargs):
        # super调用 学到了没
        forms.ModelForm.__init__(self, *args, **kwargs)
        # BootstrapForm 并没有fields字段 实际上是从self的父类中找到的fields
        BootstrapForm.__init__(self, *args, **kwargs)
        #
        if method == 'get':
            parent_wikis = [("", 'NULL')]
            parent_wikis.extend(list(models.Wiki.objects.filter(project=project).values_list('id', 'title')))
            self.fields['parent'].choices = parent_wikis

    def is_valid(self):
        return super(forms.ModelForm, self).is_valid()

    class Meta:
        model = models.Wiki
        exclude = ['project', 'level']

    def save(self, commit=True):
        if self.instance.parent:
            self.instance.level = self.instance.parent.level + 1
        super(forms.ModelForm, self).save()
