from flask import Flask, request, jsonify, render_template

from tools import encrypt

app = Flask(__name__,  static_url_path='/static')


@app.route('/', methods=['GET'])
def home():
    return render_template('index.html')


@app.route('/hasher', methods=['POST'])
def hasher():
    errors = {}
    valid_data = {}
    data = request.json
    required = ('hasher', 'key', 'message')
    for key in required:
        if not data.get(key):
            errors[key] = f'invalid {key}'
        valid_data[key] = data.get(key)
    if errors:
        return jsonify({'error': errors})

    hash = encrypt(valid_data)
    if not hash:
        return jsonify({'error': 'Selected encoder not implemented'})
    return jsonify({'hash': hash})



if __name__ == "__main__":
    app.run(debug=False)