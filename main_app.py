import streamlit as st
import pandas as pd
import random
import urllib.parse

# Configuración visual
st.set_page_config(page_title="AGROCORE 360", page_icon="🚜", layout="wide")

st.markdown("""
    <style>
    .main { background-color: #f5f7f9; }
    .btn-wa { background-color: #25D366; color: white; padding: 8px 16px; border-radius: 8px; text-decoration: none; font-weight: bold; display: inline-block; margin-right: 10px; }
    .btn-pdf { background-color: #31333F; color: white; padding: 8px 16px; border-radius: 8px; text-decoration: none; font-weight: bold; display: inline-block; cursor: pointer; border: none; }
    th { background-color: #1b5e20 !important; color: white !important; }
    @media print { .no-print { display: none !important; } .stSidebar { display: none !important; } }
    </style>
    """, unsafe_allow_html=True)

def f_num(valor):
    if valor is None: return ""
    if valor == int(valor): return f"{int(valor):,}".replace(",", ".")
    else: return f"{valor:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")

# 1. BASE DE DATOS TÉCNICA (12 MESES X CULTIVO)
# Aquí es donde ocurre la magia: cada cultivo tiene su propio "libro" de 12 meses.
CATALOGO_TECNICO = {
    '🌿 Olivar e Higueras': [
        ["Ene", "Poda y aclareo", 15, "Jornal", 65], ["Feb", "Picado de madera", 1, "Ha", 80],
        ["Mar", "Cupreder (Cobre)", 3, "kg", 11.5], ["Abr", "Roundup Ultra (Herbicida)", 2.5, "L", 18],
        ["May", "Karate Zeon (Prays)", 0.15, "L", 120], ["Jun", "YaraVera AMIDAS", 300, "kg", 1],
        ["Jul", "Isabion (Aminoácidos)", 2, "L", 15], ["Ago", "Riego de apoyo", 1, "Ha", 55],
        ["Sep", "Desvaretado manual", 10, "Jornal", 65], ["Oct", "Cobre Nordox 75", 2, "kg", 14.8],
        ["Nov", "Gasóleo Recolección", 100, "L", 1.15], ["Dic", "Mantenimiento suelos", 1, "Ha", 40]
    ],
    '🌾 Cereales': [
        ["Ene", "YaraVera (Cobertera)", 250, "kg", 0.95], ["Feb", "Atlantis Flex (Herbicida)", 0.3, "kg", 118],
        ["Mar", "Puma Super (Avena loca)", 0.8, "L", 42], ["Abr", "Elatus Era (Fungicida)", 0.75, "L", 88],
        ["May", "Karate Zeon (Garrapatillo)", 0.15, "L", 120], ["Jun", "Cosecha (Maquilero)", 1, "Ha", 135],
        ["Jul", "Transporte a Silo", 1, "Ha", 45], ["Ago", "Manejo rastrojos", 1, "Ha", 30],
        ["Sep", "Preparación terreno", 1, "Ha", 55], ["Oct", "Abono Fondo D-Coder", 350, "kg", 1.10],
        ["Nov", "Semilla Certificada R1", 180, "kg", 0.90], ["Dic", "Herbicida Pre-emergencia", 2, "L", 35]
    ],
    '🍋 Cítricos': [
        ["Ene", "Recolección temprana", 35, "Jornal", 65], ["Feb", "Poda de formación", 20, "Jornal", 65],
        ["Mar", "Sivanto Prime (Piojo)", 0.7, "L", 78], ["Abr", "Quelatos Hierro (Clorosis)", 3, "kg", 18],
        ["May", "YaraLiva Nitrabor", 15, "kg", 3], ["Jun", "Abamectina (Ácaros)", 1.2, "L", 30],
        ["Jul", "Energía Riego", 1, "Ha", 180], ["Ago", "Movento (Cochinilla)", 1.5, "L", 58],
        ["Sep", "Switch (Fungicida)", 0.8, "kg", 95], ["Oct", "Cobre Nordox", 2, "kg", 14],
        ["Nov", "Abono Completo YaraMila", 400, "kg", 1.1], ["Dic", "Revisión goteo", 1, "Ha", 45]
    ],
    '🍷 Vid': [
        ["Ene", "Poda en seco", 25, "Jornal", 65], ["Feb", "Atado de sarmientos", 10, "Jornal", 65],
        ["Mar", "Tratamiento Cobre", 2, "kg", 11.5], ["Abr", "Azufre Microlux (Oidio)", 5, "kg", 5],
        ["May", "Luna Experience (Mildiu)", 0.6, "L", 95], ["Jun", "Poda en verde", 15, "Jornal", 65],
        ["Jul", "Vivando (Oidio)", 0.2, "L", 140], ["Ago", "Switch (Botritis)", 0.8, "kg", 95],
        ["Sep", "Vendimia manual", 45, "Jornal", 65], ["Oct", "Abono de otoño", 300, "kg", 1],
        ["Nov", "Enmienda orgánica", 1, "Ha", 120], ["Dic", "Análisis de sarmiento", 1, "Ha", 40]
    ]
}

