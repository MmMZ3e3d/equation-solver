from flask import Flask, render_template, request, redirect, url_for
import numpy as np
import matplotlib
matplotlib.use('Agg')  # برای رسم نمودار بدون GUI
import matplotlib.pyplot as plt
import io
import base64
import re

app = Flask(__name__)

# --- تابع استخراج ضرایب از معادله ---
def parse_polynomial(equation):
    equation = equation.replace(' ', '').replace('=0','')
    # پیدا کردن توان‌ها
    terms = re.findall(r'[+-]?[^+-]+', equation)
    max_power = 0
    for t in terms:
        m = re.search(r'x\^(\d+)', t)
        if m:
            p = int(m.group(1))
            if p>max_power: max_power = p
        elif 'x' in t:
            if 1>max_power: max_power=1
    coeffs = [0]*(max_power+1)
    for t in terms:
        m = re.match(r'([+-]?\d*\.?\d*)\*?x\^?(\d*)', t)
        if m:
            coef = float(m.group(1)) if m.group(1) not in ('','+') else 1.0
            if m.group(1)=='-': coef=-1.0
            pow_ = int(m.group(2)) if m.group(2) else (1 if 'x' in t else 0)
            coeffs[max_power - pow_] = coef
        else:
            coeffs[max_power] = float(t)
    return coeffs

# --- ریشه معادله ---
def solve_polynomial(equation):
    coeffs = parse_polynomial(equation)
    roots = np.roots(coeffs)
    return roots

# --- رسم نمودار ---
def plot_polynomial(coeffs):
    x = np.linspace(-10, 10, 400)
    y = np.polyval(coeffs, x)
    plt.figure()
    plt.plot(x,y,label='f(x)')
    plt.axhline(0,color='black',linewidth=0.5)
    plt.axvline(0,color='black',linewidth=0.5)
    plt.grid(True)
    plt.legend()
    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    plt.close()
    buf.seek(0)
    img_base64 = base64.b64encode(buf.getvalue()).decode('utf-8')
    return img_base64

# --- حل سیستم خطی ---
def solve_system(system_text):
    rows = system_text.strip().split('\n')
    A=[]
    b=[]
    for row in rows:
        nums = re.findall(r'[-+]?\d*\.?\d+', row)
        nums = [float(n) for n in nums]
        A.append(nums[:-1])
        b.append(nums[-1])
    A = np.array(A)
    b = np.array(b)
    solution = np.linalg.solve(A,b)
    return solution

# --- مسیر اصلی ---
@app.route('/', methods=['GET','POST'])
def index():
    poly_result = ''
    system_result = ''
    chart_img = ''
    if request.method == 'POST':
        if 'solve_poly' in request.form:
            equation = request.form['polyInput']
            try:
                roots = solve_polynomial(equation)
                poly_result = ', '.join([str(r) for r in roots])
                coeffs = parse_polynomial(equation)
                chart_img = plot_polynomial(coeffs)
            except Exception as e:
                poly_result = f'خطا در حل معادله: {e}'
        if 'solve_system' in request.form:
            system_text = request.form['systemInput']
            try:
                sol = solve_system(system_text)
                system_result = ', '.join([str(s) for s in sol])
            except Exception as e:
                system_result = f'خطا در حل سیستم: {e}'

    return render_template('index.html', poly_result=poly_result, 
                           system_result=system_result, chart_img=chart_img)
import os

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))  # Render مقدار PORT را ست می‌کند
    app.run(host="0.0.0.0", port=port)

