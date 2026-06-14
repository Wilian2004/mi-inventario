import streamlit as st
import pandas as pd

# Inicializar catálogo si no existe
if 'catalogo' not in st.session_state:
    st.session_state.catalogo = {
        "Arroz": {"costo": 2, "precio_venta": 4, "vencimiento": "18122026", "stock": 20, "tipo": "kilos", "ventas": {"05-2026": 20}},
        "Leche": {"costo": 3, "precio_venta": 5, "vencimiento": "20062026", "stock": 10, "tipo": "litros", "ventas": {"06-2026": 10}}
    }

st.sidebar.title("MENÚ")
opcion = st.sidebar.radio("Selecciona una opción:", [
    "1. Inventario", "2. Ordenar Ventas (Desc)", "3. Ordenar Ventas (Asc)", 
    "4. Agregar Producto", "5. Actualizar Stock/Ventas", "6. Reporte Mensual", 
    "7. Sugerir compras", "8. Reporte Producto/Mes", "9. Salir"
])

# --- LÓGICA ---

if opcion == "1. Inventario":
    st.header("Inventario Detallado")
    df = pd.DataFrame.from_dict(st.session_state.catalogo, orient='index')
    st.table(df)

elif opcion == "2. Ordenar Ventas (Desc)":
    st.header("Ordenado por Ventas (Desc)")
    lista = sorted(st.session_state.catalogo.items(), key=lambda x: sum(x[1]['ventas'].values()), reverse=True)
    for n, p in lista:
        st.write(f"{n} | Total ventas: {sum(p['ventas'].values())}")

elif opcion == "3. Ordenar Ventas (Asc)":
    st.header("Ordenado por Ventas (Asc)")
    lista = sorted(st.session_state.catalogo.items(), key=lambda x: sum(x[1]['ventas'].values()))
    for n, p in lista:
        st.write(f"{n} | Total ventas: {sum(p['ventas'].values())}")

elif opcion == "4. Agregar Producto":
    with st.form("agregar"):
        n = st.text_input("Nombre").capitalize()
        v = st.text_input("Vencimiento (ddmmaaaa)")
        c = st.number_input("Costo", 0)
        p = st.number_input("Precio", 0)
        s = st.number_input("Stock", 0)
        t = st.text_input("Tipo")
        if st.form_submit_button("Guardar"):
            st.session_state.catalogo[n] = {"costo": c, "precio_venta": p, "vencimiento": v, "stock": s, "tipo": t, "ventas": {}}
            st.success("Producto agregado")

elif opcion == "5. Actualizar Stock/Ventas":
    prod = st.selectbox("Producto", list(st.session_state.catalogo.keys()))
    sub = st.radio("Acción", ["1. Stock", "2. Ventas"])
    if sub == "1. Stock":
        c = st.number_input("Cambio")
        if st.button("Actualizar"): st.session_state.catalogo[prod]['stock'] += c
    else:
        m = st.text_input("Mes-Año (ej: 06-2026)")
        cant = st.number_input("Cantidad")
        if st.button("Registrar"): st.session_state.catalogo[prod]['ventas'][m] = st.session_state.catalogo[prod]['ventas'].get(m, 0) + cant

elif opcion == "6. Reporte Mensual":
    m = st.text_input("Mes-Año")
    if m:
        for n, p in st.session_state.catalogo.items():
            v = p['ventas'].get(m, 0)
            g = v * (p['precio_venta'] - p['costo'])
            st.write(f"{n}: {v} ventas | Ganancia: ${g}")

elif opcion == "7. Sugerir compras":
    ranking = sorted(st.session_state.catalogo.items(), key=lambda x: (x[1]['precio_venta'] - x[1]['costo']) * sum(x[1]['ventas'].values()), reverse=True)
    st.table(pd.DataFrame([(n, p['stock'], p['precio_venta']-p['costo']) for n, p in ranking], columns=["Producto", "Stock", "Margen"]))

elif opcion == "8. Reporte Producto/Mes":
    n = st.selectbox("Producto", list(st.session_state.catalogo.keys()))
    m = st.text_input("Mes-Año")
    if st.button("Consultar"):
        v = st.session_state.catalogo[n]['ventas'].get(m, 0)
        st.write(f"Ventas: {v}")

elif opcion == "9. Salir":
    st.write("Cierra esta pestaña para salir.")


