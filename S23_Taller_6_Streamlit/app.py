import streamlit as st
import pandas as pd
import numpy as np
import yfinance as yf
import plotly.express as px

st.set_page_config(page_title="Observatorio Financiero · ITM", page_icon="📈", layout="wide")
st.markdown("""<style>
[data-testid="stApp"]{background:linear-gradient(145deg,#0b1425,#101f33);color:#edf4ff}
[data-testid="stSidebar"]{background:#0d1c30}
[data-testid="stMetric"]{background:#172b43;padding:15px;border-radius:14px;border:1px solid #29415b}
h1,h2,h3{letter-spacing:-.03em}
</style>""", unsafe_allow_html=True)
st.image("assets/banner_financiero.png", use_container_width=True)
st.title("FinanceLab · Mi Observatorio Financiero")
st.caption("ITM · Python · Streamlit · Yahoo Finance")

UNIVERSO = ["AAPL", "MSFT", "NVDA", "JPM", "GOOGL", "SPY", "GLD"]
st.sidebar.header("⚙️ Configura tu análisis")
tickers = st.sidebar.multiselect("Tickers", UNIVERSO, default=["AAPL", "MSFT", "JPM"], max_selections=5)
periodo = st.sidebar.selectbox("Período histórico", ["3mo", "6mo", "1y", "2y"], index=2,
    format_func=lambda x: {"3mo":"3 meses", "6mo":"6 meses", "1y":"1 año", "2y":"2 años"}[x])
capital = st.sidebar.number_input("Capital inicial (USD)", min_value=100.0, value=10000.0, step=500.0)
fuente = st.sidebar.radio("Fuente de datos", ["Yahoo Finance", "Simulados (práctica)"], index=0)

@st.cache_data(ttl=1800, show_spinner=False)
def descargar_precios(simbolos, periodo):
    datos = yf.download(list(simbolos), period=periodo, auto_adjust=True, progress=False, threads=False)
    if datos.empty:
        raise ValueError("Yahoo Finance no devolvió datos")
    if isinstance(datos.columns, pd.MultiIndex):
        cierre = datos["Close"]
    else:
        cierre = datos[["Close"]].rename(columns={"Close": simbolos[0]})
    if isinstance(cierre, pd.Series):
        cierre = cierre.to_frame(name=simbolos[0])
    cierre = cierre.reindex(columns=list(simbolos))
    return cierre.sort_index().ffill().dropna()

def simular_precios(simbolos):
    rng = np.random.default_rng(23)
    fechas = pd.bdate_range(end=pd.Timestamp.today().normalize(), periods=180)
    return pd.DataFrame({t:100*np.cumprod(1+rng.normal(.0004,.014,len(fechas))) for t in simbolos}, index=fechas)

if not tickers:
    st.info("Selecciona al menos un ticker en la barra lateral.")
    st.stop()

simulados = fuente == "Simulados (práctica)"
if simulados:
    precios = simular_precios(tickers)
else:
    try:
        with st.spinner("Consultando Yahoo Finance..."):
            precios = descargar_precios(tuple(tickers), periodo)
        if precios.empty or len(precios) < 30:
            raise ValueError("No hay suficientes precios comunes")
    except Exception as error:
        st.warning("Yahoo Finance no está disponible. Se mostrarán DATOS SIMULADOS para continuar la práctica.")
        st.caption(f"Detalle técnico: {error}")
        precios = simular_precios(tickers)
        simulados = True

if simulados:
    st.error("MODO DEMOSTRACIÓN: los resultados NO corresponden a cotizaciones reales.")
else:
    st.success("Datos históricos descargados de Yahoo Finance")

rendimientos = precios.pct_change().dropna()
cartera = rendimientos.mean(axis=1)  # Pesos iguales, rebalanceo diario.
acumulado = (1 + cartera).cumprod()
rendimiento_total = acumulado.iloc[-1] - 1
volatilidad = cartera.std(ddof=1) * np.sqrt(252)
valor_inversion = capital * acumulado

c1, c2, c3 = st.columns(3)
c1.metric("Rendimiento acumulado", f"{rendimiento_total:+.2%}")
c2.metric("Volatilidad anualizada", f"{volatilidad:.2%}")
c3.metric("Valor final teórico", f"USD {valor_inversion.iloc[-1]:,.2f}")
st.caption("Portafolio con pesos iguales y rebalanceo diario; sin costos, impuestos ni dividendos adicionales.")

p1, p2, p3 = st.tabs(["📈 Portafolio", "📊 Estadística", "ℹ️ Proyecto"])
with p1:
    st.subheader("Comparación de activos · base 100")
    base_100 = precios.div(precios.iloc[0]) * 100
    st.line_chart(base_100)
    izquierda, derecha = st.columns(2)
    with izquierda:
        st.subheader("Valor de la inversión")
        st.line_chart(valor_inversion.rename("USD"))
    with derecha:
        st.subheader("Rendimiento diario de la cartera")
        st.bar_chart(cartera.mul(100).rename("%"))
    st.info("Interpretación: la escala base 100 permite comparar trayectorias aunque los activos tengan precios diferentes.")
with p2:
    st.subheader("Estadística descriptiva de rendimientos")
    resumen = pd.DataFrame({"Media diaria (%)":rendimientos.mean()*100,
                            "Mediana diaria (%)":rendimientos.median()*100,
                            "Desviación diaria (%)":rendimientos.std()*100,
                            "Mínimo diario (%)":rendimientos.min()*100,
                            "Máximo diario (%)":rendimientos.max()*100})
    st.dataframe(resumen.round(3), use_container_width=True)
    a, b = st.columns(2)
    with a:
        fig = px.histogram(x=cartera*100, nbins=30, title="Distribución de rendimientos diarios",
                           labels={"x":"Rendimiento (%)", "y":"Frecuencia"})
        st.plotly_chart(fig, use_container_width=True)
    with b:
        fig = px.imshow(rendimientos.corr(), text_auto=".2f", zmin=-1, zmax=1,
                        color_continuous_scale="RdBu_r", title="Correlaciones")
        st.plotly_chart(fig, use_container_width=True)
    st.info("Interpretación: una correlación alta no implica causalidad. La volatilidad mide dispersión de rendimientos.")
with p3:
    st.subheader("Cómo se construyó")
    st.write("**Layout:** sidebar, columns, tabs. **Widgets:** multiselect, selectbox, number_input.")
    st.write("**Datos:** yfinance, pandas. **Gráficos:** Streamlit y Plotly.")
    st.write("**Fórmulas:** rendimiento diario, rendimiento acumulado, desviación estándar anualizada.")

with st.expander("🔎 Ver datos y descargar CSV"):
    st.dataframe(precios.tail(30), use_container_width=True)
    st.download_button("Descargar precios CSV", precios.to_csv().encode("utf-8"), "precios_financelab.csv", "text/csv")
st.caption("Uso académico. Los resultados históricos no garantizan rentabilidades futuras.")
