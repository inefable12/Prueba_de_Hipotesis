import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import norm

# Configuración de la página
st.title("Prueba de Hipótesis: Lanzamiento de una Moneda")
st.write("""
Esta aplicación permite realizar una prueba de hipótesis para determinar si una moneda es justa, basada en el número de caras observadas en un conjunto de lanzamientos.
""")

# Entradas del usuario
n = st.number_input("Número total de lanzamientos (n):", min_value=1, value=100, step=1)
k = st.number_input("Número de caras observadas (k):", min_value=0, max_value=n, value=60, step=1)
alpha = st.number_input("Nivel de significancia (α):", min_value=0.001, max_value=0.1, value=0.05, step=0.001)

# Función para calcular el p-value
def calcular_p_value(n, k):
    p = 0.5
    mu = n * p
    sigma = np.sqrt(n * p * (1 - p))
    z = (k - mu) / sigma
    p_value = 2 * (1 - norm.cdf(abs(z)))
    return p_value, z, mu, sigma

# Botón para calcular el valor de p
if st.button("Calcular p-value"):
    p_value, z, mu, sigma = calcular_p_value(n, k)
    st.write(f"**Valor-p:** {p_value:.4f}")
    st.write(f"**Estadístico Z:** {z:.2f}")

    # Generar la figura
    x = np.linspace(mu - 4 * sigma, mu + 4 * sigma, 500)
    y = norm.pdf(x, mu, sigma)
    fig, ax = plt.subplots(figsize=(8, 5))

    ax.plot(x, y, label="Distribución Normal")
    ax.axvline(k, color="red", linestyle="--", label=f"Valor observado (k={k})")
    ax.axvline(mu + norm.ppf(1 - alpha / 2) * sigma, color="green", linestyle="--", label="Límite crítico superior")
    ax.axvline(mu - norm.ppf(1 - alpha / 2) * sigma, color="green", linestyle="--", label="Límite crítico inferior")
    ax.fill_between(x, y, where=(x >= mu + norm.ppf(1 - alpha / 2) * sigma) | (x <= mu - norm.ppf(1 - alpha / 2) * sigma), color="orange", alpha=0.5, label="Regiones críticas")
    ax.set_title("Distribución Normal y Regiones Críticas")
    ax.set_xlabel("Número de caras observadas")
    ax.set_ylabel("Densidad de probabilidad")
    ax.legend()
    st.pyplot(fig)

# Botón para aceptar/rechazar la hipótesis nula
if st.button("Decidir sobre la hipótesis nula"):
    p_value, z, mu, sigma = calcular_p_value(n, k)
    if p_value < alpha:
        st.write(f"**Rechazamos \(H_0\):** Hay evidencia suficiente para concluir que la moneda no es justa (α={alpha}).")
    else:
        st.write(f"**No rechazamos \(H_0\):** No hay evidencia suficiente para concluir que la moneda no es justa (α={alpha}).")
