from django.views import generic
from django.shortcuts import render,redirect
from django.contrib.auth import authenticate,login

from .models import Album
from django.views.generic.edit import CreateView,UpdateView,DeleteView
from django.core.urlresolvers import reverse_lazy
from django.views.generic import View
from .forms import UserForm
class IndexView(generic.ListView):
    template_name = 'music/index.html'
    context_object_name = 'all_albums'
    def get_queryset(self):
        return Album.objects.all()


class DetailsView(generic.DetailView):
    model=Album
    template_name = 'music/detail.html'


class AlbumCreate (CreateView):
    model=Album
    fields = ['artist','album_title','genre','album_logo']


class AlbumUpdate (UpdateView):
    model=Album
    fields = ['artist','album_title','genre','album_logo']

class AlbumDelete(DeleteView):
    model=Album
    success_url = reverse_lazy('music:index')


class UserFormView(View):
    form_class=UserForm
    template_name='music/registration_form.html'

    #display blank form
    def get(self,request):
        form=self.form_class(None)
        return render(request,self.template_name,{'form':form})


    #process to the database
    def post(self,request):
        form=self.form_class(request.POST)
        if form.is_valid():
            user=form.save(commit=False)
            #cleaned (normalized) data
            username=form.cleaned_data['username']
            password=form.cleaned_data['password']
            user.set_password(password)
            user.save()


            #returns user objects if credentials are correct

            user=authenticate(username=username,password=password)
            if user is not None:
                if user.is_active:
                    login(request,user)
                    return redirect('music:index')


        return render(request,self.template_name,{'form':form})

def logout_user(request):
    logout(request)
    form = UserForm(request.POST or None)
    context = {
        "form": form,
    }
    return render(request, 'music/login.html', context)


def login_user(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                albums = Album.objects.filter(user=request.user)
                return render(request, 'music/index.html', {'albums': albums})
            else:
                return render(request, 'music/login.html', {'error_message': 'Your account has been disabled'})
        else:
            return render(request, 'music/login.html', {'error_message': 'Invalid login'})
    return render(request, 'music/login.html')

def register(request):
    form = UserForm(request.POST or None)
    if form.is_valid():
        user = form.save(commit=False)
        username = form.cleaned_data['username']
        password = form.cleaned_data['password']
        user.set_password(password)
        user.save()
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                albums = Album.objects.filter(user=request.user)
                return render(request, 'music/index.html', {'albums': albums})
    context = {
        "form": form,
    }
    return render(request, 'music/register.html', context)
