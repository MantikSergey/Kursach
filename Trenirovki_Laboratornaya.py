import tkinter as tk
from tkinter import ttk
from datetime import datetime, timedelta

# Список всех карт абонементов
cards = ["123", "456", "789"]

# Список всех занятий
start_date = datetime(2024, 5, 6)
end_date = start_date + timedelta(days=6)
classes = [
    {"type": "Йога", "time": ["10:00", "11:00", "12:00"], "location": "Зал 1", "trainer": "Анна", "capacity": 20, "age_limit": 16, "class_type": "Групповое", "date": start_date.strftime("%Y-%m-%d")},
    {"type": "Бокс", "time": ["15:00", "16:00", "17:00"], "location": "Зал 2", "trainer": "Иван", "capacity": 1, "age_limit": 18, "class_type": "Индивидуальное", "date": (start_date + timedelta(days=1)).strftime("%Y-%m-%d")},
    {"type": "Пилатес", "time": ["18:00", "19:00", "20:00"], "location": "Зал 3", "trainer": "Мария", "capacity": 12, "age_limit": 14, "class_type": "Групповое", "date": (start_date + timedelta(days=2)).strftime("%Y-%m-%d")}
]

# Список забронированных тренировок
booked_classes = []

def login():

    # Получаем номер карты из поля ввода
    card_number = card_entry.get()
    
    # Проверяем, был ли введен номер карты
    if not card_number:
        # Если номер карты не введен, выводим сообщение об ошибке
        message_label.config(text="Пожалуйста, введите номер карты.")
        return
    
    # Проверяем, есть ли введенный номер карты в списке
    if card_number in cards:
        # Если номер карты найден, закрываем окно авторизации и открываем главный экран
        auth_window.destroy()
        show_main_screen()
    else:
        # Если номер карты не найден, выводим сообщение об ошибке
        message_label.config(text="Неверный номер карты. Попробуйте еще раз.", fg="red")

def show_main_screen():
    # Создаем окно главного экрана
    main_window = tk.Tk()
    main_window.title("Тренажерный клуб 'Boss of the ♂GYM♂' ")
    
    # Создаем таблицу для отображения занятий
    global class_table, message_label
    class_table = ttk.Treeview(main_window)
    class_table["columns"] = ("Вид", "Время", "Место", "Тренер", "Тип", "Дата", "Места", "Возраст")
    class_table.column("#0", width=50)
    class_table.column("Вид", width=60)
    class_table.column("Время", width=110)
    class_table.column("Место", width=50)
    class_table.column("Тренер", width=70)
    class_table.column("Тип", width=110)
    class_table.column("Дата", width=100)
    class_table.column("Места", width=140)
    class_table.column("Возраст", width=160)
    class_table.heading("#0", text="ID")
    class_table.heading("Вид", text="Вид")
    class_table.heading("Время", text="Время")
    class_table.heading("Место", text="Место")
    class_table.heading("Тренер", text="Тренер")
    class_table.heading("Тип", text="Тип")
    class_table.heading("Дата", text="Дата")
    class_table.heading("Места", text="Свободные места")
    class_table.heading("Возраст", text="Возрастное ограничение")
    
    # Заполняем таблицу данными о занятиях
    for i, class_info in enumerate(classes):
        class_table.insert("", "end", text=str(i+1), values=(
            class_info["type"],
            ", ".join(class_info["time"]),
            class_info["location"],
            class_info["trainer"],
            class_info["class_type"],
            class_info["date"],
            class_info["capacity"] if class_info["class_type"] == "Групповое" else 1,
            class_info["age_limit"]
        ))
    
    # Обрабатываем событие нажатия на ячейку с временем
    def show_time_options(event):
        # Получаем выбранную строку в таблице
        selected_item = class_table.identify_row(event.y)
        if selected_item:
            # Получаем данные о выбранном занятии
            values = class_table.item(selected_item)["values"]
            class_type = values[0]
            class_times = [t for t in classes[int(class_table.item(selected_item)["text"]) - 1]["time"]]
            
            # Создаем всплывающее меню с доступными временами
            time_menu = tk.Menu(main_window, tearoff=0)
            for time in class_times:
                time_menu.add_command(label=time, command=lambda t=time: update_time(selected_item, t))
            time_menu.post(event.x_root, event.y_root)
    
    def update_time(selected_item, new_time):
        # Обновляем ячейку с временем в таблице
        class_table.set(selected_item, "Время", new_time)
    
    # Обрабатываем событие нажатия на ячейку с датой
    def show_date_options(event):
        # Получаем выбранную строку в таблице
        selected_item = class_table.identify_row(event.y)
        if selected_item:
            # Получаем данные о выбранном занятии
            values = class_table.item(selected_item)["values"]
            class_date = values[5]
            
            # Создаем всплывающее меню с доступными датами
            date_menu = tk.Menu(main_window, tearoff=0)
            current_date = start_date
            while current_date <= end_date:
                date_menu.add_command(label=current_date.strftime("%Y-%m-%d"), command=lambda d=current_date.strftime("%Y-%m-%d"): update_date(selected_item, d))
                current_date += timedelta(days=1)
            date_menu.post(event.x_root, event.y_root)
    
    def update_date(selected_item, new_date):
        # Обновляем ячейку с датой в таблице
        class_table.set(selected_item, "Дата", new_date)
    
    class_table.bind("<Double-1>", show_time_options, add="+")
    class_table.bind("<Double-1>", show_date_options, add="+")
    class_table.pack()
    
    # Создаем кнопку для бронирования занятия
    book_button = tk.Button(main_window, text="Забронировать", command=lambda: book_class(class_table))
    book_button.pack(side=tk.BOTTOM, pady=10)
    
    # Создаем кнопку для перехода к окну "Мои тренировки"
    my_classes_button = tk.Button(main_window, text="Мои тренировки", command=show_my_classes)
    my_classes_button.pack(side=tk.BOTTOM, pady=10)
    
    # Создаем виджет для вывода сообщений
    message_label = tk.Label(main_window, text="")
    message_label.pack(side=tk.BOTTOM, pady=10)
    
    # Запускаем главный цикл приложения
    main_window.mainloop()

