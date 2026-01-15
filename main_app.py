import streamlit as st
import pandas as pd
import random
from datetime import datetime
import urllib.parse

# Configuración de la App e Icono para el móvil
st.set_page_config(
    page_title="AGROCORE 360",
    page_icon="🚜",
    layout="wide"
)

# 1. TU LISTA DE CULTIVOS (SIN CAMBIOS)
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
    st.title("🚜 AGROCORE 360")
    prov_sel = st.selectbox("Provincia", sorted(provincias_espana))
    mun_sel = st.text_input("Municipio", placeholder="Ej: Martos...")
    st.divider()
    sistema_sel = st.selectbox("Sistema", ["Secano Tradicional", "Regadío Estándar", "Intensivo", "Superintensivo"])
    grupo_sel = st.selectbox("Grupo", list(cultivos_master.keys()))
    variedad_sel = st.selectbox("Variedad", cultivos_master[grupo_sel])
    ha = st.number_input("Hectáreas", min_value=0.1, value=10.0)
    st.divider()
    precio_venta = st.number_input("Precio Venta Est. (€/kg)", value=0.65)
    ayuda_base = st.number_input("Ayuda PAC (€/Ha)", value=125.0)
    st.divider()
    foto = st.camera_input("Capturar Evidencia")

# 3. LÓGICA DE CLIMA
prob_lluvia = random.randint(0, 100)
st.title(f"📊 Informe: {variedad_sel}")
if prob_lluvia > 70:
    st.error(f"🌧️ ALERTA DE LLUVIA ({prob_lluvia}%): No se recomiendan tratamientos hoy.")
else:
    st.success(f"☀️ CLIMA ÓPTIMO ({prob_lluvia}% lluvia): Proceder con el plan.")

# 4. MOTOR DE TRATAMIENTOS SEGÚN EL GRUPO SELECCIONADO
if st.button("🚀 GENERAR INFORME COMPLETO"):
    mult = {"Secano Tradicional": 1.0, "Regadío Estándar": 1.5, "Intensivo": 2.2, "Superintensivo": 3.5}[sistema_sel]
    
    # Seleccionamos el plan según el grupo de tu lista
    if grupo_sel == '🍎 Frutales':
        plan = [
            ["Marzo", "Floración", "Captan 80 (Moteado)", 1.5*mult, "kg", 14.00],
            ["Mayo", "Cuajado", "Coragen (Carpocapsa)", 0.2*mult, "L", 210.00],
            ["Junio", "Engorde", "Nitrato Calcio (Bitter Pit)", 5*mult, "kg", 2.20],
            ["Julio", "Vuelo", "Movento (Pulgón)", 1.5*mult, "L", 55.00]
        ]
    elif grupo_sel == '🧄 Aliáceas':
        plan = [
            ["Enero", "Siembra/Fondo", "Entec 26", 450*mult, "kg", 0.70],
            ["Marzo", "Herbicida", "Challenge (Pre-emergencia)", 2.5*mult, "L", 32.00],
            ["Abril", "Fungicida", "Folicur (Roya/Mildiu)", 1.0*mult, "L", 48.00],
            ["Mayo", "Insecticida", "Deltametrina (Trips)", 0.5*mult, "L", 22.00]
        ]
    elif grupo_sel == '🌿 Olivar e Higueras':
        plan = [
            ["Marzo", "Cobre", "Cupreder", 3.0*mult, "kg", 9.50],
            ["Abril", "Foliar", "Aminoácidos 24%", 2.0*mult, "L", 12.00],
            ["Mayo", "Prays", "Dimetoato", 1.0*mult, "L", 18.00],
            ["Nov", "Pre-cosecha", "Gasóleo Recolección", 60*mult, "L", 1.20]
        ]
    else:
        # Plan estándar para el resto de grupos
        plan = [
            ["Ene", "Fertilización", "YaraMila Complex", 400*mult, "kg", 0.85],
            ["Mar", "Herbicida", "Roundup Ultra", 3*mult, "L", 18.00],
            ["Abr", "Fungicida", "Score 25 EC", 0.5*mult, "L", 95.00],
            ["May", "Insecticida", "Karate Zeon", 0.15*mult, "L", 110.00]
        ]
    
    df_plan = pd.DataFrame(plan, columns=["Mes", "Tarea", "Producto", "Dosis/Ha", "Unid", "Precio/Unid"])
    df_plan["Total Finca"] = df_plan["Dosis/Ha"] * ha * df_plan["Precio/Unid"]
    
    st.header(f"🛒 Plan Técnico para {grupo_sel}")
    st.table(df_plan)

    # Balance Final (Mantenemos tu lógica de rentabilidad)
    inv_bruta = df_plan["Total Finca"].sum()
    subvencion = (ayuda_base + 65.0) * ha
    inv_neta = inv_bruta - subvencion
    prod_est = (ha * 5000) * (1.1 if "Secano" in sistema_sel else 1.5)
    ingresos = prod_est * precio_venta
    beneficio = ingresos - inv_neta

    col1, col2, col3 = st.columns(3)
    col1.metric("Cosecha Est.", f"{prod_est:,.0f} kg")
    col2.metric("Gasto Neto", f"{inv_neta:,.2f} €")
    col3.metric("BENEFICIO NETO", f"{beneficio:,.2f} €")

    # Botón WhatsApp
    mensaje = f"Informe AgroCore 360\nCultivo: {variedad_sel}\nBeneficio Est: {beneficio:,.2f}€\nCosecha: {prod_est:,.0f}kg"
    url_wa = f"https://wa.me/?text={urllib.parse.quote(mensaje)}"
    st.markdown(f'[@ Enviar Informe por WhatsApp]({url_wa})')

    if foto:
        st.image(foto, caption="Captura del cultivo")
