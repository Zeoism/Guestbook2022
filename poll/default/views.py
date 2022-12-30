from ast import Delete
from dataclasses import fields
from re import U, template
from sre_constants import SUCCESS
from django.shortcuts import render
#from .models import Poll,Option
from django.views.generic import ListView, DetailView, RedirectView, CreateView, UpdateView, DeleteView                            
from .models import *
# Create your views here.

def poll_list(req):
    
    polls = Poll.objects.all()
    
    return render(req,'poll_list.html',{'list_poll':polls})

class PollList(ListView):
    
    model = Poll

class PollView(DetailView):

    model = Poll

    def get_context_data(self, **kwargs):

        ctx = super().get_context_data(**kwargs)
        ctx['option_list'] = Option.objects.filter(poll_id=self.object.id)
        #ctx['option_list'] = Option.objects.filter(poll_id=self.kwargs['pk'])
        return ctx

class PollVote(RedirectView):
    #url = 'http://www.google.com/'  
    def get_redirect_url(self, *args, **kwargs):

        option = Option.objects.get(id=self.kwargs['oid'])
        option.count += 1 
        option.save()
        
        return "/poll/{}/".format(option.poll_id)
        return "/poll/" * str(option.poll_id) + "/"
        #return super().get_redirect_url(*args, **kwargs)
          
class PollCreate(CreateView):

    model = Poll

    fields = ['subject']

    success_url = '/poll/'

    extra_context = {'mytitle': 'Add new vote subject'}

class PollEdit(UpdateView):

    model = Poll

    fields = ['subject']

    def get_success_url(self):
        return "/poll/{}/".format(self.object.id)

    extra_context = {'mytitle': 'Edit vote subject'}

class PollDelete(DeleteView):

    model = Poll

    success_url = '/poll/'


class OptionCreate(CreateView):

    model = Option

    fields = ['title']

    def form_valid(self, form):
        
        form.instance.poll_id = self.kwargs['pk']

        return super().form_valid(form)

    def get_success_url(self):

        return "/poll/{}/".format(self.kwargs['pk'])

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['datatype'] = 'Option'
        
        return ctx


class OptionEdit(UpdateView):
    
    models = Option

    fields = ['title']

    template_name = 'default/poll_form.html'

    pkp_url_kwarg = 'oid'

    def get_success_url(self):
        return "/poll/{}/".format(self.object.id)

class OptionDelete(DeleteView):

    model = Option

    pk_url_kwarg = 'oid'

    template_name = 'default/poll_confirm_delete.html'

    def get_success_url(self):

        return '/poll/{}/'.format(self.object.poll_id)