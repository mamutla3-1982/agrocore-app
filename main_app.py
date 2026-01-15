import streamlit as st
import pandas as pd
import random
import urllib.parse

# Configuración visual de la App
st.set_page_config(page_title="AGROCORE 360", page_icon="🚜", layout="wide")

# Estilo para quitar ceros y mejorar la tabla
st.markdown("""
    <style>
    .main { background-color: #f5f7f9; }
    div.stButton > button:first-child { background-color: #25D366; color: white; width: 100%; border-radius: 10px; height: 3em; font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)

# 1. LISTAS DE DATOS
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

# 2. PANEL LATERAL (SIDEBAR)
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/2318/2318282.png", width=50)
    st.title("AGROCORE 360")
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

# 3. CABECERA DEL INFORME
st.header(f"Informe: {variedad_sel}")
st.write(f"📍 Ubicación: {mun_sel}, {prov_sel} | Sistema: {sistema_sel}")

prob_lluvia = random.randint(5, 40)
if prob_lluvia > 70:
    st.error(f"🌧️ ALERTA CRÍTICA ({prob_lluvia}% lluvia): No tratar hoy.")
else:
    st.success(f"☀️ CLIMA ÓPTIMO ({prob_lluvia}% lluvia): Proceder con el plan.")

# 4. MOTOR DE TRATAMIENTOS (SIN CEROS SOBRANTES)
if st.button("🚀 GENERAR INFORME COMPLETO"):
    mult = {"Secano Tradicional": 1, "Regadío Estándar": 1.5, "Intensivo": 2.2, "Superintensivo": 3.5}[sistema_sel]
    
    if grupo_sel == '🍎 Frutales':
        plan = [
            ["Marzo", "Captan 80 (Moteado)", int(1.5*mult*ha), "kg", 14],
            ["Mayo", "Coragen (Carpocapsa)", int(0.2*mult*ha), "L", 210],
            ["Junio", "Nitrato Calcio (Bitter Pit)", int(5*mult*ha), "kg", 2],
            ["Julio", "Movento (Pulgón)", int(1.5*mult*ha), "L", 55]
        ]
    elif grupo_sel == '🌿 Olivar e Higueras':
        plan = [
            ["Marzo", "Cobre Cupreder", int(3*mult*ha), "kg", 9],
            ["Abril", "Aminoácidos 24%", int(2*mult*ha), "L", 12],
            ["Mayo", "Dimetoato (Prays)", int(1*mult*ha), "L", 18],
            ["Sept", "Gasóleo Recolección", int(60*mult*ha), "L", 1]
        ]
    else:
        plan = [
            ["Ene", "YaraMila Complex", int(400*mult*ha), "kg", 1],
            ["Mar", "Roundup Ultra", int(3*mult*ha), "L", 18],
            ["Abr", "Score 25 EC", int(0.5*mult*ha), "L", 95]
        ]

    # Crear DataFrame y formatear números para que no tengan .0000
    df = pd.DataFrame(plan, columns=["Mes", "Producto", "Cant. Total", "Unid", "Precio/Unid"])
    df["Subtotal (€)"] = df["Cant. Total"] * df["Precio/Unid"]
    
    # Mostrar tabla limpia
    st.table(df.style.format({"Precio/Unid": "{:.0f}", "Subtotal (€)": "{:,.0f}"}))

    # 5. BALANCE FINAL
    inv_neta = df["Subtotal (€)"].sum() - ((ayuda_base + 65) * ha)
    prod_est = int(ha * 5000 * (1.1 if "Secano" in sistema_sel else 1.5))
    ingresos = prod_est * precio_venta
    beneficio = ingresos - inv_neta

    st.divider()
    c1, c2, c3 = st.columns(3)
    c1.metric("📦 Cosecha Est.", f"{prod_est:,.0f} kg")
    c2.metric("📉 Gasto Neto", f"{inv_neta:,.0f} €")
    c3.metric("💰 BENEFICIO", f"{beneficio:,.0f} €")

    # BOTÓN WHATSAPP (Estilo imagen)
    mensaje = f"Informe AgroCore 360\nCultivo: {variedad_sel}\nBeneficio: {beneficio:,.0f}€\nCosecha: {prod_est:,.0f}kg"
    url_wa = f"https://wa.me/?text={urllib.parse.quote(mensaje)}"
    
    st.markdown(f'''
        <a href="{url_wa}" target="_blank" style="text-decoration: none;">
            <div style="background-color: #25D366; color: white; padding: 15px; border-radius: 10px; text-align: center; font-weight: bold; font-size: 20px;">
                🟢 WhatsApp.App
            </div>
        </a>
    ''', unsafe_allow_html=True)

    if foto:
        st.image(foto, width=300)
