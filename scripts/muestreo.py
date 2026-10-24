# muestreo.py — Parte B: población vs. muestra (RetailAndina).
# Uso (desde la raíz del repositorio):  python scripts/muestreo.py

import pandas as pd

pd.set_option("display.width", 100)


def reporte(nombre, muestra, parametro):
    """Imprime n, media estimada y composición por ciudad de una muestra."""
    if muestra is None:
        print(f"[{nombre}] pendiente de completar (TODO)")
        return
    n = len(muestra)
    media = muestra["ingresos_mensuales"].mean()
    comp = muestra["ciudad"].value_counts().to_dict()
    print(f"[{nombre}] n={n}  media={media:.2f} USD  "
          f"(parámetro {parametro:.2f}, diferencia {media - parametro:+.2f})")
    print(f"    composición por ciudad: {comp}")


# ---------------------------------------------------------------------------
# 1. La población y su parámetro (N = 400)
# ---------------------------------------------------------------------------
poblacion = pd.read_csv("data/clientes_400.csv")
parametro = poblacion["ingresos_mensuales"].mean()
print(f"Población: {poblacion.shape[0]} clientes × {poblacion.shape[1]} columnas")
print(f"Parámetro poblacional — ingreso medio: {parametro:.2f} USD")
print("Ciudades en la población:", poblacion["ciudad"].value_counts().to_dict())
print()

# ---------------------------------------------------------------------------
# 2. Muestra por conveniencia: "los primeros que llegaron"
# ---------------------------------------------------------------------------
# TODO 1 resuelto:
muestra_conv = poblacion.head(20)

# ---------------------------------------------------------------------------
# 3. Muestra aleatoria simple: el sorteo de 20
# ---------------------------------------------------------------------------
# TODO 2 resuelto:
muestra_aas = poblacion.sample(20, random_state=1)

# TODO 3 resuelto: Variabilidad en 5 sorteos distintos (semillas 1 a 5)
print("Variabilidad del Muestreo Aleatorio Simple (semillas 1 a 5):")
for semilla in range(1, 6):
    m_temp = poblacion.sample(20, random_state=semilla)
    media_s = m_temp["ingresos_mensuales"].mean()
    dif_s = media_s - parametro
    print(f"  Semilla {semilla}: media = {media_s:.2f} USD (diferencia {dif_s:+.2f} USD)")
print()

# ---------------------------------------------------------------------------
# 4. Muestra estratificada: 5 % dentro de cada ciudad
# ---------------------------------------------------------------------------
# TODO 4 resuelto:
muestra_est = poblacion.groupby("ciudad", group_keys=False).sample(frac=0.05, random_state=1)

# ---------------------------------------------------------------------------
# 5. Comparación final
# ---------------------------------------------------------------------------
reporte("Conveniencia", muestra_conv, parametro)
reporte("Aleatorio simple", muestra_aas, parametro)
reporte("Estratificado", muestra_est, parametro)
print()

if muestra_conv is not None and muestra_aas is not None and muestra_est is not None:
    resumen = pd.DataFrame([
        {"diseño": "Conveniencia (head)", "n": len(muestra_conv),
         "media estimada": round(muestra_conv["ingresos_mensuales"].mean(), 2)},
        {"diseño": "Aleatorio simple (sample)", "n": len(muestra_aas),
         "media estimada": round(muestra_aas["ingresos_mensuales"].mean(), 2)},
        {"diseño": "Estratificado (groupby + frac)", "n": len(muestra_est),
         "media estimada": round(muestra_est["ingresos_mensuales"].mean(), 2)},
    ])
    print(f"Parámetro poblacional: {parametro:.2f} USD")
    print(resumen.to_string(index=False))