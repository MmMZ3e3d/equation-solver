from flask import Flask, render_template, request, jsonify
import numpy as np
import re
import os

app = Flask(__name__)

def parse_polynomial(expr):
    expr = expr.replace(" ", "").replace("=0", "")
    terms = re.findall(r'[+-]?[^+-]+', expr)

    max_pow = 0
    for t in terms:
        if '^' in t:
            max_pow = max(max_pow, int(t.split('^')[1]))
        elif 'x' in t:
            max_pow = max(max_pow, 1)

    coeffs = [0]*(max_pow+1)

    for t in terms:
        if 'x' in t:
            coef_match = re.match(r'([+-]?\d*\.?\d*)\*?x', t)
            coef = coef_match.group(1)
            coef = float(coef) if coef not in ["", "+", "-"] else (-1 if coef == "-" else 1)
            power = int(t.split('^')[1]) if '^' in t else 1
            coeffs[max_pow - power] += coef
        else:
            coeffs[-1] += float(t)

    return coeffs

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/solve", methods=["POST"])
def solve():
    expr = request.json["equation"]
    coeffs = parse_polynomial(expr)
    roots = [str(r) for r in np.roots(coeffs)]
    x = np.linspace(-10, 10, 400).tolist()
    y = np.polyval(coeffs, x).tolist()
    return jsonify({"roots": roots, "x": x, "y": y})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
