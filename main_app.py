import streamlit as st
import pandas as pd
import random
import urllib.parse

# Configuración visual
st.set_page_config(page_title="AGROCORE 360", page_icon="🚜", layout="wide")

st.markdown("""
    <style>
    .main { background-color: #f5f7f9; }
    /* Botón WhatsApp Pequeño */
    .btn-wa { background-color: #25D366; color: white; padding: 8px 16px; border-radius: 8px; text-decoration: none; font-weight: bold; display: inline-block; margin-right: 10px; }
    /* Botón Imprimir */
    .btn-pdf { background-color: #31333F; color: white; padding: 8px 16px; border-radius: 8px; text-decoration: none; font-weight: bold; display: inline-block; cursor: pointer; border: none; }
    th { background-color: #1b5e20 !important; color: white !important; }
    @media print { .no-print { display: none !important; } }
    </style>
    """, unsafe_allow_html=True)

# Función de formato español
def f_num(valor):
    if valor is None: return ""
    if valor == int(valor):
        return f"{int(valor):,}".replace(",", ".")
    else:
        return f"{valor:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")

# 1. DATOS DE CULTIVOS
cultivos_master = {
    '🌿 Olivar e Higueras': ["Olivo Picual", "Olivo Arbequina", "Higuera"],
    '🍎 Frutales': ["Almendro", "Nogal", "Peral", "Manzano", "Cerezo", "Melocotonero"],
    '🌾 Cereales': ["Trigo", "Cebada", "Avena", "Centeno", "Maíz", "Arroz"],
    '🍋 Cítricos': ["Limón", "Naranjo", "Mandarino", "Lima", "Pomelo"],
    '🍷 Vid': ["Uva de mesa", "Uva vinificación"],
    '🧄 Aliáceas': ["Ajo", "Cebolla", "Puerro"],
    '🥔 Tubérculos': ["Patata", "Boniato"]
}

# 2. PANEL LATERAL (Se oculta al imprimir)
with st.sidebar:
    st.title("🚜 AGROCORE 360")
    prov_sel = st.selectbox("Provincia", ["Córdoba", "Sevilla", "Jaén", "Málaga", "Huelva", "Granada", "Almería", "Cádiz"])
    mun_sel = st.text_input("Municipio", value="Córdoba")
    st.divider()
    sistema_sel = st.selectbox("Sistema", ["Secano Tradicional", "Regadío Estándar", "Intensivo", "Superintensivo"])
    grupo_sel = st.selectbox("Grupo", list(cultivos_master.keys()))
    variedad_sel = st.selectbox("Variedad", cultivos_master[grupo_sel])
    ha = st.number_input("Hectáreas", min_value=0.1, value=10.0, step=0.1)
    precio_venta = st.number_input("Precio Venta Est. (€/kg)", value=0.65)
    ayuda_base = st.number_input("Ayuda PAC (€/Ha)", value=125.0)

# 3. CUERPO DEL INFORME
st.header(f"Informe Técnico: {variedad_sel}")
st.write(f"📍 {mun_sel} | {sistema_sel} | {ha} Ha")

# 4. GENERACIÓN DE PLAN (12 MESES)
mult = {"Secano Tradicional": 1, "Regadío Estándar": 1.5, "Intensivo": 2.2, "Superintensivo": 3.5}[sistema_sel]

# Plan ejemplo Olivar (puedes replicar para otros)
plan_data = [
    ["Enero", "Poda Invierno", 15*ha, "Jornal", 65],
    ["Febrero", "Picado Restos", 1*ha, "Ha", 85],
    ["Marzo", "Cupreder (Cobre)", 3*mult*ha, "kg", 11.5],
    ["Abril", "Roundup Ultra", 2.5*mult*ha, "L", 18.2],
    ["Mayo", "Karate Zeon", 0.15*mult*ha, "L", 120],
    ["Junio", "YaraVera AMIDAS", 300*mult*ha, "kg", 1.05],
    ["Julio", "Riego Apoyo", 1*ha, "Ha", 60],
    ["Agosto", "Isabion Amino.", 2*mult*ha, "L", 15],
    ["Septiembre", "Desvaretado", 10*ha, "Jornal", 65],
    ["Octubre", "Cobre Nordox", 2*mult*ha, "kg", 14.8],
    ["Noviembre", "Recolección", 100*mult*ha, "L", 1.18],
    ["Diciembre", "Laboreo", 1*ha, "Ha", 45]
]

df = pd.DataFrame(plan_data, columns=["Mes", "Tarea / Producto", "Cant. Total", "Unid", "Precio Unit. (€)"])
df["Subtotal (€)"] = df["Cant. Total"] * df["Precio Unit. (€)"]

# Tabla visual
df_ver = df.copy()
df_ver["Cant. Total"] = df_ver["Cant. Total"].apply(f_num)
df_ver["Precio Unit. (€)"] = df_ver["Precio Unit. (€)"].apply(f_num)
df_ver["Subtotal (€)"] = df_ver["Subtotal (€)"].apply(f_num)
st.table(df_ver)

# Balance
inv_neta = df["Subtotal (€)"].sum() - ((ayuda_base + 65) * ha)
prod_est = int(ha * 5500 * (0.6 if "Secano" in sistema_sel else 1.0))
beneficio = (prod_est * precio_venta) - inv_neta

st.divider()
c1, c2, c3 = st.columns(3)
c1.metric("📦 Cosecha", f"{f_num(prod_est)} kg")
c2.metric("📉 Gasto", f"{f_num(inv_neta)} €")
c3.metric("💰 BENEFICIO", f"{f_num(beneficio)} €")

# 5. BOTONES DE ACCIÓN (WhatsApp pequeño e Imprimir PDF)
st.divider()
msg = f"INFORME AGROCORE\nCultivo: {variedad_sel}\nBeneficio: {f_num(beneficio)}€\nCosecha: {f_num(prod_est)}kg"
url_wa = f"https://wa.me/?text={urllib.parse.quote(msg)}"

# Contenedor de botones
col_btns = st.container()
with col_btns:
    st.markdown(f'''
        <div class="no-print">
            <a href="{url_wa}" target="_blank" class="btn-wa">🟢 WhatsApp</a>
            <button onclick="window.print()" class="btn-pdf">📄 Imprimir PDF</button>
        </div>
    ''', unsafe_allow_html=True)
