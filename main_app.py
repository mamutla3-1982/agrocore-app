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

# 1. LISTAS DE DATOS ORIGINALES
provincias_espana = ["Álava", "Albacete", "Alicante", "Almería", "Asturias", "Ávila", "Badajoz", "Baleares", "Barcelona", "Burgos", "Cáceres", "Cádiz", "Cantabria", "Castellón", "Ciudad Real", "Córdoba", "A Coruña", "Cuenca", "Gipuzkoa", "Girona", "Granada", "Guadalajara", "Huelva", "Huesca", "Jaén", "León", "Lleida", "Lugo", "Madrid", "Málaga", "Murcia", "Navarra", "Ourense", "Palencia", "Las Palmas", "Pontevedra", "La Rioja", "Salamanca", "Segovia", "Sevilla", "Soria", "Tarragona", "Santa Cruz de Tenerife", "Teruel", "Toledo", "Valencia", "Valladolid", "Bizkaia", "Zamora", "Zaragoza", "Ceuta", "Melilla"]

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

# 3. CABECERA E INFORME DE CLIMA (REINSTALADO)
st.header(f"Informe Técnico: {variedad_sel}")
st.write(f"📍 {mun_sel}, {prov_sel} | {sistema_sel}")

# Lógica de Clima
prob_lluvia = random.randint(0, 100)
if prob_lluvia > 70:
    st.error(f"🌧️ ALERTA DE LLUVIA ({prob_lluvia}%): No se recomiendan tratamientos hoy por riesgo de lavado de producto.")
elif prob_lluvia > 30:
    st.warning(f"⛅ CLIMA INESTABLE ({prob_lluvia}% lluvia): Precaución en aplicaciones foliares.")
else:
    st.success(f"☀️ CLIMA ÓPTIMO ({prob_lluvia}% lluvia): Condiciones excelentes para trabajar el campo.")

