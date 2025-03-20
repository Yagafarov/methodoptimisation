import numpy as np
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Метод золотого сечения
def golden_section_search(a, b, epsilon, func):
    tau = (np.sqrt(5) - 1) / 2  
    iterations = []  # Сохраняем интервал на каждой итерации
    
    # Вычисляем начальные точки:
    x1 = b - tau * (b - a)
    x2 = a + tau * (b - a)
    f1 = func(x1)
    f2 = func(x2)
    
    # Выполняем итерации
    n = 1  # Номер итерации
    while (b - a) > epsilon:
        iterations.append([n, x1, f1])
        if f1 < f2:
            # Минимум находится слева
            b = x2
            x2 = x1
            f2 = f1
            x1 = b - tau * (b - a)
            f1 = func(x1)
        else:
            # Минимум находится справа
            a = x1
            x1 = x2
            f1 = f2
            x2 = a + tau * (b - a)
            f2 = func(x2)
        n += 1
    
    # Определяем конечную минимальную точку:
    lam_min = (a + b) / 2
    f_min = func(lam_min)
    iterations.append([n, lam_min, f_min])  # Добавляем последнюю итерацию
    return lam_min, f_min, iterations

# Метод Фибоначчи
def fibonacci_search(a, b, epsilon, func):
    phi = (1 + np.sqrt(5)) / 2  # Число золотого сечения
    iterations = []  # Сохраняем интервал на каждой итерации
    
    # Определяем количество шагов для вычислений
    n = int(np.ceil(np.log((b - a) / epsilon) / np.log(phi)))
    
    # Вычисляем начальные точки
    x1 = a + (b - a) / phi
    x2 = b - (b - a) / phi
    f1 = func(x1)
    f2 = func(x2)
    
    # Выполняем итерации
    for i in range(1, n):
        iterations.append([i, x1, f1])
        if f1 < f2:
            b = x2
            x2 = x1
            f2 = f1
            x1 = a + (b - a) / phi
            f1 = func(x1)
        else:
            a = x1
            x1 = x2
            f1 = f2
            x2 = b - (b - a) / phi
            f2 = func(x2)
    
    # Определяем минимальную точку
    lam_min = (a + b) / 2
    f_min = func(lam_min)
    iterations.append([n, lam_min, f_min])  # Добавляем последнюю итерацию
    return lam_min, f_min, iterations

# Метод локализации экстремума функции
def extremum_localization(a, b, epsilon, func):
    # Здесь используется метод поиска экстремума методом деления интервала пополам
    iterations = []  # Сохраняем интервал на каждой итерации
    
    n = 1  # Номер итерации
    while (b - a) > epsilon:
        mid = (a + b) / 2
        f1 = func(mid - epsilon)
        f2 = func(mid + epsilon)
        
        iterations.append([n, mid, (f1 + f2) / 2])
        
        if f1 < f2:
            b = mid
        else:
            a = mid
        
        n += 1
    
    lam_min = (a + b) / 2
    f_min = func(lam_min)
    iterations.append([n, lam_min, f_min])  # Добавляем последнюю итерацию
    return lam_min, f_min, iterations

# Настройка интерфейса Streamlit
st.set_page_config(page_title="Метод Золотого Сечения", layout="centered")
st.title("Минимизация функции с помощью различных методов")

# Получаем параметры от пользователя
a = st.number_input("Введите значение a:", min_value=0.000, step=0.1, value=0.425, format="%.3f")
b = st.number_input("Введите значение b:", min_value=0.000, step=0.1, value=1.275, format="%.3f")
epsilon = st.number_input("Введите значение Epsilon ε:", min_value=0.0001, step=0.0001, value=0.0045, format="%.4f")

# Функция, введенная пользователем
user_function = st.text_area("Введите функцию R(λ) [λ=lam]:", value="lam*lam + (1/lam*lam)", height=100)

# Преобразуем введенную строку в функцию
def R(lam):
    return eval(user_function)

# Выбор метода
method = st.selectbox("Выберите метод минимизации:", ["Метод золотого сечения", "Метод Фибоначчи", "Метод локализации экстремума"])

# Кнопка для выполнения расчётов
if st.button("Выполнить"):
    if method == "Метод золотого сечения":
        lam_min, f_min, iter_data = golden_section_search(a, b, epsilon, R)
    elif method == "Метод Фибоначчи":
        lam_min, f_min, iter_data = fibonacci_search(a, b, epsilon, R)
    elif method == "Метод локализации экстремума":
        lam_min, f_min, iter_data = extremum_localization(a, b, epsilon, R)

    st.write(f"### Минимальная точка: λ = {lam_min}")
    st.write(f"### Минимальное значение функции: R(λ) = {f_min:.6f}")  # Значение функции с 6 знаками после запятой
    st.write(f"### Общее количество итераций: {len(iter_data)}")
    
    # Показать таблицу с итерациями
    iter_df = pd.DataFrame(iter_data, columns=["n - номер эксперимента", "Адрес эксперимента ƛn", "Значение целевой функции R(λn)"])
    st.write("### Таблица итераций", iter_df)
    
    # Построить график
    x_vals = [row[1] for row in iter_data]  # Значения ƛn
    f_vals = [row[2] for row in iter_data]  # Значения R(λn)
    
    fig, ax = plt.subplots(figsize=(8, 6))
    ax.plot(x_vals, f_vals, label="R(λn)", marker='o', color='blue', linestyle='-', markersize=6, linewidth=2)
    
    # Добавление вертикальных и горизонтальных линий для лучшего восприятия
    ax.axvline(x=lam_min, color='red', linestyle='--', label=f'Минимум (λ = {lam_min:.4f})')
    ax.axhline(y=f_min, color='green', linestyle='--', label=f'R(λ) = {f_min:.6f}')
    
    # Настройки графика
    ax.set_xlabel("ƛn", fontsize=12)
    ax.set_ylabel("Значение функции R(λn)", fontsize=12)
    ax.set_title("Итерации метода минимизации", fontsize=14)
    ax.legend()
    ax.grid(True, which='both', linestyle='--', linewidth=0.5, color='gray')  # Сетка
    
    # Добавление аннотации
    ax.annotate(f"Минимум: (λ = {lam_min:.4f}, R(λ) = {f_min:.6f})", 
                xy=(lam_min, f_min), 
                xytext=(lam_min + 0.05, f_min + 0.1),
                arrowprops=dict(facecolor='black', arrowstyle="->"),
                fontsize=10)
    
    st.pyplot(fig)

st.write("Имя: Динмухаммад Ягафаров")
st.write("Веб-сайт: [www.anodra.uz](https://anodra.uz)")
