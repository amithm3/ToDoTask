from flask import Flask

import v1

app = Flask(__name__)
app.register_blueprint(v1.app)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=9999, debug=True, use_reloader=False)
