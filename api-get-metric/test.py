from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/test/contr/', endpoint='contr', methods=["POST", "GET"])
@app.route('/test/primary/', endpoint='primary', methods=["POST", "GET"])
def test():
    if request.endpoint == 'contr':
        msg = 'View function test() called from "contr" route'
    elif request.endpoint == 'primary':
        msg = 'View function test() called from "primary" route'
    else:
        msg = 'View function test() called unexpectedly'

    return msg
if __name__ == '__main__':
    app.run(debug=True)