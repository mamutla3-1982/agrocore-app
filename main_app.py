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

# 1. LISTAS COMPLETAS (RECUPERADAS)
provincias_espana = ["Álava", "Albacete", "Alicante", "Almería", "Asturias", "Ávila", "Badajoz", "Baleares", "Barcelona", "Burgos", "Cáceres", "Cádiz", "Cantabria", "Castellón", "Ciudad Real", "Córdoba", "A Coruña", "Cuenca", "Gipuzkoa", "Girona", "Granada", "Guadalajara", "Huelva", "Huesca", "Jaén", "León", "Lleida", "Lugo", "Madrid", "Málaga", "Murcia", "Navarra", "Ourense", "Palencia", "Las Palmas", "Pontevedra", "La Rioja", "Salamanca", "Segovia", "Sevilla", "Soria", "Tarragona", "Santa Cruz de Tenerife", "Teruel", "Toledo", "Valencia", "Valladolid", "Bizkaia", "Zamora", "Zaragoza", "Ceuta", "Melilla"]

cultivos_master = {
    '🧄 Aliáceas': ["Ajo", "Cebolla", "Puerro", "Escaluña"],
    '🌾 Cereales': ["Trigo", "Cebada", "Avena", "Centeno", "Maíz"],
    '🍋 Cítricos': ["Limón", "Naranjo", "Mandarino", "Lima"],
    '🥔 Tubérculos': ["Patata", "Boniato", "Chufa"],
    '🍎 Frutales': ["Almendro", "Nogal", "Peral", "Manzano", "Cerezo"],
    '🌿 Olivar e Higueras': ["Olivo Picual", "Olivo Arbequina", "Higuera"],
    '🍷 Vid': ["Uva de mesa", "Uva vinificación"]
}

# 2. PANEL LATERAL (RECUPERADO)
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

# 3. CABECERA Y CLIMA (RECUPERADO)
st.header(f"Informe Técnico: {variedad_sel}")
st.write(f"📍 {mun_sel} ({prov_sel}) | {sistema_sel}")

prob_lluvia = random.randint(0, 100)
if prob_lluvia > 70:
    st.error(f"🌧️ ALERTA DE LLUVIA ({f_num(prob_lluvia)}%): Riesgo de lavado. No aplicar químicos hoy.")
else:
    st.success(f"☀️ CLIMA ÓPTIMO ({f_num(prob_lluvia)}% lluvia): Buenas condiciones para el campo.")

# 4. CATÁLOGO TÉCNICO ESPECÍFICO
CATALOGO = {
    '🌿 Olivar e Higueras': [
        ["Ene", "Poda e Higiene", 15, "Jornal", 65], ["Mar", "Cupreder (Cobre)", 3, "kg", 11.5],
        ["May", "Karate Zeon (Prays)", 0.15, "L", 120], ["Jun", "YaraVera AMIDAS", 300, "kg", 1.05],
        ["Oct", "Cobre Nordox 75", 2, "kg", 14.8], ["Nov", "Recolección", 100, "L", 1.2]
    ],
    '🌾 Cereales': [
        ["Nov", "Semilla Certificada", 180, "kg", 0.95], ["Ene", "YaraVera Cobertera", 250, "kg", 1],
        ["Feb", "Atlantis Flex", 0.3, "kg", 118], ["Abr", "Elatus Era", 0.75, "L", 88],
        ["Jun", "Cosecha Maquilero", 1, "Ha", 135], ["Ago", "Laboreo", 1, "Ha", 45]
    ]
    # Se pueden añadir los demás grupos aquí con la misma estructura
}

# 5. GENERAR PLAN 12 MESES
if st.button("🚀 GENERAR INFORME COMPLETO"):
    mult = {"Secano Tradicional": 1, "Regadío Estándar": 1.5, "Intensivo": 2.2, "Superintensivo": 3.5}[sistema_sel]
    
    # Lógica de relleno de 12 meses (Para que siempre salgan 12 filas)
    meses = ["Ene", "Feb", "Mar", "Abr", "May", "Jun", "Jul", "Ago", "Sep", "Oct", "Nov", "Dic"]
    plan_base = CATALOGO.get(grupo_sel, CATALOGO['🌿 Olivar e Higueras'])
    
    filas_finales = []
    for m_nombre in meses:
        # Buscar si el mes tiene tarea técnica, si no, poner mantenimiento
        tarea = next((x for x in plan_base if x[0] == m_nombre), [m_nombre, "Mantenimiento General", 1, "Ha", 35])
        
        cant_calc = tarea[2] * ha
        if tarea[3] in ["kg", "L"]: cant_calc *= mult # Aplicar multiplicador si es químico
        
        subtotal = cant_calc * tarea[4]
        filas_finales.append([m_nombre, tarea[1], cant_calc, tarea[3], tarea[4], subtotal])

    df = pd.DataFrame(filas_finales, columns=["Mes", "Tarea", "Cant. Total", "Unid", "Precio Unit. (€)", "Subtotal (€)"])
    
    # Mostrar tabla con formato
    df_ver = df.copy()
    for col in ["Cant. Total", "Precio Unit. (€)", "Subtotal (€)"]:
        df_ver[col] = df_ver[col].apply(f_num)
    st.table(df_ver)

    # 6. BALANCE ECONÓMICO (RECUPERADO)
    total_gastos = df["Subtotal (€)"].sum()
    ingresos_pac = (ayuda_base + 65) * ha
    gasto_neto = total_gastos - ingresos_pac
    
    rendimientos = {'🌿 Olivar e Higueras': 5500, '🌾 Cereales': 4800, '🍎 Frutales': 22000, '🍋 Cítricos': 30000}
    prod_est = int(ha * rendimientos.get(grupo_sel, 5000) * (0.7 if "Secano" in sistema_sel else 1.3))
    beneficio = (prod_est * precio_venta) - gasto_neto

    st.divider()
    c1, c2, c3 = st.columns(3)
    c1.metric("📦 Cosecha Total", f"{f_num(prod_est)} kg")
    c2.metric("📉 Gasto Neto Anual", f"{f_num(gasto_neto)} €")
    c3.metric("💰 BENEFICIO ESTIMADO", f"{f_num(beneficio)} €")

    # 7. BOTONES (RECUPERADOS Y MEJORADOS)
    st.divider()
    msg = f"INFORME AGROCORE: {variedad_sel}\nBeneficio: {f_num(beneficio)}€\nCosecha: {f_num(prod_est)}kg"
    url_wa = f"https://wa.me/?text={urllib.parse.quote(msg)}"
    
    st.markdown(f'''
        <div class="no-print">
            <a href="{url_wa}" target="_blank" class="btn-wa">🟢 Enviar WhatsApp</a>
            <button onclick="window.print()" class="btn-pdf">📄 Imprimir PDF</button>
        </div>
    ''', unsafe_allow_html=True)