# 4. MOTOR DE 12 MESES
if st.button("🚀 GENERAR PLAN COMERCIAL 12 MESES"):
    mult = {"Secano Tradicional": 1, "Regadío Estándar": 1.5, "Intensivo": 2.2, "Superintensivo": 3.5}[sistema_sel]
    
    # Planes detallados por grupo
    planes = {
        '🌿 Olivar e Higueras': [
            ["Enero", "Poda (Mano de Obra)", 15*ha, "Jornal", 65],
            ["Febrero", "Desvaretado / Limpieza", 10*ha, "Jornal", 65],
            ["Marzo", "Cupreder (Cobre 50%)", 3*mult*ha, "kg", 11],
            ["Abril", "Roundup Ultra (Herbicida)", 2.5*mult*ha, "L", 18],
            ["Mayo", "Karate Zeon (Prays)", 0.15*mult*ha, "L", 120],
            ["Junio", "YaraVera AMIDAS (Abono)", 200*mult*ha, "kg", 1],
            ["Julio", "Isabion (Aminoácidos)", 2*mult*ha, "L", 15],
            ["Agosto", "Riego de Apoyo", 1*ha, "ha", 60],
            ["Septiembre", "Cobre Nordox 75", 2*mult*ha, "kg", 14],
            ["Octubre", "Tratamiento Mosca (Cebo)", 0.5*mult*ha, "L", 45],
            ["Noviembre", "Gasóleo Recolección", 50*mult*ha, "L", 1],
            ["Diciembre", "Transporte Almazara", 1*ha, "ha", 150]
        ],
        '🍎 Frutales': [
            ["Enero", "Poda Invierno", 25*ha, "Jornal", 65],
            ["Febrero", "Promanar (Aceite Invierno)", 10*mult*ha, "L", 8],
            ["Marzo", "Captan 80 (Moteado)", 1.5*mult*ha, "kg", 16],
            ["Abril", "Bayleton (Fungicida)", 0.5*mult*ha, "L", 95],
            ["Mayo", "Coragen (Carpocapsa)", 0.18*mult*ha, "L", 220],
            ["Junio", "YaraLiva Calcinit", 5*mult*ha, "kg", 2],
            ["Julio", "Movento (Pulgón)", 1.2*mult*ha, "L", 58],
            ["Agosto", "Aclareo Manual", 15*ha, "Jornal", 65],
            ["Septiembre", "Recolección (Jornales)", 40*ha, "Jornal", 65],
            ["Octubre", "Limpieza y Desbroce", 1*ha, "ha", 70],
            ["Noviembre", "YaraMila Complex", 400*mult*ha, "kg", 1],
            ["Diciembre", "Mantenimiento Maquinaria", 1*ha, "ha", 120]
        ],
        '🌾 Cereales': [
            ["Octubre", "Preparación (Servicio)", 1*ha, "ha", 55],
            ["Noviembre", "Semilla R-1 Certificada", 180*ha, "kg", 1],
            ["Diciembre", "Abono Fondo (D-Coder)", 350*mult*ha, "kg", 1],
            ["Enero", "YaraVera (Cobertera)", 250*mult*ha, "kg", 1],
            ["Febrero", "Atlantis Flex (Herbicida)", 0.3*mult*ha, "kg", 118],
            ["Marzo", "Puma Super (Avena loca)", 0.8*mult*ha, "L", 42],
            ["Abril", "Elatus Era (Fungicida)", 0.75*mult*ha, "L", 88],
            ["Mayo", "Karate Zeon (Garrapatillo)", 0.15*mult*ha, "L", 120],
            ["Junio", "Cosecha (Maquilero)", 1*ha, "ha", 130],
            ["Julio", "Transporte a Silo", 1*ha, "ha", 45],
            ["Agosto", "Manejo de Rastrojos", 1*ha, "ha", 30],
            ["Septiembre", "Planificación Campaña", 0, "-", 0]
        ],
        '🍷 Vid': [
            ["Enero", "Poda Tirada", 25*ha, "Jornal", 65],
            ["Febrero", "Atado de Sépas", 10*ha, "Jornal", 65],
            ["Marzo", "Cobre Cupreder", 2*mult*ha, "kg", 11],
            ["Abril", "Azufre Microlux", 5*mult*ha, "kg", 5],
            ["Mayo", "Luna Experience (Mildiu)", 0.6*mult*ha, "L", 95],
            ["Junio", "Poda en verde", 15*ha, "Jornal", 65],
            ["Julio", "Vivando (Oídio)", 0.2*mult*ha, "L", 140],
            ["Agosto", "Switch (Botritis)", 0.8*mult*ha, "kg", 95],
            ["Septiembre", "Vendimia (Cuadrilla)", 45*ha, "Jornal", 65],
            ["Octubre", "Abono Otoño", 300*mult*ha, "kg", 1],
            ["Noviembre", "Limpieza Madera", 1*ha, "ha", 55],
            ["Diciembre", "Plan de Invierno", 0, "-", 0]
        ]
    }

    # SELECCIONAR PLAN
    plan_final = planes.get(grupo_sel, planes['🌿 Olivar e Higueras'])
    df = pd.DataFrame(plan_final, columns=["Mes", "Tarea / Producto Comercial", "Cant. Total", "Unid", "Precio Unit. (€)"])
    df["Subtotal (€)"] = df["Cant. Total"] * df["Precio Unit. (€)"]
    
    # TABLA SIN CEROS
    st.table(df.style.format({"Cant. Total": "{:.0f}", "Precio Unit. (€)": "{:.0f}", "Subtotal (€)": "{:,.0f}"}))

    # 5. BALANCE
    inv_neta = df["Subtotal (€)"].sum() - ((ayuda_base + 65) * ha)
    rendimientos = {"🍎 Frutales": 25000, "🌿 Olivar e Higueras": 5500, "🌾 Cereales": 4800, "🍋 Cítricos": 32000, "🍷 Vid": 9000, "🧄 Aliáceas": 13000, "🥔 Tubérculos": 38000}
    prod_est = int(ha * rendimientos.get(grupo_sel, 5000) * (0.6 if "Secano" in sistema_sel else 1.0))
    ingresos = prod_est * precio_venta
    beneficio = ingresos - inv_neta

    st.divider()
    c1, c2, c3 = st.columns(3)
    c1.metric("📦 Cosecha Total", f"{prod_est:,.0f} kg")
    c2.metric("📉 Gasto Anual", f"{inv_neta:,.0f} €")
    c3.metric("💰 BENEFICIO", f"{beneficio:,.0f} €")

    # BOTÓN WHATSAPP
    msg = f"INFORME AGROCORE\nCultivo: {variedad_sel}\nBeneficio: {beneficio:,.0f}€"
    url_wa = f"https://wa.me/?text={urllib.parse.quote(msg)}"
    st.markdown(f'''<a href="{url_wa}" target="_blank" style="text-decoration: none;"><div style="background-color: #25D366; color: white; padding: 15px; border-radius: 10px; text-align: center; font-weight: bold; font-size: 20px;">🟢 WhatsApp.App</div></a>''', unsafe_allow_html=True)
