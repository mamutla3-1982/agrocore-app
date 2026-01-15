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
    th { background-color: #2e7d32 !important; color: white !important; }
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

st.header(f"📅 Ciclo Anual Técnico: {variedad_sel}")
st.write(f"📍 {mun_sel} ({prov_sel}) | Régimen: {sistema_sel}")

# 3. MOTOR DE 12 MESES POR CULTIVO
if st.button("🚀 GENERAR CALENDARIO COMPLETO (ENE-DIC)"):
    mult = {"Secano Tradicional": 1, "Regadío Estándar": 1.5, "Intensivo": 2.2, "Superintensivo": 3.5}[sistema_sel]
    
    if grupo_sel == '🌿 Olivar e Higueras':
        plan = [
            ["Enero", "Poda de mantenimiento", 15*ha, "Jornal", 65],
            ["Febrero", "Retirada de restos poda", 1*ha, "Servicio", 80],
            ["Marzo", "Cobre Cupreder (Repilo)", 3*mult*ha, "kg", 9],
            ["Abril", "Herbicida de ruedos", 2*mult*ha, "L", 18],
            ["Mayo", "Dimetoato (Prays)", 1*mult*ha, "L", 18],
            ["Junio", "Abonado Nitrogenado", 200*mult*ha, "kg", 1],
            ["Julio", "Riego / Control Estrés", 1*ha, "ha", 50],
            ["Agosto", "Tratamiento Mosca (Cebo)", 0.5*mult*ha, "L", 45],
            ["Septiembre", "Preparación de suelos", 1*ha, "ha", 40],
            ["Octubre", "Cobre Pre-cosecha", 2*mult*ha, "kg", 9],
            ["Noviembre", "Recolección (Vibrador)", 40*ha, "L/Gasóleo", 1],
            ["Diciembre", "Transporte a Almazara", 1*ha, "Servicio", 120]
        ]
    elif grupo_sel == '🍎 Frutales':
        plan = [
            ["Enero", "Poda de invierno", 20*ha, "Jornal", 65],
            ["Febrero", "Aceite Parafina (Plagas)", 10*mult*ha, "L", 7],
            ["Marzo", "Captan 80 (Moteado)", 1.5*mult*ha, "kg", 14],
            ["Abril", "Abonado Foliar Floración", 2*mult*ha, "L", 12],
            ["Mayo", "Coragen (Carpocapsa)", 0.2*mult*ha, "L", 210],
            ["Junio", "Nitrato Calcio (Bitter Pit)", 5*mult*ha, "kg", 2],
            ["Julio", "Movento (Pulgón)", 1.5*mult*ha, "L", 55],
            ["Agosto", "Aclareo de fruta", 10*ha, "Jornal", 65],
            ["Septiembre", "Recolección Principal", 40*ha, "Jornal", 65],
            ["Octubre", "Limpieza de parcelas", 1*ha, "ha", 60],
            ["Noviembre", "Abono de Otoño", 300*mult*ha, "kg", 1],
            ["Diciembre", "Mantenimiento Maquinaria", 1*ha, "Servicio", 150]
        ]
    elif grupo_sel == '🍋 Cítricos':
        plan = [
            ["Enero", "Recolección Variedades", 30*ha, "Jornal", 65],
            ["Febrero", "Poda y aclareo", 20*ha, "Jornal", 65],
            ["Marzo", "Sivanto Prime (Piojo)", 0.8*mult*ha, "L", 75],
            ["Abril", "Quelatos Hierro (Clorosis)", 3*mult*ha, "kg", 18],
            ["Mayo", "Nitrato Potásico", 15*mult*ha, "kg", 3],
            ["Junio", "Abamectina (Ácaros)", 1.2*mult*ha, "L", 28],
            ["Julio", "Riego intensivo", 1*ha, "ha", 120],
            ["Agosto", "Poda en verde", 10*ha, "Jornal", 65],
            ["Septiembre", "Fungicida (Aguado)", 1.5*mult*ha, "L", 40],
            ["Octubre", "Control de Mosca", 0.5*mult*ha, "L", 45],
            ["Noviembre", "Abonado Fondo", 400*mult*ha, "kg", 1],
            ["Diciembre", "Mantenimiento Riego", 1*ha, "ha", 60]
        ]
    else:
        # Plan genérico de 12 meses para el resto
        plan = [[m, "Mantenimiento / Insumos", 10*mult, "Unid", 15] for m in ["Ene", "Feb", "Mar", "Abr", "May", "Jun", "Jul", "Ago", "Sep", "Oct", "Nov", "Dic"]]

    # Formatear tabla
    df = pd.DataFrame(plan, columns=["Mes", "Tarea / Producto", "Cantidad Total", "Unidad", "Precio Unit. (€)"])
    df["Subtotal (€)"] = df["Cantidad Total"] * df["Precio Unit. (€)"]
    
    st.table(df.style.format({
        "Cantidad Total": "{:.0f}",
        "Precio Unit. (€)": "{:.0f}",
        "Subtotal (€)": "{:,.0f}"
    }))

    # 4. BALANCE DE RENTABILIDAD
    inv_neta = df["Subtotal (€)"].sum() - ((ayuda_base + 65) * ha)
    rendimientos = {"🍎 Frutales": 25000, "🌿 Olivar e Higueras": 5500, "🌾 Cereales": 4800, "🍋 Cítricos": 32000, "🍷 Vid": 9000, "🧄 Aliáceas": 13000, "🥔 Tubérculos": 38000}
    prod_est = int(ha * rendimientos.get(grupo_sel, 5000) * (0.6 if "Secano" in sistema_sel else 1.0))
    ingresos = prod_est * precio_venta
    beneficio = ingresos - inv_neta

    st.divider()
    c1, c2, c3 = st.columns(3)
    c1.metric("📦 Cosecha Total", f"{prod_est:,.0f} kg")
    c2.metric("📉 Coste Anual Neto", f"{inv_neta:,.0f} €")
    c3.metric("💰 BENEFICIO ESTIMADO", f"{beneficio:,.0f} €")

    # BOTÓN WHATSAPP
    msg = f"Infor_AgroCore\nCultivo: {variedad_sel}\nBeneficio: {beneficio:,.0f}€\nPlan: 12 meses completo"
    url_wa = f"https://wa.me/?text={urllib.parse.quote(msg)}"
    st.markdown(f'''<a href="{url_wa}" target="_blank" style="text-decoration: none;"><div style="background-color: #25D366; color: white; padding: 15px; border-radius: 10px; text-align: center; font-weight: bold; font-size: 20px;">🟢 Enviar Ciclo por WhatsApp</div></a>''', unsafe_allow_html=True)
