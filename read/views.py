from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import *
from aspirasi.models import Aspiration
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from .models import Feedback
from .utils import staff_required
from django.urls import reverse_lazy
from django.http import HttpResponseRedirect
from .forms import FeedbackForm


class AllAspirations(ListView):
    model = Aspiration
    template_name = 'read/main.html'
    ordering = ['-id'] #ini akan jadi descending order
    paginate_by = 20 #kalau ini menampilkan max 20 list dalam page

    def get_queryset(self):
        object_list = Aspiration.objects.filter(status='unread')
        return object_list

    @method_decorator(staff_required)
    def dispatch(self, request, *args, **kwargs):
        return super(AllAspirations, self).dispatch(request, *args, **kwargs)

# class AllAspirations(TemplateView):
#     template_name = 'read/main.html'
#
#     def get_context_data(self, *args, **kwargs):
#         context = super(AllAspirations, self).get_context_data(*args, **kwargs)
#         object_list = Aspiration.objects.filter(status='unread').order_by('-id')
#
#         context['object_list'] = object_list
#         return context


class ReadAspiration(DetailView):
    model = Aspiration
    template_name = 'read/details.html'
    # query_pk_and_slug = True
    # pk_url_kwarg = 'pk'

    @method_decorator(staff_required)
    def dispatch(self, request, *args, **kwargs):
        return super(ReadAspiration, self).dispatch(request, *args, **kwargs)


@staff_required
def read_view(request, pk):
    obj = Aspiration.objects.filter(pk=pk)
    if obj.exists():
        if request.user:
            obj.update(status='read')

    return redirect('read:list')


class CreateFeedback(CreateView):
    model = Feedback
    template_name = 'read/create.html'
    success_url = reverse_lazy()
    form_class = FeedbackForm
    query_pk_and_slug = True
    pk_url_kwarg = 'pk'

    def form_valid(self, form):
        id_ = Aspiration.objects.get(pk=self.kwargs['pk'])
        form.instance.staff_name_id = self.request.user.id
        form.instace.aspiration_id = id_.pk
        con = super(CreateFeedback, self).form_valid(form)
        red = HttpResponseRedirect(self.get_success_url())
        return con and red

    @method_decorator(staff_required)
    def dispatch(self, request, *args, **kwargs):
        return super(CreateFeedback, self).dispatch(request, *args, **kwargs)
