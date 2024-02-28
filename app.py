from flask import Flask

import app_v1
import app_auth

app = Flask(__name__)
app.register_blueprint(app_v1.app)
app.register_blueprint(app_auth.app)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=9999, debug=True, use_reloader=False)

# @app.route('/template')
# def template():
#     data = request.get_json()
#     args = request.args
#     try:
#         pass
#     except Error4XX as e:
#         return jsonify({'error': str(e)}), e.xx
#     except Exception as e:
#         logging.error(e)
#         return jsonify({'error': "Something went wrong"}), 500
