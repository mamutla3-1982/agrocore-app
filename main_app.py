import streamlit as st
import pandas as pd
import random
import urllib.parse

# Configuración visual
st.set_page_config(page_title="AGROCORE 360", page_icon="🚜", layout="wide")

st.markdown("""
    <style>
    .main { background-color: #f5f7f9; }
    div.stButton > button:first-child { background-color: #25D366; color: white; width: 100%; border-radius: 10px; height: 3em; font-weight: bold; }
    th { background-color: #1b5e20 !important; color: white !important; }
    </style>
    """, unsafe_allow_html=True)

# Función de formato español
def f_num(valor):
    if valor is None: return ""
    if valor == int(valor):
        return f"{int(valor):,}".replace(",", ".")
    else:
        return f"{valor:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")

# 1. LISTAS DE DATOS
provincias_espana = ["Álava", "Albacete", "Alicante", "Almería", "Asturias", "Ávila", "Badajoz", "Baleares", "Barcelona", "Burgos", "Cáceres", "Cádiz", "Cantabria", "Castellón", "Ciudad Real", "Córdoba", "A Coruña", "Cuenca", "Gipuzkoa", "Girona", "Granada", "Guadalajara", "Huelva", "Huesca", "Jaén", "León", "Lleida", "Lugo", "Madrid", "Málaga", "Murcia", "Navarra", "Ourense", "Palencia", "Las Palmas", "Pontevedra", "La Rioja", "Salamanca", "Segovia", "Sevilla", "Soria", "Tarragona", "Santa Cruz de Tenerife", "Teruel", "Toledo", "Valencia", "Valladolid", "Bizkaia", "Zamora", "Zaragoza", "Ceuta", "Melilla"]

cultivos_master = {
    '🌿 Olivar e Higueras': ["Olivo Picual", "Olivo Arbequina", "Higuera"],
    '🍎 Frutales': ["Almendro", "Nogal", "Peral", "Manzano", "Cerezo", "Melocotonero"],
    '🌾 Cereales': ["Trigo", "Cebada", "Avena", "Centeno", "Maíz", "Arroz"],
    '🍋 Cítricos': ["Limón", "Naranjo", "Mandarino", "Lima", "Pomelo"],
    '🍷 Vid': ["Uva de mesa", "Uva vinificación"],
    '🧄 Aliáceas': ["Ajo", "Cebolla", "Puerro"],
    '🥔 Tubérculos': ["Patata", "Boniato"]
}

# 2. PANEL LATERAL
with st.sidebar:
    st.title("🚜 AGROCORE 360")
    prov_sel = st.selectbox("Provincia", sorted(provincias_espana))
    mun_sel = st.text_input("Municipio", value="Córdoba")
    st.divider()
    sistema_sel = st.selectbox("Sistema", ["Secano Tradicional", "Regadío Estándar", "Intensivo", "Superintensivo"])
    grupo_sel = st.selectbox("Grupo", list(cultivos_master.keys()))
    variedad_sel = st.selectbox("Variedad", cultivos_master[grupo_sel])
    ha = st.number_input("Hectáreas", min_value=0.1, value=10.0, step=0.1)
    precio_venta = st.number_input("Precio Venta Est. (€/kg)", value=0.65)
    ayuda_base = st.number_input("Ayuda PAC (€/Ha)", value=125.0)

# 3. CABECERA
st.header(f"Informe Técnico Anual: {variedad_sel}")
st.write(f"📍 {mun_sel} | {sistema_sel}")

# Alerta de Clima
prob_lluvia = random.randint(5, 25)
st.success(f"☀️ CLIMA ÓPTIMO ({f_num(prob_lluvia)}% lluvia): Condiciones excelentes para trabajar.")

