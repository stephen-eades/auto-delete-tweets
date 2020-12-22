from flask import Flask, request, jsonify
app = Flask(__name__)

@app.route('/wakeup/', methods=['GET'])
def respond():
    
    response = {"200"}
    return jsonify(response)