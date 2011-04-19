from django.forms import ModelForm
from django import forms
from django.utils.translation import ugettext_lazy as _

from dinette.models import Ftopics ,Reply

import settings

#create a form from this Ftopics and use this when posting the a Topic
class FtopicForm(ModelForm):
    subject = forms.CharField(label=_('Subject'), widget=forms.TextInput(attrs={"size":90}))
    message = forms.CharField(label=_('Message'), widget=forms.Textarea(attrs={"cols":90, "rows":10}))
    class Meta:
        model = Ftopics
        try: #TODO better way
            if settings.HIDE_MARKUP:
                fields = ('subject', 'message', 'file' )
            else:
                fields = ('subject', 'message', 'message_markup_type', 'file' )
        except AttributeError:
            fields = ('subject', 'message', 'message_markup_type', 'file' )
            

#create a form from Reply
class ReplyForm(ModelForm):
    message = forms.CharField(label=_('Message'), widget=forms.Textarea(attrs={"cols":90, "rows":10}))
    class Meta:
        model = Reply
        try:
            if settings.HIDE_MARKUP:
                fields = ('message', 'file')
            else: 
                fields = ('message', 'message_markup_type', 'file')
        except AttributeError:
            fields = ('message', 'message_markup_type', 'file')
            
