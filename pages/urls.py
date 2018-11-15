from django.urls import path
from django.contrib.admin.views.decorators import staff_member_required
from .views import PageListView, PageDetailView, PageCreate, PageUpdate, PageDelete, category

pages_patterns = ([
    path('', PageListView.as_view(), name='pages'),
    path('<int:pk>/<slug:slug>/', PageDetailView.as_view(), name='page'),
    path('nuevo/', staff_member_required(PageCreate.as_view()), name='create'),
    path('editar/<int:pk>', staff_member_required(PageUpdate.as_view()), name='update'),
    path('borrar/<int:pk>', staff_member_required(PageDelete.as_view()), name='delete'),
    path('categoria/<int:categoryId>/', category, name="category"),
], 'pages')