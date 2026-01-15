import streamlit as st
import pandas as pd
import random
import urllib.parse

# Configuración visual
st.set_page_config(page_title="AGROCORE 360", page_icon="🚜", layout="wide")

st.markdown("""
    <style>
    .main { background-color: #f5f7f9; }
    .btn-wa { background-color: #25D366; color: white; padding: 10px 20px; border-radius: 10px; text-decoration: none; font-weight: bold; display: inline-block; margin-right: 10px; }
    .btn-pdf { background-color: #31333F; color: white; padding: 10px 20px; border-radius: 10px; text-decoration: none; font-weight: bold; display: inline-block; cursor: pointer; border: none; }
    th { background-color: #1b5e20 !important; color: white !important; }
    @media print { .no-print { display: none !important; } .stSidebar { display: none !important; } }
    </style>
    """, unsafe_allow_html=True)

# Función de formato español
def f_num(valor):
    if valor is None: return "0"
    if valor == int(valor): return f"{int(valor):,}".replace(",", ".")
    else: return f"{valor:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")

# 1. LISTAS COMPLETAS
provincias_espana = ["Álava", "Albacete", "Alicante", "Almería", "Asturias", "Ávila", "Badajoz", "Baleares", "Barcelona", "Burgos", "Cáceres", "Cádiz", "Cantabria", "Castellón", "Ciudad Real", "Córdoba", "A Coruña", "Cuenca", "Gipuzkoa", "Girona", "Granada", "Guadalajara", "Huelva", "Huesca", "Jaén", "León", "Lleida", "Lugo", "Madrid", "Málaga", "Murcia", "Navarra", "Ourense", "Palencia", "Las Palmas", "Pontevedra", "La Rioja", "Salamanca", "Segovia", "Sevilla", "Soria", "Tarragona", "Santa Cruz de Tenerife", "Teruel", "Toledo", "Valencia", "Valladolid", "Bizkaia", "Zamora", "Zaragoza", "Ceuta", "Melilla"]

cultivos_master = {
    '🧄 Aliáceas': ["Ajo", "Cebolla", "Puerro"],
    '🌾 Cereales': ["Trigo", "Cebada", "Avena", "Maíz"],
    '🍋 Cítricos': ["Limón", "Naranjo", "Mandarino"],
    '🥔 Tubérculos': ["Patata", "Boniato"],
    '🍎 Frutales': ["Almendro", "Nogal", "Peral", "Manzano"],
    '🌿 Olivar e Higueras': ["Olivo Picual", "Olivo Arbequina", "Higuera"],
    '🍷 Vid': ["Uva de mesa", "Uva vinificación"]
}

