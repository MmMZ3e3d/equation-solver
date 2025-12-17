from flask import Flask, render_template, request, jsonify
import numpy as np
from sympy import symbols, Eq, solve

app = Flask(__name__)
x = symbols('x')

def solve_equation(equation_text):
    try:
        eq_left = equation_text.split('=')[0]
        eq_sympy = Eq(eval(eq_left.replace('^','**')), 0)
        roots = solve(eq_sympy, x)
        return [str(r) for r in roots]
    except Exception as e:
        print("Error:", e)
        return []

def generate_plot(equation_text):
    eq_left = equation_text.split('=')[0].replace('^','**')
    f = lambda val: eval(eq_left.replace('x',f'({val})'))
    X = np.linspace(-10,10,400)
    Y = np.array([f(v) for v in X])
    return X.tolist(), Y.tolist()

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/solve", methods=["POST"])
def solve_route():
    data = request.get_json()
    equation_text = data.get("equation")
    if not equation_text:
        return jsonify({"error":"No equation received"})
    roots = solve_equation(equation_text)
    X,Y = generate_plot(equation_text)
    return jsonify({"roots":roots,"x":X,"y":Y})

if __name__=="__main__":
    app.run(host="0.0.0.0", port=5000)
