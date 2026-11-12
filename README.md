# Lanzamiento de un cohete por la NASA: método de Euler

Aplicación web de simulación hecha con Streamlit para la asignatura de Métodos Numéricos. Inspirada en la película *Talentos ocultos* (NASA, 1962).

## Modelo

Segunda ley de Newton para el ascenso vertical:

    m·dv/dt = T − m·g − k·v        dy/dt = v

Con m = 1000 kg, T = 15000 N, g = 9,81 m/s², k = 100 kg/s, v(0) = 0, y(0) = 0 se obtiene `v' = 5,19 − 0,1·v`.

Solución analítica:

    v(t) = 51,9·(1 − e^(−0,1t))
    y(t) = 51,9·t − 519·(1 − e^(−0,1t))

## Qué hace la aplicación

- Permite cambiar masa, empuje, gravedad, resistencia, condiciones iniciales, tiempo final y paso h (2, 1, 0,5 y 0,25 s).
- Resuelve con Euler, y como ampliación con Heun y Runge-Kutta 4.
- Calcula la solución analítica y la compara con tabla de iteraciones, gráficas y errores.
- Verifica si se cumplen los requisitos: error de velocidad menor que 0,5 m/s y de altura menor que 5 m.

## Cómo usarla

En local: `pip install -r requirements.txt` y luego `streamlit run app.py`.

## Enlace de la aplicación

[PEGA AQUÍ TU ENLACE DE STREAMLIT COMMUNITY CLOUD]

Autor: Valeria Isabel Estrugo Perez