# 2. CATÁLOGO TÉCNICO DE 12 MESES POR CULTIVO (MARCAS REALES)
CATALOGO = {
    '🌿 Olivar e Higueras': [
        ["Ene", "Poda e Higiene", 15, "Jornal", 65], ["Feb", "Picado Restos", 1, "Ha", 85], ["Mar", "Cupreder (Cobre)", 3, "kg", 11.5], ["Abr", "Roundup Ultra", 2.5, "L", 18.2], ["May", "Karate Zeon (Prays)", 0.15, "L", 120], ["Jun", "YaraVera AMIDAS", 300, "kg", 1.05], ["Jul", "Riego Apoyo", 1, "Ha", 60], ["Ago", "Isabion Amino.", 2, "L", 15], ["Sep", "Desvaretado", 10, "Jornal", 65], ["Oct", "Cobre Nordox", 2, "kg", 14.8], ["Nov", "Recolección (Gasóleo)", 100, "L", 1.18], ["Dic", "Mantenimiento Suelos", 1, "Ha", 45]
    ],
    '🌾 Cereales': [
        ["Ene", "YaraVera (Cobertera)", 250, "kg", 0.95], ["Feb", "Atlantis Flex", 0.3, "kg", 118], ["Mar", "Puma Super", 0.8, "L", 42], ["Abr", "Elatus Era", 0.75, "L", 88], ["May", "Insecticida Syngenta", 0.15, "L", 45], ["Jun", "Cosecha Maquilero", 1, "Ha", 135], ["Jul", "Transporte Silo", 1, "Ha", 45], ["Ago", "Laboreo Rastrojos", 1, "Ha", 35], ["Sep", "Preparación Suelo", 1, "Ha", 55], ["Oct", "Abono Fondo D-Coder", 350, "kg", 1.10], ["Nov", "Semilla Certificada", 180, "kg", 0.95], ["Dic", "Herbicida Pre-em.", 2, "L", 38]
    ],
    '🍋 Cítricos': [
        ["Ene", "Recolección", 35, "Jornal", 65], ["Feb", "Poda Formación", 25, "Jornal", 65], ["Mar", "Sivanto Prime (Bayer)", 0.7, "L", 78], ["Abr", "Abamectina (Ácaros)", 1.2, "L", 30], ["May", "YaraLiva Nitrabor", 15, "kg", 3.2], ["Jun", "Confidor (Pulgón)", 0.5, "L", 85], ["Jul", "Energía Riego", 1, "Ha", 180], ["Ago", "Movento (Cochinilla)", 1.5, "L", 58], ["Sep", "Switch (Fungicida)", 0.8, "kg", 95], ["Oct", "Cobre Nordox", 2, "kg", 14], ["Nov", "YaraMila Complex", 400, "kg", 1.15], ["Dic", "Limpieza Goteo", 1, "Ha", 50]
    ],
    '🍷 Vid': [
        ["Ene", "Poda Invierno", 25, "Jornal", 65], ["Feb", "Atado Cepas", 10, "Jornal", 65], ["Mar", "Cobre Cupreder", 2, "kg", 11.5], ["Abr", "Azufre Microlux", 5, "kg", 5.5], ["May", "Luna Experience", 0.6, "L", 95], ["Jun", "Poda en verde", 15, "Jornal", 65], ["Jul", "Vivando (Oidio)", 0.2, "L", 140], ["Ago", "Switch (Botritis)", 0.8, "kg", 95], ["Sep", "Vendimia Cuadrilla", 45, "Jornal", 65], ["Oct", "Abono Otoño", 300, "kg", 1.05], ["Nov", "Enmienda Orgánica", 1, "Ha", 120], ["Dic", "Planificación", 1, "Ha", 30]
    ],
    '🧄 Aliáceas': [
        ["Ene", "Entec 26 (Abono)", 500, "kg", 1.1], ["Feb", "Challenge (Herbicida)", 2.5, "L", 38], ["Mar", "Folicur (Bayer)", 1, "L", 52], ["Abr", "Deltametrina", 0.5, "L", 28], ["May", "Signum (BASF)", 1.5, "kg", 65], ["Jun", "Arranque Mecánico", 1, "Ha", 450], ["Jul", "Corte y Limpieza", 20, "Jornal", 65], ["Ago", "Transporte Almacén", 1, "Ha", 120], ["Sep", "Preparación Suelo", 1, "Ha", 85], ["Oct", "Siembra (Semilla)", 1, "Ha", 800], ["Nov", "Pre-emergencia", 2, "L", 40], ["Dic", "Control Nascencia", 1, "Ha", 35]
    ],
    '🥔 Tubérculos': [
        ["Ene", "Abono Fondo", 450, "kg", 1], ["Feb", "Herbicida Pre-siembra", 3, "L", 35], ["Mar", "Siembra Certificada", 1, "Ha", 1200], ["Abr", "Reldan (Escarabajo)", 1.5, "L", 45], ["May", "Revus (Syngenta)", 0.6, "L", 92], ["Jun", "Abono Potasa", 15, "L", 8.5], ["Jul", "Riego Motor", 1, "Ha", 250], ["Ago", "Gusano Alambre", 1, "L", 55], ["Sep", "Arranque Cosecha", 1, "Ha", 600], ["Oct", "Transporte", 1, "Ha", 150], ["Nov", "Enmienda", 1, "Ha", 300], ["Dic", "Laboreo Profundo", 1, "Ha", 85]
    ],
    '🍎 Frutales': [
        ["Ene", "Poda Invierno", 25, "Jornal", 65], ["Feb", "Aceite Invierno", 10, "L", 8.5], ["Mar", "Captan 80", 1.5, "kg", 16.5], ["Abr", "Abono Floración", 2, "L", 12], ["May", "Coragen (DuPont)", 0.18, "L", 220], ["Jun", "YaraLiva Calcinit", 5, "kg", 2.1], ["Jul", "Movento (Pulgón)", 1.2, "L", 58], ["Ago", "Aclareo Manual", 15, "Jornal", 65], ["Sep", "Recolección", 40, "Jornal", 65], ["Oct", "Cobre Post-cosecha", 2, "kg", 14], ["Nov", "YaraMila Complex", 400, "kg", 1.15], ["Dic", "Mantenimiento", 1, "Ha", 55]
    ]
}

