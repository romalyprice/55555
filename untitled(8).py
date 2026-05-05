import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
import json
import os

# Создаем главное окно
root = tk.Tk()
root.title("Weather Diary")

# --- Поля для ввода новых записей ---
# Дата
date_label = tk.Label(root, text="Дата (YYYY-MM-DD):")
date_entry = tk.Entry(root)

# Температура
temp_label = tk.Label(root, text="Температура (°C):")
temp_entry = tk.Entry(root)

# Описание погоды
desc_label = tk.Label(root, text="Описание погоды:")
desc_entry = tk.Text(root, height=4, width=30)

# Осадки
precip_var = tk.BooleanVar()
precip_check = tk.Checkbutton(root, text="Осадки", variable=precip_var)

# Размещение элементов для ввода
date_label.grid(row=0, column=0, sticky='w', padx=5, pady=2)
date_entry.grid(row=0, column=1, padx=5, pady=2)

temp_label.grid(row=1, column=0, sticky='w', padx=5, pady=2)
temp_entry.grid(row=1, column=1, padx=5, pady=2)

desc_label.grid(row=2, column=0, sticky='w', padx=5, pady=2)
desc_entry.grid(row=2, column=1, padx=5, pady=2)

precip_check.grid(row=3, column=0, columnspan=2, sticky='w', padx=5, pady=2)

# --- Функции ---
entries = []

def clear_fields():
    date_entry.delete(0, tk.END)
    temp_entry.delete(0, tk.END)
    desc_entry.delete("1.0", tk.END)
    precip_var.set(False)

def add_entry():
    date_str = date_entry.get()
    temp_str = temp_entry.get()
    description = desc_entry.get("1.0", tk.END).strip()
    precip = precip_var.get()

    # Валидация
    try:
        datetime.strptime(date_str, "%Y-%m-%d")
    except:
        messagebox.showerror("Ошибка", "Некорректный формат даты")
        return

    try:
        temperature = float(temp_str)
    except:
        messagebox.showerror("Ошибка", "Температура должна быть числом")
        return

    if not description:
        messagebox.showerror("Ошибка", "Описание не должно быть пустым")
        return

    record = {
        "date": date_str,
        "temperature": temperature,
        "description": description,
        "precipitation": precip
    }
    entries.append(record)
    messagebox.showinfo("Успех", "Запись добавлена")
    clear_fields()
    display_records(entries)

add_button = tk.Button(root, text="Добавить запись", command=add_entry)
add_button.grid(row=4, column=0, columnspan=2, pady=5)

# --- Таблица для отображения записей ---
columns = ("date", "temp", "desc", "precip")
tree = ttk.Treeview(root, columns=columns, show='headings')
tree.heading("date", text="Дата")
tree.heading("temp", text="Температура")
tree.heading("desc", text="Описание")
tree.heading("precip", text="Осадки")
tree.grid(row=8, column=0, columnspan=2, sticky='nsew', pady=10)

# Расширение таблицы при изменениях размера
root.grid_rowconfigure(8, weight=1)
root.grid_columnconfigure(1, weight=1)

def display_records(records):
    for row in tree.get_children():
        tree.delete(row)
    for record in records:
        tree.insert("", "end", values=(
            record["date"],
            record["temperature"],
            record["description"],
            "Да" if record["precipitation"] else "Нет"
        ))

# --- Фильтрация ---
filter_frame = tk.LabelFrame(root, text="Фильтры")
filter_frame.grid(row=9, column=0, columnspan=2, sticky='ew', padx=5, pady=5)

# Фильтр по дате
filter_date_label = tk.Label(filter_frame, text="По дате (YYYY-MM-DD):")
filter_date_var = tk.StringVar()
filter_date_entry = tk.Entry(filter_frame, textvariable=filter_date_var)

# Фильтр по температуре
filter_temp_label = tk.Label(filter_frame, text="Температура выше (°C):")
filter_temp_var = tk.StringVar()
filter_temp_entry = tk.Entry(filter_frame, textvariable=filter_temp_var)

# Размещение фильтров
filter_date_label.grid(row=0, column=0, padx=5, pady=2)
filter_date_entry.grid(row=0, column=1, padx=5, pady=2)
filter_temp_label.grid(row=0, column=2, padx=5, pady=2)
filter_temp_entry.grid(row=0, column=3, padx=5, pady=2)

def apply_filters():
    filtered = entries
    date_filter = filter_date_var.get().strip()
    temp_filter = filter_temp_var.get().strip()

    if date_filter:
        try:
            datetime.strptime(date_filter, "%Y-%m-%d")
            filtered = [e for e in filtered if e["date"] == date_filter]
        except:
            messagebox.showerror("Ошибка", "Некорректный формат даты для фильтра")
            return

    if temp_filter:
        try:
            temp_threshold = float(temp_filter)
            filtered = [e for e in filtered if e["temperature"] > temp_threshold]
        except:
            messagebox.showerror("Ошибка", "Температура должна быть числом для фильтра")
            return

    display_records(filtered)

filter_button = tk.Button(filter_frame, text="Применить фильтры", command=apply_filters)
filter_button.grid(row=1, column=0, columnspan=4, pady=5)

# --- Сохранение и загрузка ---
def save_to_json():
    with open("weather_data.json", "w", encoding="utf-8") as f:
        json.dump(entries, f, ensure_ascii=False, indent=4)
    messagebox.showinfo("Сохранено", "Данные сохранены в weather_data.json")

def load_from_json():
    global entries
    if os.path.exists("weather_data.json"):
        with open("weather_data.json", "r", encoding="utf-8") as f:
            try:
                loaded = json.load(f)
                if isinstance(loaded, list):
                    entries.clear()
                    entries.extend(loaded)
                    display_records(entries)
            except json.JSONDecodeError:
                messagebox.showerror("Ошибка", "Ошибка чтения JSON файла")
    else:
        # файл не найден, ничего не делаем
        pass

# Кнопки сохранения и загрузки
save_button = tk.Button(root, text="Сохранить в JSON", command=save_to_json)
save_button.grid(row=10, column=0, pady=5)

load_button = tk.Button(root, text="Загрузить из JSON", command=load_from_json)
load_button.grid(row=10, column=1, pady=5)

# Загружаем данные при старте
load_from_json()

# Запуск GUI
root.mainloop()