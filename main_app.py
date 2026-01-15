import streamlit as st
import pandas as pd
import random
import urllib.parse

# Configuración visual de la App
st.set_page_config(page_title="AGROCORE 360", page_icon="🚜", layout="wide")

# Estilo para quitar ceros y mejorar la interfaz móvil
st.markdown("""
    <style>
    .main { background-color: #f5f7f9; }
    div.stButton > button:first-child { background-color: #25D366; color: white; width: 100%; border-radius: 10px; height: 3em; font-weight: bold; }
    [data-testid="stMetricValue"] { font-size: 1.8rem; }
    </style>
    """, unsafe_allow_html=True)

# 1. LISTAS DE DATOS (TU LISTA ORIGINAL)
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

# 3. CABECERA
st.header(f"Informe: {variedad_sel}")
st.write(f"📍 {mun_sel}, {prov_sel} | Sistema: {sistema_sel}")

prob_lluvia = random.randint(5, 40)
st.success(f"☀️ CLIMA ÓPTIMO ({prob_lluvia}% lluvia): Proceder con el plan.")

# 4. MOTOR DE TRATAMIENTOS PARA TODOS LOS GRUPOS
if st.button("🚀 GENERAR INFORME COMPLETO"):
    mult = {"Secano Tradicional": 1, "Regadío Estándar": 1.5, "Intensivo": 2.2, "Superintensivo": 3.5}[sistema_sel]
    
    if grupo_sel == '🍎 Frutales':
        plan = [
            ["Marzo", "Captan 80 (Moteado)", 1.5*mult*ha, "kg", 14],
            ["Mayo", "Coragen (Carpocapsa)", 0.2*mult*ha, "L", 210],
            ["Junio", "Nitrato Calcio (Bitter Pit)", 5*mult*ha, "kg", 2],
            ["Julio", "Movento (Pulgón)", 1.5*mult*ha, "L", 55]
        ]
    elif grupo_sel == '🌿 Olivar e Higueras':
        plan = [
            ["Marzo", "Cupreder (Cobre)", 3*mult*ha, "kg", 9],
            ["Abril", "Aminoácidos 24%", 2*mult*ha, "L", 12],
            ["Mayo", "Dimetoato (Prays)", 1*mult*ha, "L", 18],
            ["Sept", "Gasóleo Recolección", 60*mult*ha, "L", 1]
        ]
    elif grupo_sel == '🌾 Cereales':
        plan = [
            ["Ene", "Urea 46%", 250*mult*ha, "kg", 1],
            ["Feb", "Herbicida Atlantis Flex", 0.3*mult*ha, "kg", 115],
            ["Abr", "Fungicida Elatus Era", 0.8*mult*ha, "L", 85],
            ["Jun", "Cosechadora (Servicio)", 1*ha, "ha", 120]
        ]
    elif grupo_sel == '🍋 Cítricos':
        plan = [
            ["Mar", "Sivanto Prime (Piojo)", 0.8*mult*ha, "L", 75],
            ["May", "Nitrato Potásico", 10*mult*ha, "kg", 3],
            ["Jun", "Abamectina (Ácaros)", 1.2*mult*ha, "L", 28],
            ["Ago", "Quelato de Hierro", 5*mult*ha, "kg", 15]
        ]
    elif grupo_sel == '🍷 Vid':
        plan = [
            ["Abr", "Azufre Microlux", 5*mult*ha, "kg", 4],
            ["May", "Fungicida Luna Experience", 0.6*mult*ha, "L", 92],
            ["Jun", "Poda en verde (Mano obra)", 20*ha, "jornal", 65],
            ["Ago", "Botprocaet (Oídio)", 1*mult*ha, "L", 55]
        ]
    elif grupo_sel == '🧄 Aliáceas':
        plan = [
            ["Ene", "Entec 26 (Fondo)", 500*mult*ha, "kg", 1],
            ["Mar", "Challenge (Herbicida)", 2.5*mult*ha, "L", 35],
            ["Abr", "Signum (Mildiu)", 1.5*mult*ha, "kg", 62],
            ["Jun", "Arranque (Servicio)", 1*ha, "ha", 450]
        ]
    elif grupo_sel == '🥔 Tubérculos':
        plan = [
            ["Mar", "Reldan (Escarabajo)", 1.5*mult*ha, "L", 42],
            ["Abr", "Revus (Mildiu)", 0.6*mult*ha, "L", 88],
            ["May", "Potasa Líquida", 10*mult*ha, "L", 6],
            ["Jun", "Gasóleo Arranque", 80*mult*ha, "L", 1]
        ]

    # Crear tabla y redondear valores
    df = pd.DataFrame(plan, columns=["Mes", "Producto", "Cant. Total", "Unid", "Precio/Unid"])
    df["Subtotal (€)"] = df["Cant. Total"] * df["Precio/Unid"]
    
    # Formateo para quitar ceros (int)
    st.table(df.style.format({
        "Cant. Total": "{:.0f}",
        "Precio/Unid": "{:.0f}",
        "Subtotal (€)": "{:,.0f}"
    }))

    # 5. BALANCE FINAL
    inv_neta = df["Subtotal (€)"].sum() - ((ayuda_base + 65) * ha)
    rendimiento = {"🍎 Frutales": 25000, "🌿 Olivar e Higueras": 6000, "🌾 Cereales": 4500, "🍋 Cítricos": 30000, "🍷 Vid": 8000, "🧄 Aliáceas": 12000, "🥔 Tubérculos": 35000}
    prod_est = int(ha * rendimiento[grupo_sel] * (0.6 if "Secano" in sistema_sel else 1.0))
    ingresos = prod_est * precio_venta
    beneficio = ingresos - inv_neta

    st.divider()
    c1, c2, c3 = st.columns(3)
    c1.metric("📦 Cosecha Est.", f"{prod_est:,.0f} kg")
    c2.metric("📉 Gasto Neto", f"{inv_neta:,.0f} €")
    c3.metric("💰 BENEFICIO", f"{beneficio:,.0f} €")

    # BOTÓN WHATSAPP
    msg = f"Informe AGROCORE\nCultivo: {variedad_sel}\nBeneficio: {beneficio:,.0f}€\nCosecha: {prod_est:,.0f}kg"
    url_wa = f"https://wa.me/?text={urllib.parse.quote(msg)}"
    
    st.markdown(f'''
        <a href="{url_wa}" target="_blank" style="text-decoration: none;">
            <div style="background-color: #25D366; color: white; padding: 15px; border-radius: 10px; text-align: center; font-weight: bold; font-size: 20px; box-shadow: 2px 2px 5px rgba(0,0,0,0.2);">
                🟢 WhatsApp.App
            </div>
        </a>
    ''', unsafe_allow_html=True)

    if foto:
        st.image(foto, width=300)
