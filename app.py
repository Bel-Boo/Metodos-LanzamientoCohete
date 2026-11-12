import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st

st.set_page_config(page_title="Cohete NASA 1962: método de Euler", page_icon="🚀", layout="wide")
st.title("🚀 Lanzamiento de un cohete por la NASA: método de Euler")
st.caption("Inspirado en la película Talentos ocultos (NASA, 1962). Datos ficticios con fines didácticos.")
st.markdown("**Autora:** Valeria Isabel Estrugo Perez")

# ---------------- Parámetros ----------------
sb = st.sidebar
sb.header("Parámetros")
m = sb.number_input("Masa m (kg)", value=1000.0)
T = sb.number_input("Empuje T (N)", value=15000.0)
g = sb.number_input("Gravedad g (m/s²)", value=9.81)
k = sb.number_input("Resistencia k (kg/s)", value=100.0)
v0 = sb.number_input("Velocidad inicial v(0) (m/s)", value=0.0)
y0 = sb.number_input("Altura inicial y(0) (m)", value=0.0)
tf = sb.number_input("Tiempo final (s)", value=20.0, min_value=1.0)
h = sb.selectbox("Paso h (s)", [2.0, 1.0, 0.5, 0.25])
metodo = sb.selectbox("Método", ["Euler", "Heun", "Runge-Kutta 4"])

a, b = T / m - g, k / m          # modelo: dv/dt = a - b v

# ---------------- Solución analítica ----------------
def exacta(t):
    t = np.asarray(t, dtype=float)
    if b > 1e-12:
        c = v0 - a / b
        return a / b + c * np.exp(-b * t), y0 + a / b * t + c * (1 - np.exp(-b * t)) / b
    return v0 + a * t, y0 + v0 * t + a * t**2 / 2

# ---------------- Métodos numéricos ----------------
def resolver(met, paso):
    f = lambda v: a - b * v
    t, v, y = 0.0, v0, y0
    filas = [(t, v, y)]
    while t < tf - 1e-9:
        s = min(paso, tf - t)
        if met == "Euler":
            v1, y1 = v + s * f(v), y + s * v
        elif met == "Heun":
            vp = v + s * f(v)
            v1, y1 = v + s / 2 * (f(v) + f(vp)), y + s / 2 * (v + vp)
        else:
            k1 = f(v); w2 = v + s / 2 * k1
            k2 = f(w2); w3 = v + s / 2 * k2
            k3 = f(w3); w4 = v + s * k3
            k4 = f(w4)
            v1 = v + s / 6 * (k1 + 2 * k2 + 2 * k3 + k4)
            y1 = y + s / 6 * (v + 2 * w2 + 2 * w3 + w4)
        t, v, y = t + s, v1, y1
        filas.append((t, v, y))
    df = pd.DataFrame(filas, columns=["t (s)", "v numérica", "y numérica"])
    ve, ye = exacta(df["t (s)"])
    df["v exacta"], df["y exacta"] = ve, ye
    df["error v"], df["error y"] = (df["v exacta"] - df["v numérica"]).abs(), (df["y exacta"] - df["y numérica"]).abs()
    return df

df = resolver(metodo, h)
fin = df.iloc[-1]

# ---------------- Modelo ----------------
st.header("1. Modelo matemático")
st.latex(r"m\frac{dv}{dt}=T-mg-kv \qquad \frac{dy}{dt}=v")
st.latex(rf"\frac{{dv}}{{dt}}={a:.2f}-{b:.2f}\,v")
st.header("2. Solución analítica")
if b > 1e-12:
    st.latex(rf"v(t)={a/b:.2f}\,\left(1-e^{{-{b:.2f}t}}\right)\quad (\text{{con }} v(0)=0)")
    st.latex(rf"y(t)={a/b:.2f}\,t-{a/b/b:.0f}\left(1-e^{{-{b:.2f}t}}\right)")
    st.caption("Estas dos fórmulas son las del enunciado original y valen cuando v(0)=0 y y(0)=0. Para otros valores iniciales la app calcula la solución exacta general.")
else:
    st.latex(r"v=v_0+a\,t \qquad y=y_0+v_0 t+\tfrac{1}{2}a t^2")

# ---------------- Resultados ----------------
st.header(f"3. Resultados con {metodo} (h = {h} s)")
c = st.columns(3)
c[0].metric("Velocidad final", f"{fin['v numérica']:.4f} m/s", f"exacta {fin['v exacta']:.4f}", delta_color="off")
c[1].metric("Altura final", f"{fin['y numérica']:.4f} m", f"exacta {fin['y exacta']:.4f}", delta_color="off")
c[2].metric("Error v / error y", f"{fin['error v']:.4f} / {fin['error y']:.4f}")
ok_v, ok_y = fin["error v"] < 0.5, fin["error y"] < 5
(st.success if ok_v and ok_y else st.warning)(
    f"Requisitos: error de velocidad < 0,5 m/s → {'cumple' if ok_v else 'no cumple'}; "
    f"error de altura < 5 m → {'cumple' if ok_y else 'no cumple'}." + ("" if ok_v and ok_y else " Prueba con un paso menor."))

# ---------------- Gráficas ----------------
st.header("4. Gráficas")
tt = np.linspace(0, tf, 300)
ve, ye = exacta(tt)
col1, col2 = st.columns(2)
for col, titulo, ex, num, un in ((col1, "Velocidad", ve, "v numérica", "m/s"), (col2, "Altura", ye, "y numérica", "m")):
    fig, ax = plt.subplots(figsize=(5.5, 3.6))
    ax.plot(tt, ex, label="Analítica", lw=2)
    ax.plot(df["t (s)"], df[num], "o-", label=metodo, color="tab:orange", ms=4)
    ax.set_xlabel("t (s)"); ax.set_ylabel(un); ax.set_title(titulo); ax.legend(); ax.grid(alpha=.3)
    col.pyplot(fig)

# ---------------- Tabla ----------------
st.header("5. Tabla de iteraciones")
st.dataframe(df.style.format("{:.4f}"), width="stretch", hide_index=True)

# ---------------- Comparación de pasos ----------------
st.header("6. ¿Qué pasa al reducir el paso? (error al tiempo final)")
filas = []
for s in (2, 1, 0.5, 0.25):
    fila = {"Paso h (s)": s}
    for met in ("Euler", "Heun", "Runge-Kutta 4"):
        z = resolver(met, s).iloc[-1]
        fila[f"{met}: error v"], fila[f"{met}: error y"] = z["error v"], z["error y"]
    filas.append(fila)
st.dataframe(pd.DataFrame(filas).style.format("{:.4f}"), width="stretch", hide_index=True)
st.info("El error baja casi a la mitad cada vez que el paso se divide entre 2 en Euler. Para el mismo paso, Runge-Kutta 4 es el más preciso, luego Heun y al final Euler.")
