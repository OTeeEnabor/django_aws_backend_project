from django.urls import path

from opendelta_store.views import OrderView


urlpatterns = [path("orders/", OrderView.as_view(), name="all-orders")]
