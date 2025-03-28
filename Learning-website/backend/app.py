from flask import Flask, render_template,jsonify, request,send_from_directory
from modules.floyd_cycle import detect_cycle

app = Flask(__name__, static_folder='../frontend')

@app.route('/')
def serve_frontend():
    return send_from_directory(app.static_folder, 'index.html')


@app.route('/cycle', methods=['POST'])
def cycle():
    data = request.json
    if 'list' not in data:
        return jsonify({"error": "No list provided"}), 400
    
    linked_list = data['list']
    has_cycle = detect_cycle(linked_list)
    
    return jsonify({"has_cycle": has_cycle})

if __name__ == '__main__':
    app.run(debug=True)