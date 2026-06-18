import math
import os
from flask import Flask, render_template, request

app = Flask(__name__)


def format_number(x):
    if isinstance(x, (int, float)):
        if x.is_integer():
            return str(int(x))
        return f"{round(x, 2)}".rstrip('0').rstrip('.')
    return str(x)


def solve_quadratic(a, b, c):
    delta = b ** 2 - 4 * a * c

    a_str = format_number(a)
    b_str = format_number(b)
    c_str = format_number(c)
    delta_str = format_number(delta)

    # Zmiana znaku b na przeciwny do wzoru pierwiastków
    minus_b_str = format_number(-b)

    results = {
        'delta_formula': f"Δ = {b_str}² - 4 * {a_str} * {c_str}",
        'delta': delta_str,
        'is_invisible': False,
        'steps': []
    }

    # Mianownik to zawsze 2 * a
    mianownik = format_number(2 * a)

    if delta > 0:
        sqrt_delta = delta ** 0.5
        results['steps'].append("Δ > 0, istnieją dwa pierwiastki.")

        if sqrt_delta.is_integer():
            sqrt_str = format_number(sqrt_delta)
            x1 = (-b - sqrt_delta) / (2 * a)
            x2 = (-b + sqrt_delta) / (2 * a)

            results['x1'] = {
                'licznik': f"{minus_b_str} - {sqrt_str}",
                'mianownik': mianownik,
                'wynik': format_number(x1),
                'znak': '='
            }
            results['x2'] = {
                'licznik': f"{minus_b_str} + {sqrt_str}",
                'mianownik': mianownik,
                'wynik': format_number(x2),
                'znak': '='
            }
        else:
            x1_approx = (-b - sqrt_delta) / (2 * a)
            x2_approx = (-b + sqrt_delta) / (2 * a)

            results['x1'] = {
                'licznik': f"{minus_b_str} - √{delta_str}",
                'mianownik': mianownik,
                'wynik': format_number(x1_approx),
                'znak': '≈'
            }
            results['x2'] = {
                'licznik': f"{minus_b_str} + √{delta_str}",
                'mianownik': mianownik,
                'wynik': format_number(x2_approx),
                'znak': '≈'
            }
            results['steps'].append(
                f"Uwaga: Pierwiastek z Δ (√{delta_str}) jest liczbą niewymierną. Poniżej podano zapis symboliczny oraz przybliżenie:")

    elif delta == 0:
        x0 = -b / (2 * a)
        results['steps'].append("Δ = 0, istnieje jeden pierwiastek podwójny:")
        results['x0'] = {
            'licznik': minus_b_str,
            'mianownik': mianownik,
            'wynik': format_number(x0),
            'znak': '='
        }
    else:
        results['steps'].append("Δ < 0, brak pierwiastków rzeczywistych.")

    return results


@app.route('/', methods=['GET', 'POST'])
def index():
    error = None
    results = None
    form_data = {'a': '', 'b': '', 'c': ''}

    if request.method == 'POST':
        raw_a = request.form.get('a', '').replace(',', '.')
        raw_b = request.form.get('b', '').replace(',', '.')
        raw_c = request.form.get('c', '').replace(',', '.')

        form_data = {'a': raw_a, 'b': raw_b, 'c': raw_c}

        try:
            if not raw_a or not raw_b or not raw_c:
                raise ValueError("Wszystkie pola muszą być wypełnione.")

            a, b, c = float(raw_a), float(raw_b), float(raw_c)

            if a == 0:
                error = "To nie jest równanie kwadratowe, lecz liniowe (a nie może być równe 0)!"
            else:
                results = solve_quadratic(a, b, c)

        except ValueError as e:
            if "could not convert string to float" in str(e):
                error = "Proszę wpisać poprawne liczby rzeczywiste."
            else:
                error = str(e)

    return render_template('index.html', error=error, results=results, form=form_data)


if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port, debug=True)