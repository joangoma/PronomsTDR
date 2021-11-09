from flask import Flask, jsonify
import introduirDades

app = Flask(__name__)

@app.route('/pronominalitza/<cadena>', methods=['GET'])
def pronominalitza(cadena):
    if len(cadena) > 0:
        dades = {'frase': introduirDades.entrada(cadena), 'svg': introduirDades.return_svg(cadena)}
        return jsonify(dades)

if __name__ == '__main__':
    app.run(port="5001")