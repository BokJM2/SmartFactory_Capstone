# app.py
from flask import Flask, jsonify, request
from fashion import get_data

app = Flask(__name__) # 创建flask应用

# 默认为get请求
@app.route('/v1/fashion', methods=['POST'])
def fashion():
    auth_header = request.headers.get('Authorization')
    if auth_header != 'Bearer Fashion!@#':
        return jsonify({"error": "Invalid Authorization header"}), 500
    payload = request.json
    query = payload['query']
    data, err = get_data(query, model="Qwen/Qwen2.5-7B-Instruct")
    if err:
        return jsonify({'error': err}), 500
    return jsonify({"result": data})

# 错误处理
@app.errorhandler(Exception)
def error_handler(e):
    return jsonify({'error': repr(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=False)
