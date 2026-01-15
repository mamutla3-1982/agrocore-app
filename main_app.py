import streamlit as st
import pandas as pd
import random
from datetime import datetime

st.set_page_config(page_title="AGROCORE 360 - Profesional", layout="wide")

# =============================================================================
# 1. BASES DE DATOS Y CONFIGURACIÓN
# =============================================================================
foto = None 

provincias_espana = [
    "Álava", "Albacete", "Alicante", "Almería", "Asturias", "Ávila", "Badajoz", "Baleares", "Barcelona", "Burgos", "Cáceres", "Cádiz", "Cantabria", "Castellón", "Ciudad Real", "Córdoba", "A Coruña", "Cuenca", "Gipuzkoa", "Girona", "Granada", "Guadalajara", "Huelva", "Huesca", "Jaén", "León", "Lleida", "Lugo", "Madrid", "Málaga", "Murcia", "Navarra", "Ourense", "Palencia", "Las Palmas", "Pontevedra", "La Rioja", "Salamanca", "Segovia", "Sevilla", "Soria", "Tarragona", "Santa Cruz de Tenerife", "Teruel", "Toledo", "Valencia", "Valladolid", "Bizkaia", "Zamora", "Zaragoza", "Ceuta", "Melilla"
]

cultivos_master = {
    '🧄 Aliáceas': ["Ajo", "Cebolla", "Puerro", "Escaluña", "Ajoporro"],
    '🌾 Cereales': ["Trigo", "Cebada", "Avena", "Centeno", "Maíz", "Arroz"],
    '🍋 Cítricos': ["Limón", "Naranjo", "Mandarino", "Lima", "Pomelo"],
    '🥔 Tubérculos': ["Patata", "Boniato", "Chufa", "Zanahoria"],
    '🍎 Frutales': ["Almendro", "Nogal", "Peral", "Manzano", "Cerezo", "Melocotonero"],
    '🌿 Olivar e Higueras': ["Olivo Picual", "Olivo Arbequina", "Higuera"],
    '🍷 Vid': ["Uva de mesa", "Uva vinificación"]
}

# =============================================================================
# 2. PANEL LATERAL
# =============================================================================
with st.sidebar:
    st.title("🚜 Panel AGROCORE 360")
    prov_sel = st.selectbox("Provincia", sorted(provincias_espana))
    mun_sel = st.text_input("Municipio", placeholder="Ej: Martos...")
    
    st.divider()
    st.header("⚙️ Configuración Técnica")
    sistema_sel = st.selectbox("Sistema", ["Secano Tradicional", "Regadío Estándar", "Intensivo", "Superintensivo"])
    grupo_sel = st.selectbox("Grupo (PDF)", list(cultivos_master.keys()))
    variedad_sel = st.selectbox("Variedad", cultivos_master[grupo_sel])
    
    ha = st.number_input("Hectáreas Totales", min_value=0.1, value=10.0)
    prod_ant = st.number_input("Producción Anterior (kg)", value=50000)
    
    st.divider()
    st.header("💰 Mercado y PAC")
    precio_venta = st.number_input("Precio Venta Est. (€/kg)", value=0.65)
    ayuda_base = st.number_input("Ayuda PAC (€/Ha)", value=125.0)
    eco_regimen = st.checkbox("Eco-regímenes", value=True)
    
    foto = st.camera_input("Capturar evidencia")

# =============================================================================
# 3. MOTOR DE PRODUCTOS COMERCIALES Y CLIMA
# =============================================================================
prob_lluvia = random.randint(0, 100)
viento = random.randint(5, 40)

