import streamlit as st
import json
import os
from datetime import datetime

# Налаштування сторінки
st.set_page_config(page_title="ЖКХ Калькулятор", page_icon="📝")

DB_FILE = "utility_db.json"

def load_data():
    if os.path.exists(DB_FILE):
        try:
            with open(DB_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except: return {"history": [], "last_input": {}}
    return {"history": [], "last_input": {}}

def save_data(history, last_input):
    with open(DB_FILE, "w", encoding="utf-8") as f:
        json.dump({"history": history, "last_input": last_input}, f, ensure_ascii=False, indent=4)

data = load_data()
history = data.get("history", [])
last_input = data.get("last_input", {})

st.title("📊 Мій Калькулятор")

tab1, tab2 = st.tabs(["🧮 Новий розрахунок", "📜 Архів"])

with tab1:
    with st.expander("⚙️ Налаштувати Тарифи"):
        t_el_d = st.number_input("Ціна кВт День", value=last_input.get("t_el_d", 4.32))
        t_el_n = st.number_input("Ціна кВт Ніч", value=last_input.get("t_el_n", 2.16))
        t_wat = st.number_input("Ціна м3 Вода", value=last_input.get("t_wat", 40.0))
        t_gas = st.number_input("Ціна м3 Газ", value=last_input.get("t_gas", 7.99))

    col1, col2 = st.columns(2)
    with col1:
        st.write("**Старі**")
        l_el_d = st.number_input("Електро Д (ст)", value=last_input.get("c_el_d", 0.0))
        l_el_n = st.number_input("Електро Н (ст)", value=last_input.get("c_el_n", 0.0))
        l_wat = st.number_input("Вода (ст)", value=last_input.get("c_wat", 0.0))
        l_gas = st.number_input("Газ (ст)", value=last_input.get("c_gas", 0.0))

    with col2:
        st.write("**Нові**")
        c_el_d = st.number_input("Електро Д (нов)", value=0.0)
        c_el_n = st.number_input("Електро Н (нов)", value=0.0)
        c_wat = st.number_input("Вода (нов)", value=0.0)
        c_gas = st.number_input("Газ (нов)", value=0.0)

    # Розрахунок в реальному часі
    res_el_d = (c_el_d - l_el_d) * t_el_d
    res_el_n = (c_el_n - l_el_n) * t_el_n
    res_wat = (c_wat - l_wat) * t_wat + 52 if (c_wat - l_wat) > 0 else 0
    res_gas = (c_gas - l_gas) * t_gas
    total = res_el_d + res_el_n + res_wat + res_gas

    st.divider()
    st.subheader("💰 Підсумок")
    
    # Детальний розпис
    st.write(f"💡 Електроенергія (день): **{res_el_d:.2f}** грн")
    st.write(f"🌙 Електроенергія (ніч): **{res_el_n:.2f}** грн")
    st.write(f"💧 Вода (+52 аб): **{res_wat:.2f}** грн")
    st.write(f"🔥 Газ: **{res_gas:.2f}** грн")
    st.markdown(f"### 💵 ЗАГАЛОМ: {total:.2f} грн")

    if st.button("📥 ЗБЕРЕГТИ В АРХІВ", use_container_width=True):
        current_save = {
            "t_el_d": t_el_d, "t_el_n": t_el_n, "t_wat": t_wat, "t_gas": t_gas,
            "c_el_d": c_el_d, "c_el_n": c_el_n, "c_wat": c_wat, "c_gas": c_gas
        }
        entry = {
            "date": datetime.now().strftime("%d.%m.%Y %H:%M"),
            "total": total,
            "details": {
                "Електро День": res_el_d,
                "Електро Ніч": res_el_n,
                "Вода": res_wat,
                "Газ": res_gas
            },
            "readings": {"Е-д": c_el_d, "Е-н": c_el_n, "В": c_wat, "Г": c_gas}
        }
        history.append(entry)
        save_data(history, current_save)
        st.success("Дані заархівовано!")
        st.rerun()

with tab2:
    st.subheader("📜 Історія розрахунків")
    if history:
        for item in reversed(history):
            with st.expander(f"📅 {item['date']} — {item['total']:.2f} грн"):
                st.write("**Розпис по послугах:**")
                for service, price in item['details'].items():
                    st.write(f"- {service}: {price:.2f} грн")
                st.write("**Зафіксовані показники:**")
                st.json(item['readings'])
                
        if st.button("🗑 Очистити історію"):
            save_data([], last_input)
            st.rerun()
    else:
        st.write("Архів порожній.")
