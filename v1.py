from flask import Blueprint, jsonify

app = Blueprint('v1', __name__, url_prefix='/api/v1')


@app.route('/health', methods=['GET'])
def health():
    return jsonify({'status': 'ok'})