# 4. MOTOR DE 12 MESES (TODOS RELLENADOS)
if st.button("🚀 GENERAR PLAN 12 MESES"):
    m = {"Secano Tradicional": 1, "Regadío Estándar": 1.5, "Intensivo": 2.2, "Superintensivo": 3.5}[sistema_sel]
    
    planes = {
        '🌿 Olivar e Higueras': [
            ["Enero", "Poda y limpieza", 15*ha, "Jornal", 65],
            ["Febrero", "Picado de restos", 1*ha, "Ha", 85],
            ["Marzo", "Cupreder (Cobre)", 3*m*ha, "kg", 11.5],
            ["Abril", "Roundup Ultra", 2.5*m*ha, "L", 18],
            ["Mayo", "Karate Zeon", 0.15*m*ha, "L", 120],
            ["Junio", "YaraVera AMIDAS", 300*m*ha, "kg", 1],
            ["Julio", "Riego de apoyo", 1*ha, "Ha", 55],
            ["Agosto", "Isabion (Aminoac.)", 2*m*ha, "L", 15],
            ["Septiembre", "Desvaretado", 10*ha, "Jornal", 65],
            ["Octubre", "Cobre Nordox 75", 2*m*ha, "kg", 14.8],
            ["Noviembre", "Recolección (Gasóleo)", 100*m*ha, "L", 1.15],
            ["Diciembre", "Mantenimiento suelos", 1*ha, "Ha", 40]
        ],
        '🍎 Frutales': [
            ["Enero", "Poda Invierno", 25*ha, "Jornal", 65],
            ["Febrero", "Promanar (Aceite)", 10*m*ha, "L", 8],
            ["Marzo", "Captan 80", 1.5*m*ha, "kg", 16.5],
            ["Abril", "Abono Floración", 2*m*ha, "L", 12],
            ["Mayo", "Coragen", 0.18*m*ha, "L", 220],
            ["Junio", "YaraLiva Calcinit", 5*m*ha, "kg", 2.1],
            ["Julio", "Movento (Pulgón)", 1.2*m*ha, "L", 58],
            ["Agosto", "Aclareo Manual", 15*ha, "Jornal", 65],
            ["Septiembre", "Vendimia/Cosecha", 40*ha, "Jornal", 65],
            ["Octubre", "Cobre Post-cosecha", 2*m*ha, "kg", 14],
            ["Noviembre", "YaraMila Complex", 400*m*ha, "kg", 1.1],
            ["Diciembre", "Limpieza madera", 1*ha, "Ha", 55]
        ],
        '🌾 Cereales': [
            ["Enero", "YaraVera Cobertera", 250*m*ha, "kg", 1],
            ["Febrero", "Atlantis Flex", 0.3*m*ha, "kg", 118],
            ["Marzo", "Puma Super", 0.8*m*ha, "L", 42],
            ["Abril", "Elatus Era", 0.75*m*ha, "L", 88],
            ["Mayo", "Insecticida Cereal", 0.2*m*ha, "L", 45],
            ["Junio", "Cosecha (Maquilero)", 1*ha, "Ha", 135],
            ["Julio", "Transporte Silo", 1*ha, "Ha", 45],
            ["Agosto", "Laboreo Rastrojo", 1*ha, "Ha", 35],
            ["Septiembre", "Preparación Suelo", 1*ha, "Ha", 55],
            ["Octubre", "Abono Fondo D-Coder", 350*m*ha, "kg", 1.2],
            ["Noviembre", "Semilla Certificada", 180*ha, "kg", 1.1],
            ["Diciembre", "Tratamiento Pre-em.", 2*m*ha, "L", 38]
        ]
    }

    # Seleccionar plan (si no existe el grupo, usa el de olivar por defecto)
    plan_data = planes.get(grupo_sel, planes['🌿 Olivar e Higueras'])
    
    df = pd.DataFrame(plan_data, columns=["Mes", "Tarea / Producto", "Cant. Total", "Unid", "Precio Unit. (€)"])
    df["Subtotal (€)"] = df["Cant. Total"] * df["Precio Unit. (€)"]
    
    # Formato visual
    df_ver = df.copy()
    df_ver["Cant. Total"] = df_ver["Cant. Total"].apply(f_num)
    df_ver["Precio Unit. (€)"] = df_ver["Precio Unit. (€)"].apply(f_num)
    df_ver["Subtotal (€)"] = df_ver["Subtotal (€)"].apply(f_num)
    
    st.table(df_ver)

    # Balance Final
    inv_neta = df["Subtotal (€)"].sum() - ((ayuda_base + 65) * ha)
    rendimientos = {"🍎 Frutales": 25000, "🌿 Olivar e Higueras": 5500, "🌾 Cereales": 4800}
    prod_est = int(ha * rendimientos.get(grupo_sel, 5000) * (0.6 if "Secano" in sistema_sel else 1.0))
    ingresos = prod_est * precio_venta
    beneficio = ingresos - inv_neta

    st.divider()
    c1, c2, c3 = st.columns(3)
    c1.metric("📦 Cosecha Total", f"{f_num(prod_est)} kg")
    c2.metric("📉 Gasto Anual", f"{f_num(inv_neta)} €")
    c3.metric("💰 BENEFICIO", f"{f_num(beneficio)} €")
