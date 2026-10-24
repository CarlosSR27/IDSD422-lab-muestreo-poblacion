# clasificacion_variables.R — Parte A: clasificación de las variables de clientes.csv.
# Uso (desde la raíz del repositorio):  Rscript scripts/clasificacion_variables.R

clientes <- read.csv("data/clientes.csv", stringsAsFactors = FALSE)

# ---------------------------------------------------------------------------
# 1. Estructura del archivo
# ---------------------------------------------------------------------------
cat(sprintf("Dimensiones: %d filas × %d columnas\n\n", nrow(clientes), ncol(clientes)))
print(clientes)
cat("\n")

# ---------------------------------------------------------------------------
# 2. Tipos inferidos (str) — la pista que da el lenguaje
# ---------------------------------------------------------------------------
cat("Estructura inferida (str):\n")
str(clientes)
cat("\n")

# ---------------------------------------------------------------------------
# 3. Valores únicos — ¿cuántas categorías hay y cuáles son?
# ---------------------------------------------------------------------------
cat("Valores únicos por columna:\n")
for (columna in names(clientes)) {
  unicos <- unique(clientes[[columna]])
  cat(sprintf(
    "  %-18s: %2d únicos -> %s\n",
    columna, length(unicos), paste(unicos, collapse = ", ")
  ))
}
cat("\n")

# ---------------------------------------------------------------------------
# 4. Declarar el orden de las variables ordinales
# ---------------------------------------------------------------------------
# TODO 3: nivel_educacion como factor ordenado
niveles_edu <- c("Primaria", "Secundaria", "Universitaria", "Posgrado")
clientes$nivel_educacion_ord <- factor(clientes$nivel_educacion,
  levels = niveles_edu,
  ordered = TRUE
)
cat("Verificación de orden en nivel_educacion:\n")
cat(
  "  Mínimo:", as.character(min(clientes$nivel_educacion_ord)),
  "| Máximo:", as.character(max(clientes$nivel_educacion_ord)), "\n"
)

# Prueba extra (typo 'Postgrado' con t):
edu_typo <- factor(clientes$nivel_educacion,
  levels = c("Primaria", "Secundaria", "Universitaria", "Postgrado"),
  ordered = TRUE
)
cat("  Faltantes (NA) por typo 'Postgrado':", sum(is.na(edu_typo)), "\n")

# TODO 4: satisfaccion (escala 1-5) como factor ordenado
clientes$satisfaccion_ord <- factor(clientes$satisfaccion,
  levels = 1:5,
  ordered = TRUE
)
cat(
  "  Satisfacción ordenada -> Mínimo:", as.character(min(clientes$satisfaccion_ord)),
  "| Máximo:", as.character(max(clientes$satisfaccion_ord)), "\n"
)

# ---------------------------------------------------------------------------
# 5. Resumen de la clasificación (para el informe)
# ---------------------------------------------------------------------------
clasificacion <- c(
  cliente_id         = "Categórica nominal (identificador)",
  edad               = "Numérica continua (discretizada en años cumplidos)",
  numero_hijos       = "Numérica discreta",
  genero             = "Categórica binaria (nominal)",
  nivel_educacion    = "Categórica ordinal",
  ciudad             = "Categórica nominal",
  ingresos_mensuales = "Numérica continua",
  satisfaccion       = "Categórica ordinal (codificada 1-5)"
)
cat("\nResumen de la clasificación (para el informe):\n")
for (variable in names(clasificacion)) {
  cat(sprintf("  %-18s %s\n", variable, clasificacion[[variable]]))
}
