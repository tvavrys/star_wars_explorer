from django.urls import path

from star_wars_explorer.explorer import views

urlpatterns = [
    path("", views.CollectionListView.as_view(), name="collections"),
    path(
        "collection/<int:pk>/",
        views.CollectionDetailView.as_view(),
        name="collection-detail",
    ),
    path(
        "collection/<int:pk>/group-by/",
        views.CollectionGroupByView.as_view(),
        name="collection-group-by-view",
    ),
]
