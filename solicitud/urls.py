from django.urls import path

from solicitud.views import consulta, result

app_name = "solicitud"

urlpatterns = [
    path("", consulta, name="consulta"),
    path("result/", result, name="result"),
]
