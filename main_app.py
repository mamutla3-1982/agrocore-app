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

# --- FUNCIONES DE FORMATO ESPAÑOL ---
def f_num(valor):
    """Formatea miles con punto y decimales con coma solo si existen"""
    if valor is None: return ""
    # Si es entero, solo puntos en miles
    if valor == int(valor):
        return f"{int(valor):,}".replace(",", ".")
    # Si tiene decimales, puntos en miles y coma en decimal
    else:
        return f"{valor:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")

# 1. LISTAS DE DATOS ORIGINALES
provincias_espana = ["Álava", "Albacete", "Alicante", "Almería", "Asturias", "Ávila", "Badajoz", "Baleares", "Barcelona", "Burgos", "Cáceres", "Cádiz", "Cantabria", "Castellón", "Ciudad Real", "Córdoba", "A Coruña", "Cuenca", "Gipuzkoa", "Girona", "Granada", "Guadalajara", "Huelva", "Huesca", "Jaén", "León", "Lleida", "Lugo", "Madrid", "Málaga", "Murcia", "Navarra", "Ourense", "Palencia", "Las Palmas", "Pontevedra", "La Rio_ja", "Salamanca", "Segovia", "Sevilla", "Soria", "Tarragona", "Santa Cruz de Tenerife", "Teruel", "Toledo", "Valencia", "Valladolid", "Bizkaia", "Zamora", "Zaragoza", "Ceuta", "Melilla"]

cultivos_master = {
    '🧄 Aliáceas': ["Ajo", "Cebolla", "Puerro", "Escaluña", "Ajoporro"],
    '🌾 Cereales': ["Trigo", "Cebada", "Avena", "Centeno", "Maíz", "Arroz"],
    '🍋 Cítricos': ["Limón", "Naranjo", "Mandarino", "Lima", "Pomelo"],
    '🥔 Tubérculos': ["Patata", "Boniato", "Chufa", "Zanahoria"],
    '🍎 Frutales': ["Almendro", "Nogal", "Peral", "Manzano", "Cerezo", "Melocotonero"],
    '🌿 Olivar e Higueras': ["Olivo Picual", "Olivo Arbequina", "Higuera"],
    '🍷 Vid': ["Uva de mesa", "Uva vinificación"]
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
    foto = st.camera_input("Capturar Evidencia")

# 3. CABECERA
st.header(f"Informe Técnico: {variedad_sel}")
st.write(f"📍 {mun_sel}, {prov_sel} | {sistema_sel}")

# Alerta de Clima
prob_lluvia = random.randint(0, 100)
if prob_lluvia > 70:
    st.error(f"🌧️ ALERTA DE LLUVIA ({f_num(prob_lluvia)}%): No tratar hoy.")
else:
    st.success(f"☀️ CLIMA ÓPTIMO ({f_num(prob_lluvia)}% lluvia): Proceder.")

# 4. MOTOR DE 12 MESES
if st.button("🚀 GENERAR PLAN COMERCIAL 12 MESES"):
    mult = {"Secano Tradicional": 1, "Regadío Estándar": 1.5, "Intensivo": 2.2, "Superintensivo": 3.5}[sistema_sel]
    
    # Planes detallados (Ejemplo ampliado)
    planes = {
        '🌿 Olivar e Higueras': [
            ["Enero", "Poda (Mano de Obra)", 15*ha, "Jornal", 65],
            ["Marzo", "Cupreder (Cobre 50%)", 3*mult*ha, "kg", 11.50],
            ["Mayo", "Karate Zeon (Prays)", 0.15*mult*ha, "L", 120],
            ["Junio", "YaraVera AMIDAS (Abono)", 200*mult*ha, "kg", 1],
            ["Septiembre", "Cobre Nordox 75", 2*mult*ha, "kg", 14.80],
            ["Noviembre", "Gasóleo Recolección", 100*mult*ha, "L", 1.15]
        ],
        '🍎 Frutales': [
            ["Enero", "Poda Invierno", 25*ha, "Jornal", 65],
            ["Marzo", "Captan 80 (Moteado)", 1.5*mult*ha, "kg", 16.50],
            ["Mayo", "Coragen (Carpocapsa)", 0.18*mult*ha, "L", 220],
            ["Septiembre", "Recolección (Jornales)", 40*ha, "Jornal", 65]
        ]
    }

    plan_data = planes.get(grupo_sel, planes['🌿 Olivar e Higueras'])
    df = pd.DataFrame(plan_data, columns=["Mes", "Tarea / Producto", "Cant. Total", "Unid", "Precio Unit."])
    df["Subtotal (€)"] = df["Cant. Total"] * df["Precio Unit."]
    
    # Aplicar formato visual a la tabla
    df_ver = df.copy()
    df_ver["Cant. Total"] = df_ver["Cant. Total"].apply(f_num)
    df_ver["Precio Unit."] = df_ver["Precio Unit."].apply(f_num)
    df_ver["Subtotal (€)"] = df_ver["Subtotal (€)"].apply(f_num)
    
    st.table(df_ver)

    # 5. BALANCE FINAL
    inv_neta = df["Subtotal (€)"].sum() - ((ayuda_base + 65) * ha)
    rendimientos = {"🍎 Frutales": 25000, "🌿 Olivar e Higueras": 5500, "🌾 Cereales": 4800, "🍋 Cítricos": 32000, "🍷 Vid": 9000}
    prod_est = int(ha * rendimientos.get(grupo_sel, 5000) * (0.6 if "Secano" in sistema_sel else 1.0))
    ingresos = prod_est * precio_venta
    beneficio = ingresos - inv_neta

    st.divider()
    c1, c2, c3 = st.columns(3)
    c1.metric("📦 Cosecha Total", f"{f_num(prod_est)} kg")
    c2.metric("📉 Gasto Anual", f"{f_num(inv_neta)} €")
    c3.metric("💰 BENEFICIO", f"{f_num(beneficio)} €")

    # BOTÓN WHATSAPP
    msg = f"AGROCORE: {variedad_sel}\nBeneficio: {f_num(beneficio)}€\nCosecha: {f_num(prod_est)}kg"
    url_wa = f"https://wa.me/?text={urllib.parse.quote(msg)}"
    st.markdown(f'''<a href="{url_wa}" target="_blank" style="text-decoration: none;"><div style="background-color: #25D366; color: white; padding: 15px; border-radius: 10px; text-align: center; font-weight: bold; font-size: 20px;">🟢 WhatsApp.App</div></a>''', unsafe_allow_html=True)
