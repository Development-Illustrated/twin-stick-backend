from flask import Flask
from flask import jsonify
import gen

app = Flask(__name__)


@app.route('/gen')
def gen():
    d = gen.main()
    return jsonify(d)
