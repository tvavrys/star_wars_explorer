import uuid

from django.core.files.base import ContentFile
from django.shortcuts import get_object_or_404, redirect
from django.views.generic import DetailView, ListView, TemplateView

import petl
from star_wars_explorer.explorer.models import Collection
from star_wars_explorer.explorer.transform import transform_people
from star_wars_explorer.swapi.client import SWAPIClient


class CollectionListView(ListView):
    """TODO"""

    model = Collection

    def post(self, request, *args, **kwargs):
        """Save a Star Wars People collection to a CSV file."""

        # TODO this should be done asynchronously. it's blocking the interface
        # for too long first time before everything is cached.
        people = list(SWAPIClient().get_people())
        table = transform_people(people)

        file = petl.io.sources.MemorySource()
        petl.tocsv(table, file)

        collection = Collection.objects.create()
        collection.csv_file.save(
            f"{uuid.uuid4().hex}.csv", ContentFile(file.getvalue())
        )
        return redirect("collections")


class CollectionDetailView(DetailView):
    """TODO"""

    model = Collection
    items_per_page = 10

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        table = petl.fromcsv(context["collection"].csv_file)

        # Paginator Context
        page = int(self.request.GET.get("page", 1))  # TODO error protection
        total_count = petl.nrows(table)
        has_next = page * self.items_per_page < total_count
        next_page = page + 1
        num_entries = page * self.items_per_page

        context.update(
            {
                "has_next": has_next,
                "next_page": next_page,
                "headers": petl.header(table),
                "data": petl.data(table, num_entries),
            }
        )
        return context


class CollectionGroupByView(TemplateView):
    """TODO"""

    model = Collection
    template_name = "explorer/collection_group_by.html"

    def get(self, request, *args, **kwargs):
        """TODO"""

        # Redirect to collections if no column is selected
        if "columns" not in self.request.GET:  # TODO improve the validation
            return redirect("collection-detail", pk=self.kwargs["pk"])

        return super().get(request, *args, **kwargs)

    def get_context_data(self, pk, **kwargs):
        context = super().get_context_data(**kwargs)

        context["object"] = get_object_or_404(Collection, pk=pk)

        group_by = self.request.GET.getlist("columns")
        table = petl.fromcsv(context["object"].csv_file)
        group_by_table = petl.valuecounts(table, *group_by).cutout("frequency")
        context.update(
            {
                "table_headers": petl.header(table),
                "headers": petl.header(group_by_table),
                "data": petl.data(group_by_table),
            }
        )
        return context
