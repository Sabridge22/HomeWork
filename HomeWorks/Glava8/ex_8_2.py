import numpy as np
import matplotlib.pyplot as plt
from scipy import integrate

# функция
def f(x):
    return (x ** 3 - 4*x**2 + x) * np.sin(5*x)

# производная функции
def df(x):
    return (3 * x**2 - 8*x + 1)* np.sin(5*x) + 5*x*(x**2 - 4*x + 1)*np.cos(5*x)

# вторая производная
def df2(x):
    return 10*(3*x**2 - 8*x + 1)*np.cos(5*x) - (25*x**3 - 100*x**2 + 19*x + 8) * np.sin(5*x)

# Задание интервала
x_values = np.linspace(0, 5, 1000)
y_values = f(x_values)

# 1) график функции
plt.figure(figsize=(8, 6))
plt.plot(x_values, y_values, label="График функции")
plt.title("График функции")
plt.show()

# 2) графики первой и второй производных
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(8, 12))

ax1.plot(x_values, df(x_values), label="Первая производная")
ax1.set_title("Первая производная")

ax2.plot(x_values, df2(x_values), label="Вторая производная")
ax2.set_title("Вторая производная")

plt.show()

# 3) точки минимума и максимума
min_index = np.argmin(y_values)
max_index = np.argmax(y_values)
min_point = (x_values[min_index], y_values[min_index])
max_point = (x_values[max_index], y_values[max_index])
x_min, y_min = min_point
x_max, y_max = max_point

fig, ax = plt.subplots(figsize=(8, 6))
ax.plot(x_values, f(x_values), label="График функции")

ax.plot(x_min, y_min, "ro", label="Минимум")  # Точка касания (минимум)
ax.plot(x_max, y_max, "go", label="Максимум")  # Точка касания (максимум)

ax.set_title("Точки минимума и максимума")
ax.legend()
plt.show()

# 4) касательная и нормаль в точке максимума
tangent_equation_max = lambda x: y_max + df(x_max) * (x - x_max)
normal_equation_max = lambda x: y_max - 1 / df(x_max) * (x - x_max)

fig, ax = plt.subplots(figsize=(8, 6))
ax.plot(x_values, f(x_values), label="График функции")

ax.plot(x_values, tangent_equation_max(x_values), "--", label="Касательная (максимум)")
ax.plot(x_values, normal_equation_max(x_values), "--", label="Нормаль (максимум)")
ax.plot(x_max, y_max, "go", label="Максимум")  # точка касания

ax.set_title("Касательная и нормаль в точке максимума")
ax.legend()
plt.show()

# 5) касательное расслоение
num_points = 1000  # количество точек для построения касательных
x_values = np.linspace(0, 5, num_points)

# функция для построения касательного расслоения в заданной точке x
def tangent_lines(x):
    return f(x) + df(x) * (x_values - x)

# построение графика функции
plt.figure(figsize=(8, 6))
plt.plot(x_values, f(x_values), label="График функции")

# построение касательного расслоения для нескольких точек
for x in np.linspace(0, 5, 7):
    plt.plot(x_values, tangent_lines(x), "--", alpha=0.8)

plt.title("Касательное расслоение")
plt.legend()
plt.show()

# 6) длина кривой через интеграл
curve_length, _ = integrate.quad(lambda x: np.sqrt(1 + df(x) ** 2), 0, 5, limit=1000)

print(f"Длина кривой: {curve_length:.2f}")