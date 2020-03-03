import logging
from django.views.generic import CreateView, UpdateView, \
    DeleteView, ListView, DetailView
from .forms import ItemForm
from .models import Item
from django.db.models.functions import TruncMonth

# Get an instance of a logger
logger = logging.getLogger(__name__)


class ItemCreateView(CreateView):
    form_class = ItemForm
    template_name = 'djangotask/item_form.html'


class ItemUpdateView(UpdateView):
    model = Item
    template_name = 'djangotask/item_update.html'
    fields = '__all__'


class ItemDeleteView(DeleteView):
    model = Item
    template_name = 'djangotask/item_confirm_delete.html'


class ItemDetailView(DetailView):
    model = Item
    template_name = 'djangotask/item_detail.html'
    queryset = Item.objects.select_related('unit')


class ItemListView(ListView):
    model = Item
    template_name = 'djangotask/item_list.html'

    def get_queryset(self):
        return Item.objects.all() \
            .annotate(month=TruncMonth('modified')) \
            .select_related('unit') \
            .order_by('-modified')
