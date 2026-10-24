# muestreo.R — Parte B: población vs. muestra (RetailAndina).
# Uso (desde la raíz del repositorio):  Rscript scripts/muestreo.R

suppressPackageStartupMessages(library(dplyr))

poblacion <- read.csv("data/clientes_400.csv")

reporte <- function(nombre, muestra, parametro) {
  if (is.null(muestra)) {
    cat(sprintf("[%s] pendiente de completar (TODO)\n", nombre))
    return(invisible(NULL))
  }
  media <- mean(muestra$ingresos_mensuales)
  cat(sprintf(
    "[%s] n=%d  media=%.2f USD  (parámetro %.2f, diferencia %+.2f)\n",
    nombre, nrow(muestra), media, parametro, media - parametro
  ))
  cat("    composición por ciudad: ")
  comp <- table(muestra$ciudad)
  cat(paste(names(comp), comp, sep = ": ", collapse = ", "), "\n")
}

# ---------------------------------------------------------------------------
# 1. La población y su parámetro (N = 400)
# ---------------------------------------------------------------------------
cat(sprintf("Población: %d clientes × %d columnas\n", nrow(poblacion), ncol(poblacion)))
parametro <- mean(poblacion$ingresos_mensuales)
cat(sprintf("Parámetro poblacional — ingreso medio: %.2f USD\n", parametro))
cat("Ciudades en la población:\n")
print(table(poblacion$ciudad))
cat("\n")

# ---------------------------------------------------------------------------
# 2. Muestra por conveniencia: "los primeros que llegaron"
# ---------------------------------------------------------------------------
# TODO 1 resuelto:
muestra_conv <- head(poblacion, 20)

# ---------------------------------------------------------------------------
# 3. Muestra aleatoria simple: el sorteo de 20
# ---------------------------------------------------------------------------
# TODO 2 resuelto:
set.seed(1)
muestra_aas <- poblacion[sample(nrow(poblacion), 20), ]

# TODO 3 resuelto: Semillas 1 a 5
cat("Variabilidad del Muestreo Aleatorio Simple en R (semillas 1 a 5):\n")
for (semilla in 1:5) {
  set.seed(semilla)
  m_temp <- poblacion[sample(nrow(poblacion), 20), ]
  media_s <- mean(m_temp$ingresos_mensuales)
  cat(sprintf(
    "  Semilla %d: media = %.2f USD (diferencia %+.2f USD)\n",
    semilla, media_s, media_s - parametro
  ))
}
cat("\n")

# ---------------------------------------------------------------------------
# 4. Muestra estratificada: 5 % dentro de cada ciudad
# ---------------------------------------------------------------------------
# TODO 4 resuelto:
set.seed(1)
muestra_est <- poblacion |>
  group_by(ciudad) |>
  slice_sample(prop = 0.05) |>
  ungroup()

# ---------------------------------------------------------------------------
# 5. Comparación final
# ---------------------------------------------------------------------------
reporte("Conveniencia", muestra_conv, parametro)
reporte("Aleatorio simple", muestra_aas, parametro)
reporte("Estratificado", muestra_est, parametro)
cat("\n")

if (!is.null(muestra_conv) && !is.null(muestra_aas) && !is.null(muestra_est)) {
  resumen <- data.frame(
    diseno = c("Conveniencia (head)", "Aleatorio simple (sample)", "Estratificado (slice_sample)"),
    n = c(nrow(muestra_conv), nrow(muestra_aas), nrow(muestra_est)),
    media_estimada = round(c(
      mean(muestra_conv$ingresos_mensuales),
      mean(muestra_aas$ingresos_mensuales),
      mean(muestra_est$ingresos_mensuales)
    ), 2)
  )
  cat(sprintf("Parámetro poblacional: %.2f USD\n", parametro))
  print(resumen, row.names = FALSE)
}
