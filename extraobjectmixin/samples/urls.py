from django.urls import path

from extraobjectmixin.samples.views import MyExtraObjectView


urlpatterns = [
    # The URL must also contain  the `extramodel_pk` defined in the view
    path('modela/<int:pk>/<int:extramodel_pk>/details/', MyExtraObjectView.as_view(), name='modela_details'),
]
