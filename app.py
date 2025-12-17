from flask import Flask, render_template, request, jsonify
import easyocr
import numpy as np
from sympy import symbols, Eq, solve
import cv2
import base64
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import io
import os

app = Flask(__name__)

# initialize OCR
reader = easyocr.Reader(['fa','en'])

x = symbols('x')

def normalize_equation(text):
    # اعداد فارسی → انگلیسی
    fa = '۰۱۲۳۴۵۶۷۸۹'
    en = '0123456789'
    for i,f in enumerate(fa):
        text = text.replace(f,en[i])
    # اصلاح علائم
    text = text.replace('×','*').replace('÷','/').replace('−','-')
    # توان‌ها
    text = text.replace('^','**')
    text = text.replace('=','=')
    return text

def solve_equation(equation_text):
    try:
        eq_left = equation_text.split('=')[0]
        eq_sympy = Eq(eval(eq_left),0)
        roots = solve(eq_sympy, x)
        return [str(r) for r in roots]
    except Exception as e:
        print("Error solving equation:", e)
        return []

def generate_plot(equation_text):
    eq_left = equation_text.split('=')[0]
    f = lambda val: eval(eq_left.replace('x','({})'.format(val)))
    X = np.linspace(-10,10,400)
    Y = np.array([f(v) for v in X])
    # convert to list for json
    return X.tolist(), Y.tolist()

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/solve", methods=["POST"])
def solve_route():
    file = request.files.get("image")
    if not file:
        return jsonify({"error":"No image uploaded"})
    
    # read image in memory
    img_bytes = np.frombuffer(file.read(), np.uint8)
    img = cv2.imdecode(img_bytes, cv2.IMREAD_COLOR)
    
    # OCR
    result = reader.readtext(img)
    equation_text = ''.join([t[1] for t in result])
    
    equation_text = normalize_equation(equation_text)
    
    roots = solve_equation(equation_text)
    X, Y = generate_plot(equation_text)
    
    return jsonify({
        "equation": equation_text,
        "roots": roots,
        "x": X,
        "y": Y
    })

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT",5000)))
