import streamlit as st

def run():
    # Título principal
    st.title("Análisis Estacional en Mercados de Futuros y Divisas")

    # Introducción
    st.markdown(
        """
        Invertir en los mercados de futuros y divisas puede ser un desafío, pero el análisis de estacionalidad 
        proporciona una ventaja clave para identificar patrones recurrentes y mejorar la toma de decisiones.
        """
    )

    # Sección: ¿Qué es la estacionalidad?
    st.header("¿Qué es la estacionalidad y por qué es importante?")
    st.markdown(
        """
        La estacionalidad se refiere a patrones de comportamiento que se repiten en ciertos períodos del año. 
        Estos patrones pueden estar influenciados por:
        - **Factores económicos**: Actividad comercial y fiscal.
        - **Climáticos**: Ciclos de siembra y cosecha en productos agrícolas.
        - **Políticos y sociales**: Eventos recurrentes como elecciones o vacaciones.

        **Beneficios del análisis estacional:**
        - **Predicción precisa:** Anticipa movimientos de precios con datos históricos.
        - **Reducción de riesgos:** Identifica periodos de alta volatilidad.
        - **Mejor timing:** Optimiza puntos de entrada y salida.
        """
    )

    # Sección: ¿Por qué se forman las tendencias estacionales?
    st.header("¿Por qué se forman las tendencias estacionales?")
    st.markdown(
        """
        Las tendencias estacionales tienen razones lógicas detrás, como:

        1. **Ciclos económicos:** Picos y caídas en función del año fiscal o temporadas clave.
        2. **Factores climáticos y agrícolas:** Impacto de las estaciones en la producción y precios de materias primas.
        3. **Eventos anuales recurrentes:** Festividades, políticas monetarias planificadas o ciclos de consumo.
        4. **Psicología del mercado:** Comportamiento cíclico de los inversores.
        """
    )

    # Sección: Aplicación práctica
    st.header("Aplicación práctica en tu estrategia de inversión")
    st.markdown(
        """
        Incorporar el análisis de estacionalidad en tus estrategias te permite anticiparte a oportunidades clave. Por ejemplo:

        - **Divisas:** Aprovechar la fortaleza del dólar en el cuarto trimestre debido a la alta actividad económica.
        - **Futuros de energía:** Identificar aumentos de precios del petróleo en verano, cuando la demanda de combustible es mayor.

        El análisis estacional no solo ayuda a comprender el mercado, sino también a optimizar tus decisiones de inversión.
        """
    )

    # Conclusión
    st.header("Conclusión")
    st.markdown(
        """
        El análisis de estacionalidad es una herramienta invaluable para cualquier inversor. 
        Aprovechar estos patrones históricos puede optimizar tus decisiones, reducir riesgos y maximizar beneficios. 
        ¡Empieza hoy mismo a incorporar la estacionalidad en tu estrategia de inversión!
        """
    )
