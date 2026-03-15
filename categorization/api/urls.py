from django.urls import path
from .views import CategorizeTransactionView

# creating the api endpoint
urlpatterns = [
    path("categorize-transaction/", CategorizeTransactionView.as_view(), name="categorize-transaction"),
]