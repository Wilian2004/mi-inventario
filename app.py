import streamlit as st
import pandas as pd

st.set_page_config(page_title="Gestión de Inventario", layout="wide")

if 'catalogo' not in st.session_state:
    st.session_state.catalogo = {
        "Arroz": {"costo": 2, "precio_venta": 4, "vencimiento": "18122026", "stock": 20, "tipo": "kilos", "ventas": {"05-2026": 20}},
        "Leche": {"costo": 3, "precio_venta": 5, "vencimiento": "20062026", "stock": 10, "tipo": "litros", "ventas": {"06-2026": 10}}
    }

st.title("📦 Sistema de Gestión Profesional")

menu = st.sidebar.selectbox("Seleccione una opción", 
    ["Inventario", "Agregar Producto", "Actualizar Stock/Ventas", "Reporte Mensual", "Sugerencias"])


if menu == "Inventario":
    st.header("📋 Inventario Detallado")
    df = pd.DataFrame.from_dict(st.session_state.catalogo, orient='index')
    st.dataframe(df, use_container_width=True)

elif menu == "Agregar Producto":
    st.header("➕ Nuevo Producto")
    with st.form("form_nuevo"):
        nombre = st.text_input("Nombre").capitalize()
        venc = st.text_input("Vencimiento (ddmmaaaa)")
        costo = st.number_input("Costo", min_value=0)
        precio = st.number_input("Precio Venta", min_value=0)
        stock = st.number_input("Stock Inicial", min_value=0)
        tipo = st.selectbox("Tipo", ["kilos", "litros", "unidades"])
        enviado = st.form_submit_button("Guardar Producto")
        
        if enviado and nombre:
            st.session_state.catalogo[nombre] = {
                "costo": costo, "precio_venta": precio, "vencimiento": venc, 
                "stock": stock, "tipo": tipo, "ventas": {}
            }
            st.success(f"¡{nombre} agregado!")

elif menu == "Actualizar Stock/Ventas":
    st.header("🔄 Actualizar Datos")
    prod = st.selectbox("Producto", list(st.session_state.catalogo.keys()))
    modo = st.radio("¿Qué desea actualizar?", ["Stock", "Ventas"])
    
    if modo == "Stock":
        cambio = st.number_input("Cantidad a sumar (negativo para restar)", value=0)
        if st.button("Actualizar Stock"):
            st.session_state.catalogo[prod]['stock'] += cambio
            st.success("Stock actualizado")
    else:
        mes = st.text_input("Mes-Año (ej: 06-2026)")
        cant = st.number_input("Cantidad vendida", min_value=0)
        if st.button("Registrar Venta"):
            st.session_state.catalogo[prod]['ventas'][mes] = st.session_state.catalogo[prod]['ventas'].get(mes, 0) + cant
            st.success("Venta registrada")

elif menu == "Reporte Mensual":
    st.header("📊 Ganancias del Mes")
    mes_filtro = st.text_input("Ingrese Mes-Año (ej: 06-2026)")
    if mes_filtro:
        total_ganancia = 0
        datos_reporte = []
        for n, p in st.session_state.catalogo.items():
            ventas = p['ventas'].get(mes_filtro, 0)
            ganancia = ventas * (p['precio_venta'] - p['costo'])
            total_ganancia += ganancia
            datos_reporte.append({"Producto": n, "Ventas": ventas, "Ganancia": f"${ganancia}"})
        
        st.table(datos_reporte)
        st.metric("Ganancia Total del Mes", f"${total_ganancia}")

elif menu == "Sugerencias":
    st.header("💡 Sugerencia de Compras")
    ranking = sorted(st.session_state.catalogo.items(), 
                    key=lambda x: (x[1]['precio_venta'] - x[1]['costo']) * sum(x[1]['ventas'].values()), 
                    reverse=True)
    for n, p in ranking:
        st.write(f"**{n}** - Stock actual: {p['stock']} | Margen: ${p['precio_venta']-p['costo']}")




