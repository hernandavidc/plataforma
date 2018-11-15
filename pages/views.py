from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse, reverse_lazy
from django.shortcuts import redirect, render, get_object_or_404

from .forms import PageForm

from .models import Page, Category

def category(request, categoryId):
    template_name = 'pages/category.html'
    category = get_object_or_404(Category, id=categoryId)
    contexto = {'category':category}
    return render(request, template_name, contexto)

class PageListView(ListView):
    model = Page

class PageDetailView(DetailView):
    model = Page

class PageCreate(CreateView):
    model = Page
    form_class = PageForm
    success_url = reverse_lazy('pages:pages')

class PageUpdate(UpdateView):
    model = Page
    form_class = PageForm
    template_name_suffix = '_update_form'
    
    def get_success_url(self):
        return reverse_lazy('pages:update', args=[self.object.id]) + '?ok'

class PageDelete(DeleteView):
    model = Page
    success_url = reverse_lazy('pages:pages')