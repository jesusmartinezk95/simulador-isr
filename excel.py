import pandas as pd


def generar_excel(resumen, ruta):
    df = pd.DataFrame([resumen])
    df.to_excel(ruta, index=False) 