# 2. PANEL LATERAL
with st.sidebar:
    st.title("🚜 AGROCORE 360")
    grupo_sel = st.selectbox("Grupo", list(CATALOGO_TECNICO.keys()))
    variedad_sel = st.text_input("Variedad", value="Estándar")
    ha = st.number_input("Hectáreas", min_value=0.1, value=10.0)
    sistema_sel = st.selectbox("Sistema", ["Secano Tradicional", "Regadío Estándar", "Intensivo", "Superintensivo"])
    precio_venta = st.number_input("Precio Venta Est. (€/kg)", value=0.65)
    ayuda_base = st.number_input("Ayuda PAC (€/Ha)", value=125.0)

# 3. GENERACIÓN DEL INFORME
st.header(f"Informe Anual: {grupo_sel} ({variedad_sel})")
st.write(f"Configuración para {ha} Hectáreas en sistema {sistema_sel}")

if st.button("🚀 GENERAR PLAN TÉCNICO COMPLETO"):
    mult = {"Secano Tradicional": 1, "Regadío Estándar": 1.5, "Intensivo": 2.2, "Superintensivo": 3.5}[sistema_sel]
    
    # Obtener el plan específico del catálogo
    plan_base = CATALOGO_TECNICO[grupo_sel]
    
    # Calcular cantidades reales para la finca
    filas_finales = []
    for mes, prod, cant, unid, precio in plan_base:
        cant_total = cant * ha if unid in ["Jornal", "kg", "L"] else cant * ha
        # Si es un producto químico (kg/L), le aplicamos el multiplicador de sistema
        if unid in ["kg", "L"] and "Gasóleo" not in prod and "Semilla" not in prod:
            cant_total = cant_total * mult
            
        subtotal = cant_total * precio
        filas_finales.append([mes, prod, cant_total, unid, precio, subtotal])

    df = pd.DataFrame(filas_finales, columns=["Mes", "Tarea / Producto", "Cant. Total", "Unid", "Precio Unit. (€)", "Subtotal (€)"])
    
    # Tabla con formato español
    df_ver = df.copy()
    for col in ["Cant. Total", "Precio Unit. (€)", "Subtotal (€)"]:
        df_ver[col] = df_ver[col].apply(f_num)
    
    st.table(df_ver)

    # Balance Final
    total_gastos = df["Subtotal (€)"].sum()
    ingresos_pac = (ayuda_base + 65) * ha
    gasto_neto = total_gastos - ingresos_pac
    
    st.divider()
    c1, c2 = st.columns(2)
    c1.metric("📉 Gasto Anual Neto", f"{f_num(gasto_neto)} €")
    c2.metric("💰 Coste por Hectárea", f"{f_num(gasto_neto/ha)} €/Ha")

    # Botones
    st.markdown(f'''
        <div class="no-print">
            <a href="https://wa.me/?text=Informe+Agrocore+{grupo_sel}" target="_blank" class="btn-wa">🟢 WhatsApp</a>
            <button onclick="window.print()" class="btn-pdf">📄 Imprimir PDF</button>
        </div>
    ''', unsafe_allow_html=True)