def book_class(class_table):
    # Получаем выбранную строку в таблице
    selected_item = class_table.focus()
    if selected_item:
        # Получаем данные о выбранном занятии
        values = class_table.item(selected_item)["values"]
        class_type = values[0]
        class_time = values[1]
        class_location = values[2]
        class_trainer = values[3]
        class_class_type = values[4]
        class_date = values[5]
        
        # Сохраняем информацию о забронированной тренировке
        booked_class = {
            "type": class_type,
            "time": class_time,
            "location": class_location,
            "trainer": class_trainer,
            "class_type": class_class_type,
            "date": class_date
        }
        booked_classes.append(booked_class)
        
        # Выводим сообщение об успешном бронировании
        message_label.config(text=f"{class_class_type.capitalize()} занятие '{class_type}' в {class_time} на {class_date} успешно забронировано!")
    else:
        # Если строка не выбрана, выводим сообщение об ошибке
        message_label.config(text="Пожалуйста, выберите занятие для бронирования.")

def show_my_classes():
    # Создаем окно "Мои тренировки"
    my_classes_window = tk.Tk()
    my_classes_window.title("Мои тренировки")
    
    # Создаем таблицу для отображения забронированных тренировок
    booked_classes_table = ttk.Treeview(my_classes_window)
    booked_classes_table["columns"] = ("Вид", "Время", "Место", "Тренер", "Тип", "Дата")
    booked_classes_table.column("#0", width=100)
    booked_classes_table.column("Вид", width=100)
    booked_classes_table.column("Время", width=100)
    booked_classes_table.column("Место", width=100)
    booked_classes_table.column("Тренер", width=100)
    booked_classes_table.column("Тип", width=100)
    booked_classes_table.column("Дата", width=100)
    booked_classes_table.heading("#0", text="ID")
    booked_classes_table.heading("Вид", text="Вид")
    booked_classes_table.heading("Время", text="Время")
    booked_classes_table.heading("Место", text="Место")
    booked_classes_table.heading("Тренер", text="Тренер")
    booked_classes_table.heading("Тип", text="Тип")
    booked_classes_table.heading("Дата", text="Дата")
    
    # Заполняем таблицу данными о забронированных тренировках
    for i, booked_class in enumerate(booked_classes):
        booked_classes_table.insert("", "end", text=str(i+1), values=(
            booked_class["type"],
            booked_class["time"],
            booked_class["location"],
            booked_class["trainer"],
            booked_class["class_type"],
            booked_class["date"]
        ))
    
    booked_classes_table.pack()
    
    # Создаем кнопку для отмены тренировки
    cancel_button = tk.Button(my_classes_window, text="Отменить тренировку", command=lambda: cancel_class(booked_classes_table))
    cancel_button.pack(side=tk.BOTTOM, pady=10)
    
    # Запускаем главный цикл приложения
    my_classes_window.mainloop()

def cancel_class(booked_classes_table):
    # Получаем выбранную строку в таблице
    selected_item = booked_classes_table.focus()
    if selected_item:
        # Удаляем выбранную тренировку из списка забронированных
        index = int(booked_classes_table.item(selected_item)["text"]) - 1
        del booked_classes[index]
        
        # Обновляем таблицу забронированных тренировок
        booked_classes_table.delete(selected_item)
        
        # Выводим сообщение об успешной отмене
        message_label.config(text="Тренировка успешно отменена.")
    else:
        # Если строка не выбрана, выводим сообщение об ошибке
        message_label.config(text="Пожалуйста, выберите тренировку для отмены.")

# Создаем окно авторизации
auth_window = tk.Tk()
auth_window.title("Авторизация в тренажерном клубе")
auth_window.geometry("370x90")

# Создаем виджеты для ввода номера карты и кнопки входа
card_label = tk.Label(auth_window, text="Введите номер карты:")
card_entry = tk.Entry(auth_window)
login_button = tk.Button(auth_window, text="Войти", command=login)
message_label = tk.Label(auth_window, text="")

# Размещаем виджеты в окне авторизации
card_label.pack()
card_entry.pack()
login_button.pack()
message_label.pack()

# Запускаем главный цикл приложения
auth_window.mainloop()