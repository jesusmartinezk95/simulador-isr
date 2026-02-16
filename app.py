from flask import Flask, render_template, request, send_file
import os
from calculos import leer_nominas, leer_deducciones
from tarifas import calcular_isr
from excel import generar_excel

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    resultado = None
    archivo_excel = None

    if request.method == "POST":
        nominas = request.files.getlist("nominas")
        deducciones_files = request.files.getlist("deducciones")

        ingresos, isr_retenido = leer_nominas(nominas)
        deducciones, detalles = leer_deducciones(deducciones_files)

        limite = min(ingresos * 0.15, 189222)  # aprox UMA
        deducciones_aplicables = min(deducciones, limite)

        base = ingresos - deducciones_aplicables
        isr_calculado = calcular_isr(base)

        saldo = isr_retenido - isr_calculado

        resumen = {
            "Ingresos": ingresos,
            "ISR retenido": isr_retenido,
            "Deducciones": deducciones_aplicables,
            "Base": base,
            "ISR calculado": isr_calculado,
            "Saldo": saldo
        }

        archivo_excel = "reporte.xlsx"
        generar_excel(resumen, archivo_excel)

        resultado = resumen

    return render_template("index.html", resultado=resultado, archivo=archivo_excel)


@app.route("/descargar")
def descargar():
    return send_file("reporte.xlsx", as_attachment=True)


if __name__ == "__main__":
    app.run() 
