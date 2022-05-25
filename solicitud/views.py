from statistics import mean
from django.shortcuts import render
import requests
import plotly.express as px

# Create your views here.
def consulta(request):
    return render(request, "solicitud/consulta.html")


def result(request):
    response = requests.get(
        f"https://www.banxico.org.mx/SieAPIRest/service/v1/series/SP68257,SF43718/datos/{request.GET['startDate']}/{request.GET['endDate']}",
        headers={
            "Bmx-Token": "ce7c405c95c769d87c965a393a5eddcc234986b3988a6426f6075922b47623c2"
        },
    )
    response_json = response.json()

    for serie in response_json["bmx"]["series"]:
        if serie["idSerie"] == "SF43718":
            dolar_datos = serie["datos"]

        if serie["idSerie"] == "SP68257":
            udis_datos = serie["datos"]

    dolar_values = [float(entry["dato"]) for entry in dolar_datos]
    dolar_fig = px.line(
        x=[entry["fecha"] for entry in dolar_datos], y=dolar_values, title="Dolar"
    )
    dolar_fig.update_xaxes(title_text="Fecha")
    dolar_fig.update_yaxes(title_text="Valor")
    dolar_plot = dolar_fig.to_html(full_html=False, include_plotlyjs="cdn")
    dolar_data = {
        "datos": dolar_datos,
        "mean": round(mean(dolar_values), 4),
        "min": min(dolar_values),
        "max": max(dolar_values),
        "plot": dolar_plot,
    }

    udis_values = [float(entry["dato"]) for entry in udis_datos]
    udis_fig = px.line(
        x=[entry["fecha"] for entry in udis_datos], y=udis_values, title="UDIS"
    )
    udis_fig.update_xaxes(title_text="Fecha")
    udis_fig.update_yaxes(title_text="Valor")
    udis_plot = udis_fig.to_html(full_html=False, include_plotlyjs="cdn")
    udis_data = {
        "datos": udis_datos,
        "mean": round(mean(udis_values), 6),
        "min": min(udis_values),
        "max": max(udis_values),
        "plot": udis_plot,
    }

    return render(
        request, "solicitud/resultados.html", {"dolar": dolar_data, "udis": udis_data}
    )
