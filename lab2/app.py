from flask import Flask, jsonify, render_template, request

from tools.dsa import gen_params_dsa, dsa_sign, dsa_verify
from tools.exceptions import SignatureError
from tools.rsa import sign_rsa, verify_rsa, gen_rsa_keys
from tools.utils import validate_data

app = Flask(__name__, static_url_path='/static')


@app.route('/api_doc', methods=['GET'])
def api_doc():
    return jsonify({
        'RSA keys pair': '/keys_rsa GET',
        'RSA sign message': '/sign_rsa POST {private: {n, d}, message} ', 
        'RSA verify signature': '/verify_rsa POST {message, signature, public: {d, e}}',
        'DSA params data': '/keys_dsa GET',
        'DSA sign message': '/sign_dsa POST {message, params:{p, q, g}, private}',
        'DSA varify message': '/verify_dsa POST {message, signature:{r, s}, params:{p, q, g}, private}', 
    })


@app.route('/', methods=['GET'])
def home():
    return render_template('index.html')


@app.route('/rsa/keys', methods=['GET'])
def get_keys_rsa():
    return jsonify(gen_rsa_keys())


@app.route('/rsa/sign', methods=['POST'])
def sign_rsa_route():
    print(request.json)
    validate_data(request.json, ['message', 'private'])

    message = request.json['message']
    priv = request.json['private']
    signature = sign_rsa(message.encode(), priv)
    return jsonify({'signature': signature.hex()})


@app.route('/rsa/verify', methods=['POST'])
def verify_rsa_route():
    validate_data(request.json, ['message', 'signature', 'public'])

    message = request.json['message']
    signature_str = request.json['signature']
    pub = request.json['public']
    signature_bytes = bytes.fromhex(signature_str)

    if verify_rsa(message.encode(), signature_bytes, pub):
        response = jsonify({'status': 'VALID'})
        response.status_code = 200
    else:
        response = jsonify({'status': 'INVALID'})
        response.status_code = 400
    return response


@app.route('/dsa/keys', methods=['GET'])
def get_params_dsa():
    return jsonify(gen_params_dsa())

@app.route('/dsa/sign', methods=['POST'])
def sign_dsa_route():
    validate_data(request.json, ['message', 'params', 'private'])
    validate_data(request.json['params'], ['p', 'q', 'g'], field='params')
    
    message = request.json['message'].encode()
    params = request.json['params']
    private_key = request.json['private']

    signature = dsa_sign(message, params, private_key)
    return jsonify({'signature': signature})


@app.route('/dsa/verify', methods=['POST'])
def verify_dsa_route():
    validate_data(request.json, ['message', 'signature', 'params', 'public'])
    validate_data(request.json['params'], ['p', 'q', 'g'], field='params')
    validate_data(request.json['signature'], ['r', 's'], field='signature')

    message = request.json['message'].encode()
    signature = request.json['signature']
    params = request.json['params']
    public_key = request.json['public']

    is_valid = dsa_verify(message, signature, params, public_key)

    if is_valid:
        response = jsonify({'status': 'VALID'})
        response.status_code = 200
    else:
        response = jsonify({'status': 'INVALID'})
        response.status_code = 400
    return response


@app.errorhandler(SignatureError)
def handle_rsa_signature_error(error):
    response = jsonify(error.to_dict())
    response.status_code = error.status_code
    return response

@app.errorhandler(Exception)
def handle_all_errors(error):
    response = jsonify({'error': 'Unexpected error happen contact the author'})
    response.status_code = 500
    return response

if __name__ == "__main__":
    app.run(debug=True)