def obtener_plan_comercial(sistema, ha):
    mult = {"Secano Tradicional": 1.0, "Regadío Estándar": 1.5, "Intensivo": 2.2, "Superintensivo": 3.5}
    m = mult[sistema]
    
    # [Mes, Operación, Nombre Comercial, Función, Dosis_Ha, Unidad, Precio_Unit]
    plan = [
        ["Ene/Feb", "Fertilización Fondo", "YaraMila Complex", "NPK Magnesio", 400 * m, "kg", 0.85],
        ["Marzo", "Herbicida", "Roundup UltraPlus", "Control Malas Hierbas", 3 * m, "L", 18.00],
        ["Abril", "Tratamiento Hongo", "Score 25 EC", "Fungicida Sistémico", 0.5 * m, "L", 95.00],
        ["Mayo", "Control Plagas", "Karate Zeon", "Insecticida Pulgón", 0.15 * m, "L", 110.00],
        ["Jun/Jul", "Nutrición Foliar", "Isabion", "Bioestimulante Aminoácidos", 3 * m, "L", 14.50]
    ]
    
    if sistema != "Secano Tradicional":
        plan.append(["Verano", "Riego", "Energía/Cánon", "Hidratación", 1500 * m, "m³", 0.22])
        
    return plan

# =============================================================================
# 4. CUERPO PRINCIPAL
# =============================================================================
st.title(f"📋 Informe Técnico Comercial: {variedad_sel}")
st.write(f"📍 {mun_sel}, {prov_sel} | Sistema: **{sistema_sel}**")

# Alertas de Lluvia
st.divider()
if prob_lluvia > 70:
    st.error(f"🌧️ **ALERTA: {prob_lluvia}% de lluvia.** No aplique **Score** o **Karate Zeon** hoy; se lavarán.")
elif prob_lluvia > 30:
    st.warning(f"🌦️ **AVISO: {prob_lluvia}% de lluvia.** Use mojantes si aplica productos de contacto.")
else:
    st.success(f"☀️ **ÓPTIMO: {prob_lluvia}% de lluvia.** Buen momento para el plan comercial.")

if st.button("🚀 GENERAR INFORME DE COMPRA Y RENTABILIDAD"):
    plan = obtener_plan_comercial(sistema_sel, ha)
    
    filas = []
    inv_bruta = 0
    
    for mes, op, comercial, funcion, dosis, unid, pu in plan:
        c_ha = pu * dosis
        c_tot = c_ha * ha
        inv_bruta += c_tot
        filas.append({
            "Mes": mes, "Operación": op, "Producto Comercial": comercial,
            "Función": funcion, "Dosis/Ha": f"{dosis:.2f} {unid}",
            "Coste/Ha": f"{c_ha:,.2f} €", "TOTAL": f"{c_tot:,.2f} €"
        })
    
    st.header("🛒 Calendario de Tratamientos y Suministros")
    st.table(pd.DataFrame(filas))

    # --- CÁLCULOS DE DINERO ---
    subvencion = (ayuda_base + (65.0 if eco_regimen else 0.0)) * ha
    inv_neta = inv_bruta - subvencion
    mejora = {"Secano Tradicional": 1.10, "Regadío Estándar": 1.25, "Intensivo": 1.50, "Superintensivo": 2.10}
    prod_est = prod_ant * mejora[sistema_sel]
    ingresos = prod_est * precio_venta
    ganancia = ingresos - inv_neta

    st.divider()
    st.header("🏁 Balance Económico Final")
    c1, c2, c3 = st.columns(3)
    with c1:
        st.write("### 📦 Cosecha Final")
        st.header(f"{prod_est:,.0f} kg")
    with c2:
        st.write("### 💵 Ingresos Venta")
        st.header(f"{ingresos:,.2f} €")
    with c3:
        st.write("### 📉 Gasto Neto (PAC incl.)")
        st.header(f"{inv_neta:,.2f} €")

    st.divider()
    col_final, col_roi = st.columns([2,1])
    with col_final:
        st.write("## 💰 GANANCIA LIMPIA ESTIMADA")
        st.title(f"{ganancia:,.2f} €")
    with col_roi:
        roi = (ganancia / inv_neta * 100) if inv_neta > 0 else 0
        st.metric("ROI (Rentabilidad)", f"{roi:.1f}%")

    if foto:
        st.image(foto, caption="Registro visual del cultivo", width=400)