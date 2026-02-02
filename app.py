import streamlit as st

st.set_page_config(page_title="Калькулятор ЖКХ", page_icon="⚡")

st.title("⚡ Калькулятор Комуналки")

# Секція тарифів
with st.expander("⚙️ Налаштувати Тарифи", expanded=True):
    t_el_d = st.number_input("Ціна кВт День", value=4.32, format="%.2f")
    t_el_n = st.number_input("Ціна кВт Ніч", value=2.16, format="%.2f")
    t_wat = st.number_input("Ціна м3 Вода", value=40.0, format="%.2f")
    t_gas = st.number_input("Ціна м3 Газ", value=7.99, format="%.2f")

st.divider()

# Введення показників у дві колонки
col1, col2 = st.columns(2)

with col1:
    st.markdown("### 🔙 Старі")
    l_el_d = st.number_input("Електро День (ст)", value=0.0)
    l_el_n = st.number_input("Електро Ніч (ст)", value=0.0)
    l_wat = st.number_input("Вода (ст)", value=0.0)
    l_gas = st.number_input("Газ (ст)", value=0.0)

with col2:
    st.markdown("### 🆕 Нові")
    c_el_d = st.number_input("Електро День (нов)", value=0.0)
    c_el_n = st.number_input("Електро Ніч (нов)", value=0.0)
    c_wat = st.number_input("Вода (нов)", value=0.0)
    c_gas = st.number_input("Газ (нов)", value=0.0)

st.divider()

# Розрахунок
if st.button("🚀 РОЗРАХУВАТИ", use_container_width=True):
    res_el_d = (c_el_d - l_el_d) * t_el_d
    res_el_n = (c_el_n - l_el_n) * t_el_n
    res_wat = (c_wat - l_wat) * t_wat + 52
    res_gas = (c_gas - l_gas) * t_gas
    total = res_el_d + res_el_n + res_wat + res_gas
    
    # Вивід результатів
    st.balloons()
    st.success(f"### РАЗОМ: {total:.2f} грн")
    
    st.write(f"🔹 **Електро (День):** {res_el_d:.2f} грн")
    st.write(f"🔹 **Електро (Ніч):** {res_el_n:.2f} грн")
    st.write(f"🔹 **Вода (+52 аб):** {res_wat:.2f} грн")
    st.write(f"🔹 **Газ:** {res_gas:.2f} грн")
