import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider, RadioButtons, CheckButtons, Button

# параметры фигуры Лиссажу
a, b, delta = 2, 3, np.pi / 4

# функция Лиссажу
def lissajous(a: int, b: int, delta: float, t: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    x = np.sin(a * t + delta)
    y = np.sin(b * t)
    return x, y

def tangent_line_coefficients(a: int, b: int, delta: float, t: float) -> tuple[float, float]: # находит коэф. ур. касат.
    x, y = lissajous(a, b, delta, t)
    dx_dt = a * np.cos(a * t + delta)
    dy_dt = b * np.cos(b * t)
    # вычисление коэффициента наклона касательной
    slope = dy_dt / dx_dt
    # вычисление пересечения касательной с осью y
    intercept = y - slope * x
    return slope, intercept

# обновление графика при изменении положения слайдера
def update_graph(val: float) -> None:
    global point, tangent_line, line
    t = slider_position.val
    x, y = lissajous(a, b, delta, t)

    point.set_data(x, y)

    if show_tangent: # проверка, нужно ли показывать касательную
        slope, intercept = tangent_line_coefficients(a, b, delta, t) # вычисление коэф. уравнения касат. в момент t
        tangent_line.set_data([x - 1, x + 1], [slope * (x - 1) + intercept, slope * (x + 1) + intercept]) # показ. на графике
    else:
        tangent_line.set_data([], [])

    fig.canvas.draw_idle()

# сброс положения точки
def reset_point(val: float) -> None:
    slider_position.set_val(0)
    update_graph(0)  # вызов функции обновления для отображения начальной точки

# переключение отображения касательной
def toggle_tangent(label: str) -> None:
    global show_tangent
    show_tangent = not show_tangent

    # вызов функции обновления для отображения касательной
    update_graph(0)

# изменение стиля линии фигуры Лиссажу
def change_line_style(label: str) -> None:
    line.set_linestyle(styles[label])
    fig.canvas.draw_idle()

# изменение цвета линии фигуры Лиссажу
def change_line_color(label: str) -> None:
    line.set_color(colors[label])
    fig.canvas.draw_idle()

# фиксированное начальное положение точки
initial_position = 0

# генерация значений времени в диапазоне от 0 до 2*pi
t_values = np.linspace(0, 2 * np.pi, 1000)
# вычисление координат x и y для фигуры Лиссажу
x_values, y_values = lissajous(a, b, delta, t_values)
# построение графика
fig, ax = plt.subplots(figsize=(8, 6))
# построение линии фигуры Лиссажу
(line,) = ax.plot(x_values, y_values, label="Лиссажу", linestyle="-", color="purple")

# отображение начальной точки
(point,) = ax.plot([], [], "ro", markersize=8)
(tangent_line,) = ax.plot([], [], "k--")

show_tangent = False

slider_ax_position = plt.axes([0.2, 0.01, 0.65, 0.03])
slider_position = Slider(slider_ax_position, "Положение", 0, 2 * np.pi, valinit=initial_position, valstep=0.01)
slider_position.on_changed(update_graph)

reset_button_ax = plt.axes([0.85, 0.8, 0.1, 0.04])
reset_button = Button(reset_button_ax, "Сброс")
reset_button.on_clicked(reset_point)

tangent_checkbox_ax = plt.axes([0.85, 0.75, 0.1, 0.04])
tangent_checkbox = CheckButtons(tangent_checkbox_ax, ["Касат."], actives=[False])
tangent_checkbox.on_clicked(toggle_tangent)

colors = {"purple": "purple", "red": "red", "blue": "blue", "green": "green"}
styles = {"-": "-", "--": "--", "-.": "-."}

radio_buttons_ax_color = plt.axes([0.85, 0.5, 0.1, 0.2])
radio_buttons_color = RadioButtons(radio_buttons_ax_color, list(colors.keys()))
radio_buttons_color.on_clicked(change_line_color)

radio_buttons_ax_style = plt.axes([0.85, 0.25, 0.1, 0.2])
radio_buttons_style = RadioButtons(radio_buttons_ax_style, list(styles.keys()))
radio_buttons_style.on_clicked(change_line_style)

update_graph(0)

if __name__ == "__main__":
    plt.show()
