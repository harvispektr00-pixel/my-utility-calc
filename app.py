import streamlit as st
import json
import os
from datetime import datetime

# Настройка страницы для мобильных устройств
st.set_page_config(page_title="ЖКХ Калькулятор", page_icon="📊")

# Путь к файлу "базы данных" на сервере
DB_FILE = "data_storage.json"

def load_data():
    if os.path.exists(DB_FILE):
        with open(DB_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return {"history": [], "last_input": {}}

def save_data(history, last_input):
    with open(DB_FILE, "w", encoding="utf-8") as f:
        json.dump({"history": history, "last_input": last_input}, f, ensure_ascii=False, indent=4)

# Загружаем данные из файла
data = load_data()
history = data.get("history", [])
last_input = data.get("last_input", {})

st.title("📊 Мой Калькулятор")

# Создаем вкладки
tab1, tab2 = st.tabs(["🧮 Расчет", "📜 История"])

with tab1:
    st.subheader("Настройки и ввод")
    
    with st.expander("⚙️ Тарифы (сохраняются)"):
        t_el_d = st.number_input("Тариф электро День", value=last_input.get("t_el_d", 4.32), format="%.2f")
        t_el_n = st.number_input("Тариф электро Ночь", value=last_input.get("t_el_n", 2.16), format="%.2f")
        t_wat = st.number_input("Тариф Вода", value=last_input.get("t_wat", 40.0), format="%.2f")
        t_gas = st.number_input("Тариф Газ", value=last_input.get("t_gas", 7.99), format="%.2f")

    st.divider()

    col1, col2 = st.columns(2)
    
    with col1:
        st.write("**Старые**")
        # АВТОМАТИЧЕСКИЙ ПЕРЕНОС: берем "новые" из прошлого сохранения и ставим в "старые"
        l_el_d = st.number_input("Электро Д (ст)", value=last_input.get("c_el_d", 0.0))
        l_el_n = st.number_input("Электро Н (ст)", value=last_input.get("c_el_n", 0.0))
        l_wat = st.number_input("Вода (ст)", value=last_input.get("c_wat", 0.0))
        l_gas = st.number_input("Газ (ст)", value=last_input.get("c_gas", 0.0))

    with col2:
        st.write("**Новые**")
        c_el_d = st.number_input("Электро Д (нов)", value=0.0)
        c_el_n = st.number_input("Электро Н (нов)", value=0.0)
        c_wat = st.number_input("Вода (нов)", value=0.0)
        c_gas = st.number_input("Газ (нов)", value=0.0)

    if st.button("🚀 РАССЧИТАТЬ И ЗАПОМНИТЬ", use_container_width=True):
        # Логика расчета
        res_el_d = (c_el_d - l_el_d) * t_el_d
        res_el_n = (c_el_n - l_el_n) * t_el_n
        res_wat = (c_wat - l_wat) * t_wat + 52
        res_gas = (c_gas - l_gas) * t_gas
        total = res_el_d + res_el_n + res_wat + res_gas
        
        st.success(f"### ИТОГО: {total:.2f} грн")
        
        # Готовим данные для сохранения
        current_save = {
            "t_el_d": t_el_d, "t_el_n": t_el_n, "t_wat": t_wat, "t_gas": t_gas,
            "c_el_d": c_el_d, "c_el_n": c_el_n, "c_wat": c_wat, "c_gas": c_gas
        }
        
        # Добавляем в историю
        new_history_entry = {
            "Дата": datetime.now().strftime("%d.%m.%Y %H:%M"),
            "Сумма": f"{total:.2f} грн",
            "Детали": f"Свет: {res_el_d+res_el_n:.1f}, Вода: {res_wat:.1f}, Газ: {res_gas:.1f}"
        }
        history.append(new_history_entry)
        
        # Сохраняем в файл
        save_data(history, current_save)
        st.info("Данные сохранены! При следующем входе новые станут старыми.")

with tab2:
    st.subheader("📜 Архив ваших расчетов")
    if history:
        # Показываем последние 10 записей в обратном порядке
        for item in reversed(history[-10:]):
            st.write(f"📅 **{item['Дата']}** — {item['Сумма']}")
            st.caption(item['Детали'])
            st.divider()
    else:
        st.write("История пока пуста.")
