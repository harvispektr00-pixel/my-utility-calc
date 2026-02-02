import tkinter as tk
from tkinter import messagebox
import json
import os
from datetime import datetime

# Файл базы данных
HISTORY_FILE = "utility_history.json"


def load_history():
    if os.path.exists(HISTORY_FILE):
        try:
            with open(HISTORY_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
                return data if isinstance(data, dict) else {}
        except:
            return {}
    return {}


def save_to_history(new_record):
    history = load_history()
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    history[timestamp] = new_record
    with open(HISTORY_FILE, "w", encoding="utf-8") as f:
        json.dump(history, f, ensure_ascii=False, indent=4)


def calculate():
    try:
        # Собираем данные. Если поле пустое — будет 0.0
        data = {}
        for k in entries:
            val = entries[k].get().replace(',', '.')  # замена запятой на точку для надежности
            data[k] = float(val) if val else 0.0

        res_el_d = (data["c_el_d"] - data["l_el_d"]) * data["t_el_d"]
        res_el_n = (data["c_el_n"] - data["l_el_n"]) * data["t_el_n"]
        res_wat = (data["c_wat"] - data["l_wat"]) * data["t_wat"] + 52
        res_gas = (data["c_gas"] - data["l_gas"]) * data["t_gas"]
        total = res_el_d + res_el_n + res_wat + res_gas

        res_text = (f"Электро (День): {res_el_d:.2f} грн\n"
                    f"Электро (Ночь): {res_el_n:.2f} грн\n"
                    f"Вода (+52 аб): {res_wat:.2f} грн\n"
                    f"Газ: {res_gas:.2f} грн\n"
                    f"---------------------------\nИТОГО: {total:.2f} грн")

        label_result.config(text=res_text, fg="blue")
        save_to_history(data)
        messagebox.showinfo("Готово", "Данные сохранены в файл!")

    except ValueError:
        messagebox.showerror("Ошибка", "Введите только числа")


def fill_fields(data, mode="last_to_old"):
    """Заполнение полей. mode 'last_to_old' делает Новые показания Старыми для следующего раза"""
    for k in entries:
        entries[k].delete(0, tk.END)

    if mode == "last_to_old":
        mapping = {
            "t_el_d": data.get("t_el_d", 0), "t_el_n": data.get("t_el_n", 0),
            "t_wat": data.get("t_wat", 0), "t_gas": data.get("t_gas", 0),
            "l_el_d": data.get("c_el_d", 0), "l_el_n": data.get("c_el_n", 0),
            "l_wat": data.get("c_wat", 0), "l_gas": data.get("c_gas", 0),
            "c_el_d": 0, "c_el_n": 0, "c_wat": 0, "c_gas": 0
        }
    else:  # Просто загрузка как есть
        mapping = data

    for k, v in mapping.items():
        if k in entries:
            entries[k].insert(0, str(v))


def show_history():
    history = load_history()
    if not history:
        messagebox.showinfo("Архив", "История пуста")
        return

    hist_win = tk.Toplevel(root)
    hist_win.title("Архив")
    hist_win.geometry("350x450")

    lb = tk.Listbox(hist_win)
    lb.pack(expand=True, fill="both", padx=10, pady=5)

    dates = sorted(history.keys(), reverse=True)
    for date in dates: lb.insert(tk.END, date)

    def load_selected():
        if not lb.curselection(): return
        date = lb.get(lb.curselection())
        fill_fields(history[date], mode="last_to_old")
        hist_win.destroy()

    tk.Button(hist_win, text="Загрузить выбранное", command=load_selected, bg="blue", fg="white").pack(pady=10)


# Навигация
def focus_next(e): e.widget.tk_focusNext().focus(); return "break"


def focus_prev(e): e.widget.tk_focusPrev().focus(); return "break"


# Интерфейс
root = tk.Tk()
root.title("ЖКХ Калькулятор")
root.geometry("420x700")

entries = {}
fields = [
    ("t_el_d", "Тариф электро День:"), ("t_el_n", "Тариф электро Ночь:"),
    ("t_wat", "Тариф Вода:"), ("t_gas", "Тариф Газ:"),
    ("l_el_d", "Электро день (Старые):"), ("c_el_d", "Электро день (Новые):"),
    ("l_el_n", "Электро ночь (Старые):"), ("c_el_n", "Электро ночь (Новые):"),
    ("l_wat", "Вода (Старые):"), ("c_wat", "Вода (Новые):"),
    ("l_gas", "Газ (Старые):"), ("c_gas", "Газ (Новые):")
]

for key, text in fields:
    f = tk.Frame(root);
    f.pack(fill="x", padx=20, pady=2)
    tk.Label(f, text=text, width=22, anchor="w").pack(side="left")
    e = tk.Entry(f);
    e.insert(0, "0")
    e.bind("<Down>", focus_next);
    e.bind("<Up>", focus_prev);
    e.bind("<Return>", focus_next)
    e.pack(side="right", expand=True, fill="x")
    entries[key] = e

# АВТОЗАГРУЗКА последних данных при старте
last_history = load_history()
if last_history:
    last_date = sorted(last_history.keys())[-1]
    fill_fields(last_history[last_date], mode="last_to_old")

tk.Button(root, text="РАССЧИТАТЬ И СОХРАНИТЬ", command=calculate, bg="green", fg="white", height=2).pack(fill="x",
                                                                                                         padx=20,
                                                                                                         pady=10)
tk.Button(root, text="АРХИВ", command=show_history, bg="orange").pack(fill="x", padx=20, pady=5)
label_result = tk.Label(root, text="", font=("Arial", 10, "bold"), justify="left")
label_result.pack(pady=10)

root.mainloop()