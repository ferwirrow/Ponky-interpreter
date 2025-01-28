from flask import Flask, request, render_template, jsonify
import subprocess

app = Flask(__name__)

# Ruta para servir la interfaz gráfica
@app.route("/")
def index():
    return render_template("index.html")

# Ruta para interpretar el código
@app.route("/interpretar", methods=["POST"])
def interpretar():
    try:
        # Obtén el código proporcionado desde la interfaz
        codigo = request.json.get("codigo", "")
        if not codigo:
            return jsonify({"error": "No se proporcionó código."}), 400

        # Sobrescribe el archivo del script
        script_path = "scripts/myscript.pinky"
        with open(script_path, "w") as file:
            file.write(codigo)

        # Ejecuta pinky.py como subproceso
        comando = ["python3", "pinky.py", script_path]
        proceso = subprocess.run(comando, capture_output=True, text=True)

        # Captura la salida
        salida = proceso.stdout
        errores = proceso.stderr

        if errores:
            return jsonify({"error": errores})
        return jsonify({"output": salida})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)
