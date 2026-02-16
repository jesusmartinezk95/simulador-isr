import os
from lxml import etree

METODOS_VALIDOS = ["02", "03", "04", "05", "28"]


def leer_nominas(files):
    ingresos = 0
    isr_retenido = 0

    for f in files:
        tree = etree.parse(f)
        root = tree.getroot()

        total = root.attrib.get("Total")
        if total:
            ingresos += float(total)

        retenciones = root.findall(".//{*}Retencion")
        for r in retenciones:
            if r.attrib.get("Impuesto") == "001":
                isr_retenido += float(r.attrib.get("Importe"))

    return ingresos, isr_retenido


def leer_deducciones(files):
    deducciones = 0
    detalles = []

    for f in files:
        tree = etree.parse(f)
        root = tree.getroot()

        metodo = root.attrib.get("MetodoPago")

        if metodo not in METODOS_VALIDOS:
            continue

        total = float(root.attrib.get("Total", 0))
        deducciones += total

        detalles.append({
            "total": total,
            "metodo": metodo
        })

    return deducciones, detalles
