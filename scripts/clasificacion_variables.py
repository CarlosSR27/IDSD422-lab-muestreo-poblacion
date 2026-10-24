# clasificacion_variables.py — Parte A: clasificación de las variables de clientes.csv.
# Uso (desde la raíz del repositorio):  python scripts/clasificacion_variables.py

import pandas as pd

clientes = pd.read_csv("data/clientes.csv")

# ---------------------------------------------------------------------------
# 1. Estructura del archivo
# ---------------------------------------------------------------------------
print(f"Dimensiones: {clientes.shape[0]} filas × {clientes.shape[1]} columnas\n")
print("Primeras filas:")
print(clientes.to_string(index=False))
print()

# ---------------------------------------------------------------------------
# 2. Tipos inferidos (dtype) — la pista que da el lenguaje
# ---------------------------------------------------------------------------
print("Tipos inferidos (dtype):")
print(clientes.dtypes)
print()
# TODO 1 resuelto:
# Numéricas inferidas (int64/float64): cliente_id, edad, numero_hijos, ingresos_mensuales, satisfaccion.
# Texto inferido (object/string): genero, nivel_educacion, ciudad.

# ---------------------------------------------------------------------------
# 3. Valores únicos — ¿cuántas categorías hay y cuáles son?
# ---------------------------------------------------------------------------
print("Valores únicos por columna:")
for columna in clientes.columns:
    unicos = clientes[columna].unique()
    print(f"  {columna:20s}: {len(unicos):2d} únicos -> {unicos}")
print()

# ---------------------------------------------------------------------------
# 4. Declarar el orden de las variables ordinales
# ---------------------------------------------------------------------------
# TODO 3: Convertir nivel_educacion a categoría ordenada
orden_educacion = ["Primaria", "Secundaria", "Universitaria", "Posgrado"]
tipo_educacion = pd.CategoricalDtype(categories=orden_educacion, ordered=True)
clientes["nivel_educacion_ord"] = clientes["nivel_educacion"].astype(tipo_educacion)

print("Verificación de orden en nivel_educacion:")
print(f"  Mínimo: {clientes['nivel_educacion_ord'].min()} | Máximo: {clientes['nivel_educacion_ord'].max()}")

# Prueba extra (trampa del typo silencioso con 'Postgrado'):
tipo_typo = pd.CategoricalDtype(categories=["Primaria", "Secundaria", "Universitaria", "Postgrado"], ordered=True)
na_generados = clientes["nivel_educacion"].astype(tipo_typo).isna().sum()
print(f"  Faltantes (NaN) al escribir 'Postgrado' con t: {na_generados}")

# TODO 4: Convertir satisfaccion (escala 1-5) a categoría ordenada
tipo_satisfaccion = pd.CategoricalDtype(categories=[1, 2, 3, 4, 5], ordered=True)
clientes["satisfaccion_ord"] = clientes["satisfaccion"].astype(tipo_satisfaccion)
print(f"  Satisfacción ordenada -> Mínimo: {clientes['satisfaccion_ord'].min()} | Máximo: {clientes['satisfaccion_ord'].max()}")
print()

# ---------------------------------------------------------------------------
# 5. Resumen de la clasificación (para el informe)
# ---------------------------------------------------------------------------
clasificacion = {
    "cliente_id": "Categórica nominal (identificador)",
    "edad": "Numérica continua (discretizada en años cumplidos)",
    "numero_hijos": "Numérica discreta",
    "genero": "Categórica binaria (nominal)",
    "nivel_educacion": "Categórica ordinal",
    "ciudad": "Categórica nominal",
    "ingresos_mensuales": "Numérica continua",
    "satisfaccion": "Categórica ordinal (codificada 1-5)",
}
print("Resumen de la clasificación (para el informe):")
for variable, tipo in clasificacion.items():
    print(f"  {variable:20s} {tipo}")