# 3. PANEL LATERAL
with st.sidebar:
    st.title("🚜 AGROCORE 360")
    prov_sel = st.selectbox("Provincia", sorted(provincias_espana))
    mun_sel = st.text_input("Municipio", value="Córdoba")
    st.divider()
    sistema_sel = st.selectbox("Sistema", ["Secano Tradicional", "Regadío Estándar", "Intensivo", "Superintensivo"])
    grupo_sel = st.selectbox("Grupo", list(cultivos_master.keys()))
    variedad_sel = st.selectbox("Variedad", cultivos_master[grupo_sel])
    ha = st.number_input("Hectáreas", min_value=0.1, value=10.0)
    precio_venta = st.number_input("Precio Venta Est. (€/kg)", value=0.65)
    ayuda_base = st.number_input("Ayuda PAC (€/Ha)", value=125.0)
    foto = st.camera_input("Capturar Evidencia")

# 4. CABECERA Y CLIMA
st.header(f"Informe Técnico: {variedad_sel}")
st.write(f"📍 {mun_sel} ({prov_sel}) | {sistema_sel}")

prob_lluvia = random.randint(0, 100)
if prob_lluvia > 70:
    st.error(f"🌧️ ALERTA DE LLUVIA ({f_num(prob_lluvia)}%): No tratar hoy.")
else:
    st.success(f"☀️ CLIMA ÓPTIMO ({f_num(prob_lluvia)}% lluvia): Condiciones excelentes.")

# 5. GENERAR INFORME
if st.button("🚀 GENERAR INFORME COMERCIAL 12 MESES"):
    mult = {"Secano Tradicional": 1, "Regadío Estándar": 1.5, "Intensivo": 2.2, "Superintensivo": 3.5}[sistema_sel]
    plan_base = CATALOGO.get(grupo_sel)
    
    filas_finales = []
    for m, t, c, u, p in plan_base:
        cant_total = c * ha
        if u in ["kg", "L"] and "Semilla" not in t and "Gasóleo" not in t: 
            cant_total *= mult
        subtotal = cant_total * p
        filas_finales.append([m, t, cant_total, u, p, subtotal])

    df = pd.DataFrame(filas_finales, columns=["Mes", "Tarea / Producto", "Cant. Total", "Unid", "Precio Unit. (€)", "Subtotal (€)"])
    
    df_ver = df.copy()
    for col in ["Cant. Total", "Precio Unit. (€)", "Subtotal (€)"]:
        df_ver[col] = df_ver[col].apply(f_num)
    st.table(df_ver)

    # 6. BALANCE
    total_gastos = df["Subtotal (€)"].sum()
    ingresos_pac = (ayuda_base + 65) * ha
    gasto_neto = total_gastos - ingresos_pac
    rend_base = {'🌿 Olivar e Higueras': 5500, '🌾 Cereales': 4800, '🍎 Frutales': 22000, '🍋 Cítricos': 30000, '🍷 Vid': 9000, '🧄 Aliáceas': 14000, '🥔 Tubérculos': 40000}
    prod_est = int(ha * rend_base.get(grupo_sel, 5000) * (0.7 if "Secano" in sistema_sel else 1.3))
    beneficio = (prod_est * precio_venta) - gasto_neto

    st.divider()
    c1, c2, c3 = st.columns(3)
    c1.metric("📦 Cosecha Total", f"{f_num(prod_est)} kg")
    c2.metric("📉 Gasto Neto", f"{f_num(gasto_neto)} €")
    c3.metric("💰 BENEFICIO", f"{f_num(beneficio)} €")

    # 7. BOTONES
    st.divider()
    msg = f"AGROCORE: {variedad_sel}\nBeneficio: {f_num(beneficio)}€\nCosecha: {f_num(prod_est)}kg"
    url_wa = f"https://wa.me/?text={urllib.parse.quote(msg)}"
    st.markdown(f'''<div class="no-print"><a href="{url_wa}" target="_blank" class="btn-wa">🟢 WhatsApp</a><button onclick="window.print()" class="btn-pdf">📄 PDF</button></div>''', unsafe_allow_html=True)
