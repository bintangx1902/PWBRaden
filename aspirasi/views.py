from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy, reverse
from django.views.generic import *
from .forms import *
from django.http import HttpResponseRedirect
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required


def home(request):
    return render(request, 'main.html')


class MyList(ListView):
    template_name = 'list.html'
    model = Aspiration
    paginate_by = 20
    ordering = ['-date_created']

    def get_queryset(self):
        object_list = Aspiration.objects.filter(penduduk=self.request.user.id)
        return object_list

    def get_ordering(self):
        return self.ordering

    @method_decorator(login_required(login_url='/accounts/login/'))
    def dispatch(self, request, *args, **kwargs):
        return super(MyList, self).dispatch(request, *args, **kwargs)


class CreateAnAspiration(CreateView):
    form_class = AddAspirationsForm
    model = Aspiration
    success_url = reverse_lazy('aspirasi:my-list')
    template_name = 'create.html'

    def form_valid(self, form):
        form.instance.penduduk_id = self.request.user.id
        a = super().form_valid(form)
        b = HttpResponseRedirect(self.get_success_url())
        return a and b

    @method_decorator(login_required(login_url='/accounts/login/'))
    def dispatch(self, request, *args, **kwargs):
        return super(CreateAnAspiration, self).dispatch(request, *args, **kwargs)


def check_profile(request):
    profile_ = Address.objects.filter(penduduk=request.user.id).count()
    profile_ = int(profile_)
    if profile_ == 0:
        # ini kalau dia belum bikin di lempar ke halama bikin
        return HttpResponseRedirect(reverse('aspirasi:create-profile'))
    else:
        # kalau sudah maka ke halaman profile
        return HttpResponseRedirect(reverse('aspirasi:show-profile'))


class CreateProfile(CreateView):
    model = Address
    form_class = AddProfileForm
    success_url = reverse_lazy('aspirasi:show-profile')
    template_name = 'create-profile.html'

    # def get_context_data(self, **kwargs):
    #     context = super(CreateProfile, self).get_context_data(**kwargs)
    #     user_ = Address.objects.filter(penduduk_id=self.request.user.id).count()
    #     if user_ != 0:
    #         return HttpResponseRedirect(redirect('aspirasi:show-profile'))
    #     else:
    #         pass
    #
    #     return context

    def form_valid(self, form):
        form.instance.penduduk_id = self.request.user.id
        a = super(CreateProfile, self).form_valid(form)
        b = HttpResponseRedirect(self.get_success_url())
        return a and b

    @method_decorator(login_required(login_url='/accounts/login/'))
    def dispatch(self, request, *args, **kwargs):
        return super(CreateProfile, self).dispatch(request, *args, **kwargs)


class MyProfile(TemplateView):
    # model = Address
    template_name = 'profile.html'

    def get_context_data(self, *args, **kwargs):
        context = super(MyProfile, self).get_context_data(*args, **kwargs)
        address_ = Address.objects.filter(penduduk_id=self.request.user.id)
        if address_ is None:
            return reverse('aspirasi:create-profile')
        else:
            address = Address.objects.filter(penduduk_id=self.request.user.id)

            context['address'] = address
            return context


def my_profile(request):
    address_ = Address.objects.filter(penduduk_id=request.user.id).count()

    if address_ == 0:
        return redirect('aspirasi:create-profile')
    else:
        address_ = Address.objects.get(penduduk_id=request.user.id)

    context = {
        'address': address_,
    }
    return render(request, 'profile.html', context)


def profile_check(request):
    profile_ = Address.objects.filter(penduduk_id=request.user.id)

    if profile_ is not None:
        return redirect('aspirasi:show-profile')
    else:
        return redirect('aspirasi:create-profile')


@login_required(login_url='/accounts/login/')
def update_profile(request):
    this_id = Address.objects.get(penduduk_id=request.user.id)
    form = AddProfileForm(request.POST or None, instance=this_id)
    if form.is_valid():
        form.save()
        return redirect('aspirasi:show-profile')

    con = {
        'form': form,
    }
    return render(request, 'create-profile.html', con)
